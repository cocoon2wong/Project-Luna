"""
@Author: Conghao Wong
@Date: 2023-07-18 15:40:17
@LastEditors: Conghao Wong
@LastEditTime: 2023-10-16 10:57:40
@Description: file content
@Github: https://cocoon2wong.github.io
@Copyright 2023 Conghao Wong, All Rights Reserved.
"""

from codes import nba

"""
IMPORTANT NOTE
---

Before making the NBA dataset files, you need to download their original
dataset files (636 `7z` files in total, like `10.30.2015.UTA.at.PHI`), 
them put all of them into (please make the folder manually)
`dataset_original/NBA/metadata`.
"""

if __name__ == '__main__':
    ds = nba.NBADataset()
    gamenames = './NBA/gamenames.lst'  # ds.get_game_names()
    ds.add_clips(gamenames)
    ds.save_clips_info()
    ds.save_splits_info()
    