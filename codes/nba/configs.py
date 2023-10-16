"""
@Author: Conghao Wong
@Date: 2022-08-01 18:44:59
@LastEditors: Conghao Wong
@LastEditTime: 2023-10-16 19:15:01
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

DATASET = 'NBA'
TYPE = 'foot'
SCALE = 1.0
SCALE_VIS = 1.0
DIMENSION = 2
ANNTYPE = 'coordinate'
SPLIT_NAME = 'nba50k'

CLIP_CONFIG = dict(
    order=[1, 0],
    paras=[10, 25],
    video_path='none',
    weights=[10.0, 0.0, 10.0, 0.0],
)

# only for NBA dataset
DATASET_DIR = './NBA/metadata'
ALL_RANDOM_GAMES_FILE = './NBA/gamenames.lst'
ALL_EVENTS_FILE_NAME = 'events.lst'
SOURCE_FILE = './NBA/metadata/{}.json'
SOURCE_ZIP_FILE = './NBA/metadata/{}.7z'

# Number of events (video clips) to make
# This value only works for (obs, pred) = (5, 10)
MAX_EVENT_NUMBER = 135

# Max number of games to sample trajectories
MAX_VISITED_GAMES = 30

FRAME_STEP = 0.04
SAMPLE_STEP = 0.4
SAMPLE_STEP_MS = int(SAMPLE_STEP * 1000)

QUARTER = 12 * 60
MIN_EVENT_LEN = 9.0

# This split only works for (obs, pred) = (5, 10)
TRAIN_PERCENT = 0.65
VAL_PERCENT = 0.2857
