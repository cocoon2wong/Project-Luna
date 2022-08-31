"""
@Author: Conghao Wong
@Date: 2022-08-01 15:59:44
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-31 20:50:54
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

from codes import _nuscenes, ethucy, nba, sdd, sdd_ped

if __name__ == '__main__':

    # ETH-UCY and SDD
    for structure in [
        ethucy.ETHUCYDataset,
        sdd.SDDDataset,
        # sdd_ped.SDDDataset
    ]:
        ds = structure()
        ds.add_clips(ds.subsets)
        ds.save_clips_info()
        ds.save_splits_info()

    # NBA
    ds = nba.NBADataset()
    gamenames = './NBA/gamenames.lst'  # ds.get_game_names()
    ds.add_clips(gamenames, force_update=True)
    ds.save_clips_info()
    ds.save_splits_info()

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
