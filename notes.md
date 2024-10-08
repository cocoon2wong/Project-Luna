---
layout: page
add-md-links: true
title: Dataset and Split Notes
# cover-img: /assets/img/2022-03-03/cat.jpeg
---
<!--
 * @Author: Conghao Wong
 * @Date: 2023-04-11 20:48:08
 * @LastEditors: Conghao Wong
 * @LastEditTime: 2024-10-08 10:39:03
 * @Description: file content
 * @Github: https://cocoon2wong.github.io
 * Copyright 2023 Conghao Wong, All Rights Reserved.
-->

## ETH-UCY and Stanford Drone Dataset

---

When making dataset files, we process the ETH-UCY dataset files by the `leave-one-out` strategy, and split SDD with the dataset split method from [SimAug](https://github.com/JunweiLiang/Multiverse) (`36 train sets` + `12 test sets` + `12 val sets`).

{: .box-note}
**Note:** Please note that we do not use dataset split files like TrajNet on ETH-UCY and SDD for several reasons.
For example, the frame rate problem in `ETH-eth` sub-dataset, and some of these splits only consider the `pedestrians` in the SDD dataset.
We process the original full-dataset files from these datasets with observations = 3.2 seconds (or 8 frames) and predictions = 4.8 seconds (or 12 frames) to train and test the model.
See details in [this issue](https://github.com/cocoon2wong/Vertical/issues/1).

## nuScenes

---

Since the official test set in the nuScenes dataset has no labels, we use the following method to split the training set:

- `550 Train sets`: Randomly sampling 550 video clips from the official 850 training sets;
- `150 Val sets`: Randomly sampling the other 150 video clips from the official 850 training sets;
- `150 Test sets`: We treat the official 150 val sets as our test sets.

You can also change these split settings in `/dataset_original/codes/_nuscenes/nuscenes.py`.

## Human3.6M

---

Following previous settings, we use all data from subjects `[1, 6, 7, 8, 9]` to train the model, subjects `[11]` to validate, and subjects `[5]` to test.

When making the training samples, we sample observations with the frequency of `25Hz` (*i.e.*, the sample interval is `40ms`) and use `t_h = 10` frames (`400ms`) of observations from all subjects to predict their possible trajectories for the next `t_f = 10` frames (`400ms`).
