"""
@Author: Conghao Wong
@Date: 2022-08-01 15:59:44
@LastEditors: Conghao Wong
@LastEditTime: 2023-03-21 09:37:29
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

from codes import _nuscenes

if __name__ == '__main__':

    # nuScenes and nuScenes_ov
    for nuSceneDataset in [
        _nuscenes.NuScenesDataset,
        # _nuscenes.NuscenesDataset_onlyVehicle
    ]:
        ds = nuSceneDataset(version='v1.0-trainval')
        ds.add_clips(ds.subsets)
        ds.save_clips_info()

        for _ in [0, 1]:
            ds.save_splits_info()
            ds.miniSplit = True
