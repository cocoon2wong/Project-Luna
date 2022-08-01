"""
@Author: Conghao Wong
@Date: 2022-08-01 17:46:33
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-01 18:21:34
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

DATASET = 'SDD'
TYPE = 'pixel'
SCALE = 100.0
SCALE_VIS = 2.0
DIMENSION = 4
ANNTYPE = 'boundingbox'

CLIP_CONFIG = dict(
    order=[0, 1],
    paras=[1, 30],
    video_path='./videos/sdd_{}_{}.mov',
    weights=[1.0, 0.0, 1.0, 0.0],
)

TEST_SETS = ['hyang7',
             'hyang11',
             'bookstore6',
             'nexus3',
             'deathCircle4',
             'hyang6',
             'hyang3',
             'little1',
             'hyang13',
             'gates8',
             'gates7',
             'hyang2']

TRAIN_SETS = ['quad0',
              'quad1',
              'quad3',
              'little0',
              'deathCircle0',
              'deathCircle1',
              'deathCircle2',
              'deathCircle3',
              'hyang0',
              'hyang1',
              'hyang5',
              'hyang8',
              'hyang10',
              'hyang12',
              'hyang14',
              'nexus0',
              'nexus1',
              'nexus2',
              'nexus5',
              'nexus6',
              'nexus8',
              'nexus9',
              'nexus10',
              'nexus11',
              'coupa0',
              'coupa2',
              'coupa3',
              'bookstore0',
              'bookstore1',
              'bookstore2',
              'bookstore4',
              'bookstore5',
              'gates0',
              'gates2',
              'gates5',
              'gates6']

VAL_SETS = ['nexus7',
            'coupa1',
            'gates4',
            'little2',
            'bookstore3',
            'little3',
            'nexus4',
            'hyang4',
            'gates3',
            'quad2',
            'gates1',
            'hyang9']

SUBSETS = TRAIN_SETS + TEST_SETS + VAL_SETS
