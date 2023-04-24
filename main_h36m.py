"""
@Author: Conghao Wong
@Date: 2023-04-24 18:41:00
@LastEditors: Conghao Wong
@LastEditTime: 2023-04-24 18:51:39
@Description: file content
@Github: https://cocoon2wong.github.io
@Copyright 2023 Conghao Wong, All Rights Reserved.
"""

from codes import H36M

"""
IMPORTANT NOTE
---

For the Human3.6M dataset, you need to download their annotation
files (named `HM36_annot.zip`) from their website
http://vision.imar.ro/human3.6m/description.php, then unzip it and
put the unzipped folder `annot` into `./Human3.6M/annot`.
"""

if __name__ == '__main__':
    ds = H36M.H36MDataset('./Human3.6M/annot')
    ds.add_clips(ds.subsets)
    ds.save_clips_info()
    ds.save_splits_info()
    