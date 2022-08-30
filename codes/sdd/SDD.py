"""
@Author: Conghao Wong
@Date: 2022-08-01 17:35:49
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-30 09:23:59
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

import re

import numpy as np

from .. import dataset
from .configs import *


class SDDClips(dataset.VideoClip):

    SOURCE_FILE = './sdd/{}/video{}/annotations.txt'

    def __init__(self, name: str, dataset: str, annpath: str = None,
                 order: tuple[int, int] = None, paras: tuple[int, int] = None,
                 video_path: str = None, matrix: list[float] = None,
                 datasetInfo=None, *args, **kwargs):

        super().__init__(name, dataset, annpath, order, paras,
                         video_path, matrix, datasetInfo, *args, **kwargs)

        self.scene = re.findall('[a-zA-Z]+', name)[0]
        self.scene_id = re.findall('[0-9]+', name)[0]

        self.SOURCE_FILE = self.SOURCE_FILE.format(self.scene, self.scene_id)

    def transfer_annotations(self):
        dat = []
        scale = self.datasetInfo.scale

        with open(self.SOURCE_FILE, 'r') as f:
            while data_original := f.readline():
                data_original = data_original[:-1]
                split = data_original.split(' ')
                if split[6] == '1':
                    continue

                dat.append([split[5],                    # frame number
                            split[0] + '_' + split[-1],  # name of the agent
                            float(split[2])/scale,
                            float(split[1])/scale,
                            float(split[4])/scale,
                            float(split[3])/scale,
                            split[-1]])

        dat = np.array(dat, dtype=str)
        with open(self.TARGET_FILE, 'w+') as f:
            f.writelines([','.join(item)+'\n' for item in dat])

        return dict(name=self.name,
                    dataset=self.dataset,
                    annpath=self.TARGET_FILE,
                    order=CLIP_CONFIG['order'],
                    paras=CLIP_CONFIG['paras'],
                    video_path=CLIP_CONFIG['video_path'].format(self.scene, self.scene_id),
                    matrix=CLIP_CONFIG['weights'],
                    datasetInfo=self.datasetInfo)


class SDDDataset(dataset.Dataset):

    def __init__(self) -> None:

        super().__init__(name=DATASET,
                         type=TYPE,
                         scale=SCALE,
                         scale_vis=SCALE_VIS,
                         dimension=DIMENSION,
                         anntype=ANNTYPE)

        self.set_videoClip_type(SDDClips)
        self.subsets = SUBSETS

    def get_splits(self):
        """
        Split from Simaug
        """
        return [[TRAIN_SETS, TEST_SETS, VAL_SETS, 'sdd']]
