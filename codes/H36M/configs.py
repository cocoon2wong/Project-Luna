"""
@Author: Conghao Wong
@Date: 2023-04-24 14:36:58
@LastEditors: Conghao Wong
@LastEditTime: 2023-04-24 18:29:09
@Description: file content
@Github: https://cocoon2wong.github.io
@Copyright 2023 Conghao Wong, All Rights Reserved.
"""

DATASET = 'Human3.6M'
TYPE = 'millimeter'
SCALE = 1.0
SCALE_VIS = 1.0
DIMENSION = 51
ANNTYPE = '3Dskeleton-17'

CLIP_CONFIG = dict(
    order=[0, 1],
    paras=[1, 50],
    video_path='null',
    weights=[1.0, 0.0, 1.0, 0.0],
)

USED_JOINT_INDEXES = [
    0,
    1,
    2,
    3,
    6,
    7,
    8,
    12,
    13,
    14,
    15,
    17,
    18,
    19,
    25,
    26,
    27,
]

USED_JOINT_3D_INDEXES = []
for _j in USED_JOINT_INDEXES:
    USED_JOINT_3D_INDEXES += [3 * _j, 3 * _j + 1, 3 * _j + 2]
