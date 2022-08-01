"""
@Author: Conghao Wong
@Date: 2022-08-01 16:05:26
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-01 18:34:07
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

import numpy as np

from .. import dataset
from .configs import *


class ETHUCYClips(dataset.VideoClip):

    SOURCE_FILE = './ethucy/{}/true_pos_.csv'

    def __init__(self, name: str, dataset: str, annpath: str = None,
                 order: tuple[int, int] = None, paras: tuple[int, int] = None,
                 video_path: str = None, matrix: list[float] = None,
                 datasetInfo=None, *args, **kwargs):

        super().__init__(name, dataset, annpath, order, paras,
                         video_path, matrix, datasetInfo, *args, **kwargs)

        self.SOURCE_FILE = self.SOURCE_FILE.format(self.name)

    def transfer_annotations(self):
        data_original = np.loadtxt(self.SOURCE_FILE, delimiter=',')
        r = data_original[2:].T

        config = CLIP_CONFIGS[self.name]
        weights = [1.0, 0.0, 1.0, 0.0]
        order = config['order']

        result = np.column_stack([
            weights[0] * r.T[0] + weights[1],
            weights[2] * r.T[1] + weights[3],
        ])/self.datasetInfo.scale

        dat = np.column_stack([data_original[0].astype(int).astype(str),
                               data_original[1].astype(int).astype(str),
                               result.T[order[0]].astype(str),
                               result.T[order[1]].astype(str)])

        with open(self.TARGET_FILE, 'w+') as f:
            for _dat in dat:
                f.writelines([','.join(_dat)+',Pedestrain,\n'])

        print('{} Done.'.format(self.TARGET_FILE))

        return dict(name=self.name,
                    dataset=self.dataset,
                    annpath=self.SOURCE_FILE,
                    order=order,
                    paras=config['paras'],
                    video_path=config['video_path'],
                    matrix=config['weights'],
                    datasetInfo=self.datasetInfo)


class ETHUCYDataset(dataset.Dataset):

    def __init__(self) -> None:

        super().__init__(name=DATASET,
                         type=TYPE,
                         scale=SCALE,
                         scale_vis=SCALE_VIS,
                         dimension=DIMENSION,
                         anntype=ANNTYPE)

        self.set_videoClip_type(ETHUCYClips)
        self.subsets = SUBSETS

    def get_splits(self):
        """
        Leave One Out
        """
        splits = []
        for ds in TESTSETS:
            train_sets = []
            test_sets = []
            val_sets = []

            for d in SUBSETS:
                if d == ds:
                    test_sets.append(d)
                    val_sets.append(d)
                else:
                    train_sets.append(d)

            splits.append([train_sets, test_sets, val_sets, ds])

        return splits
