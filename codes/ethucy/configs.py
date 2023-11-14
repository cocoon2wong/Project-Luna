"""
@Author: Conghao Wong
@Date: 2022-08-01 16:13:24
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-02 11:39:58
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

DATASET = 'ETH-UCY'
TYPE = 'meter'
SCALE = 1.0
SCALE_VIS = 1.0
DIMENSION = 2
ANNTYPE = 'coordinate'

TESTSETS = ['eth', 'hotel', 'univ', 'zara1', 'zara2']
SUBSETS = ['eth', 'hotel', 'univ', 'zara1', 'zara2',
           'univ3', 'unive', 'zara3']

CLIP_CONFIGS: dict = {}

CLIP_CONFIGS['eth'] = dict(
    order=[1, 0],
    paras=[6, 25],
    video_path='./videos/eth.mp4',
    weights=[17.667, 190.19, 23, 200],
)

CLIP_CONFIGS['hotel'] = dict(
    order=[1, 0],
    paras=[10, 25],
    video_path='./videos/hotel.mp4',
    weights=[44.788, 310.07, 48.308, 497.08],
)

CLIP_CONFIGS['zara1'] = dict(
    order=[0, 1],
    paras=[10, 25],
    video_path='./videos/zara1.mp4',
    weights=[-42.54748107, 580.5664891, 47.29369894, 3.196071003],
)

CLIP_CONFIGS['zara2'] = dict(
    order=[0, 1],
    paras=[10, 25],
    video_path='./videos/zara2.mp4',
    weights=[-42.54748107, 580.5664891, 47.29369894, 3.196071003],
)

CLIP_CONFIGS['univ'] = dict(
    order=[0, 1],
    paras=[10, 25],
    video_path='./videos/students003.mp4',
    weights=[-41.1428, 576, 48, 0],
)

CLIP_CONFIGS['zara3'] = dict(
    order=[0, 1],
    paras=[10, 25],
    video_path='./videos/zara2.mp4',
    weights=[-42.54748107, 580.5664891, 47.29369894, 3.196071003]
)

CLIP_CONFIGS['univ3'] = dict(
    order=[0, 1],
    paras=[10, 25],
    video_path='./videos/students003.mp4',
    weights=[-41.1428, 576, 48, 0],
)

CLIP_CONFIGS['unive'] = dict(
    order=[0, 1],
    paras=[10, 25],
    video_path='./videos/students003.mp4',
    weights=[-41.1428, 576, 48, 0],
)
