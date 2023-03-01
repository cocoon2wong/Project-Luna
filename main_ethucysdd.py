"""
@Author: Conghao Wong
@Date: 2022-08-01 15:59:44
@LastEditors: Beihao Xia
@LastEditTime: 2023-03-01 16:01:39
@Description: file content
@Github: https://cocoon2wong.github.io
@Copyright 2023 Conghao Wong, All Rights Reserved.
"""

from codes import ethucy, sdd

if __name__ == '__main__':

    # ETH-UCY and SDD
    for structure in [
        ethucy.ETHUCYDataset,
        sdd.SDDDataset,
    ]:
        ds = structure()
        ds.add_clips(ds.subsets)
        ds.save_clips_info()
        ds.save_splits_info()
