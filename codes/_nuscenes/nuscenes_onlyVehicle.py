"""
@Author: Conghao Wong
@Date: 2022-08-31 16:34:35
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-31 20:25:48
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

import random

from nuscenes import NuScenes
from nuscenes.utils.splits import create_splits_scenes

from .. import dataset
from .configs_onlyVehicle import *
from .nuscenes import NuScenesClips


class NuScenesClips_onlyVehicle(NuScenesClips):

    only_vehicle = True

    def __init__(self, name: str, dataset: str, annpath: str = None,
                 order: tuple[int, int] = None, paras: tuple[int, int] = None,
                 video_path: str = None, matrix: list[float] = None,
                 datasetInfo=None, *args, **kwargs):

        super().__init__(name, dataset, annpath, order, paras,
                         video_path, matrix, datasetInfo, *args, **kwargs)


class NuscenesDataset_onlyVehicle(dataset.Dataset):

    def __init__(self, version: str, miniSplit=False) -> None:

        self.version = version
        self.miniSplit = miniSplit
        self.ds = NuScenes(version=version, dataroot=DATAROOT)
        self.set_videoClip_type(NuScenesClips_onlyVehicle)

        super().__init__(name=DATASET,
                         type=TYPE,
                         scale=SCALE,
                         scale_vis=SCALE_VIS,
                         dimension=DIMENSION,
                         anntype=ANNTYPE)

    def get_splits(self):
        splits = create_splits_scenes()

        if self.miniSplit:
            train = [s + '_ov' for s in splits['mini_train']]
            val = [s + '_ov' for s in splits['mini_val']]
            split_name = 'nuScenes_ov_mini'

        else:
            train = [s + '_ov' for s in splits['train']]
            val = [s + '_ov' for s in splits['val']]
            split_name = 'nuScenes_ov_v1.0'

        # not that annotations of all test sets are not available
        test_real = val
        val_real = random.sample(train, int(VAL_RATIO * len(train)))
        train_real = [d for d in train if not d in val_real]
        return [[train_real, test_real, val_real, split_name]]
        