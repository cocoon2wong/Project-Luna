"""
@Author: Conghao Wong
@Date: 2022-08-01 18:44:59
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-02 11:20:49
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

DATASET = 'NBA'
TYPE = 'meter'
SCALE = 1.0
SCALE_VIS = 1.0
DIMENSION = 2
ANNTYPE = 'coordinate'
SPLIT_NAME = 'nba4000'

CLIP_CONFIG = dict(
    order=[1, 0],
    paras=[10, 25],
    video_path='./dataset_original/NBA/court.png',
    weights=[10.0, 0.0, 10.0, 0.0],
)

# only for NBA dataset
DATASET_DIR = './NBA/metadata'
ALL_RANDOM_GAMES_FILE = './NBA/gamenames.lst'
ALL_EVENTS_FILE = './NBA/events.lst'
SOURCE_FILE = './NBA/metadata/{}.json'
SOURCE_ZIP_FILE = './NBA/metadata/{}.7z'

FRAME_STEP = 0.04
SAMPLE_STEP = 0.4
SAMPLE_STEP_MS = int(SAMPLE_STEP * 1000)

QUARTER = 12 * 60
MIN_EVENT_LEN = 9.0
MAX_EVENT_NUMBER = 4000

TRAIN_PERCENT = 0.7
VAL_PERCENT = 0.3
