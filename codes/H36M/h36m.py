"""
@Author: Conghao Wong
@Date: 2023-04-24 10:16:19
@LastEditors: Conghao Wong
@LastEditTime: 2023-04-24 20:56:02
@Description: file content
@Github: https://cocoon2wong.github.io
@Copyright 2023 Conghao Wong, All Rights Reserved.
"""

import numpy as np

from .. import dataset
from .configs import *
from .utils import H36M


class H36MClips(dataset.VideoClip):

    def __init__(self, name: str, dataset: str, annpath: str = None,
                 order: tuple[int, int] = None, paras: tuple[int, int] = None,
                 video_path: str = None, matrix: list[float] = None,
                 datasetInfo=None, *args, **kwargs):

        super().__init__(name, dataset, annpath, order, paras,
                         video_path, matrix, datasetInfo, *args, **kwargs)

        # example name: 's_06_act_12'
        name_list = name.split('_')
        self.subject: int = int(name_list[1])
        self.action: int = int(name_list[3])

        self.datasetInfo: H36MDataset
        self.source_files = self.datasetInfo.ds.get_ann_files_by_index(
            self.subject, self.action)

    def transfer_annotations(self):
        dat = []
        scale = self.datasetInfo.scale
        indexes = USED_JOINT_3D_INDEXES
        frame_number = 0

        for source_file in self.source_files:
            with open(source_file, 'r') as f:
                while data_original := f.readline():
                    data_original = data_original[:-1]
                    split = data_original.split(' ')

                    if split[0] != 'pos':
                        continue
                    else:
                        split = split[1:]

                    _dat = [float(split[index])/scale for index in indexes]
                    dat.append([frame_number, self.subject] +
                               _dat + ['Subject'])

                    frame_number += 1

        dat = np.array(dat, dtype=str)
        with open(self.TARGET_FILE, 'w+') as f:
            f.writelines([','.join(item)+'\n' for item in dat])

        return dict(name=self.name,
                    dataset=self.dataset,
                    annpath=self.TARGET_FILE,
                    order=CLIP_CONFIG['order'],
                    paras=CLIP_CONFIG['paras'],
                    video_path=CLIP_CONFIG['video_path'],
                    matrix=CLIP_CONFIG['weights'],
                    datasetInfo=self.datasetInfo)


class H36MDataset(dataset.Dataset):

    def __init__(self, annotation_path: str) -> None:

        self.ds = H36M(annotation_path)
        self.subsets = self.ds.target_subsets
        self.set_videoClip_type(H36MClips)

        super().__init__(name=DATASET,
                         type=TYPE,
                         scale=SCALE,
                         scale_vis=SCALE_VIS,
                         dimension=DIMENSION,
                         anntype=ANNTYPE)

    def get_splits(self):

        # [train_subjects, test_subjects, val_subjects]
        subjects = [[1, 6, 7, 8, 9], [5], [11]]
        actions = np.arange(17)

        return [[self.ds.get_subsets_by_index(subjects[0], actions),
                 self.ds.get_subsets_by_index(subjects[1], actions),
                 self.ds.get_subsets_by_index(subjects[2], actions), 'h36m']]
