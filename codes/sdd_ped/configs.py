"""
@Author: Conghao Wong
@Date: 2022-08-01 17:46:33
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-01 18:29:54
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

DATASET = 'SDD_ped'
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

TEST_SETS = ['hyang7_ped',
             'hyang11_ped',
             'bookstore6_ped',
             'nexus3_ped',
             'deathCircle4_ped',
             'hyang6_ped',
             'hyang3_ped',
             'little1_ped',
             'hyang13_ped',
             'gates8_ped',
             'gates7_ped',
             'hyang2_ped']

TRAIN_SETS = ['quad0_ped',
              'quad1_ped',
              'quad3_ped',
              'little0_ped',
              'deathCircle0_ped',
              'deathCircle1_ped',
              'deathCircle2_ped',
              'deathCircle3_ped',
              'hyang0_ped',
              'hyang1_ped',
              'hyang5_ped',
              'hyang8_ped',
              'hyang10_ped',
              'hyang12_ped',
              'hyang14_ped',
              'nexus0_ped',
              'nexus1_ped',
              'nexus2_ped',
              'nexus5_ped',
              'nexus6_ped',
              'nexus8_ped',
              'nexus9_ped',
              'nexus10_ped',
              'nexus11_ped',
              'coupa0_ped',
              'coupa2_ped',
              'coupa3_ped',
              'bookstore0_ped',
              'bookstore1_ped',
              'bookstore2_ped',
              'bookstore4_ped',
              'bookstore5_ped',
              'gates0_ped',
              'gates2_ped',
              'gates5_ped',
              'gates6_ped']

VAL_SETS = ['nexus7_ped',
            'coupa1_ped',
            'gates4_ped',
            'little2_ped',
            'bookstore3_ped',
            'little3_ped',
            'nexus4_ped',
            'hyang4_ped',
            'gates3_ped',
            'quad2_ped',
            'gates1_ped',
            'hyang9_ped']

SUBSETS = TRAIN_SETS + TEST_SETS + VAL_SETS
