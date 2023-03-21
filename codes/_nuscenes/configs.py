"""
@Author: Conghao Wong
@Date: 2022-08-05 10:40:10
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-31 20:18:49
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

DATASET = 'nuScenes'
TYPE = 'meter'
SCALE = 1.0
SCALE_VIS = 1.0
DIMENSION = 10
ANNTYPE = '3Dboundingbox-rotate'

CLIP_CONFIG = dict(
    order=[0, 1],
    paras=[1, 2],
    video_path='null',
    weights=[1.0, 1.0, 1.0, 1.0],
)

# nuScenes Configs
DATAROOT = './nuscenes-devkit/data/sets/nuscenes'
AGENT_IDLENGTH = 6
EGO_AGENT_TYPE = 'vehicle.ego_vehicle'
VAL_RATIO = 0.215
