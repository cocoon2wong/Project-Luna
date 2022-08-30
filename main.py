"""
@Author: Conghao Wong
@Date: 2022-08-01 15:59:44
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-30 14:40:14
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

from codes import _nuscenes, ethucy, nba, sdd, sdd_ped

if __name__ == '__main__':

    # for structure in [
    #     ethucy.ETHUCYDataset,
    #     sdd.SDDDataset,
    #     sdd_ped.SDDDataset
    # ]:
    #     ds = structure()
    #     ds.add_clips(ds.subsets)
    #     ds.save_clips_info()
    #     ds.save_splits_info()

    # ds = nba.NBADataset()
    # gamenames = './NBA/gamenames.lst'  # ds.get_game_names()
    # ds.add_clips(gamenames, force_update=True)
    # ds.save_clips_info()
    # ds.save_splits_info()

    a = _nuscenes.NuScenesDataset(version='v1.0-trainval')
    b = _nuscenes.NuScenesDataset(version='v1.0-test')

    train, test, val = a.get_splits()[0][:3]
    a.add_clips(train + val)
    a.add_clips(test, datasetInfo=b)
    a.save_clips_info()

    for _ in [0, 1]:
        a.save_splits_info()
        a.miniSplit = True
