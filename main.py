"""
@Author: Conghao Wong
@Date: 2022-08-01 15:59:44
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-01 18:43:09
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

from codes import ethucy, sdd, sdd_ped

for structure in [
    ethucy.ETHUCYDataset,
    sdd.SDDDataset,
    sdd_ped.SDDDataset
]:
    ds = structure()
    ds.add_clips(ds.subsets)
    ds.save_clips_info()
    ds.save_splits_info()
