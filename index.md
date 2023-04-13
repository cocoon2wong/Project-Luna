---
layout: pageWithLink
title: Project-Luna 🌕
# subtitle: The basic setup steps to obtain dataset files used in this project
# cover-img: /assets/img/2022-03-03/cat.jpeg
# tags: [guidelines]
comments: true
---
<!--
 * @Author: Conghao Wong
 * @Date: 2023-03-21 17:52:21
 * @LastEditors: Conghao Wong
 * @LastEditTime: 2023-04-13 18:11:19
 * @Description: file content
 * @Github: https://cocoon2wong.github.io
 * Copyright 2023 Conghao Wong, All Rights Reserved.
-->

<link rel="stylesheet" type="text/css" href="./assets/css/user.css">

## Abstract

A repository for codes that are used to transform files from different datasets into a format suitable for our trajectory prediction models' training.
The code for this repository needs to be used along with a specific model's code repository.
Click on the guidelines button below to learn how to transform dataset files into the format needed for our training code.

<div style="text-align: center;">
    <a class="btn btn-colorful btn-lg" href="https://github.com/cocoon2wong/Project-Luna">🛠️ Codes</a>
    <a class="btn btn-colorful btn-lg" href="./howToUse">💡 Guidelines</a>
    <a class="btn btn-colorful btn-lg" href="./notes">⚠️ Dataset and Split Notes</a>
</div>

## Target Dataset Format

Each dataset considered for our trajectory prediction models may include different video scenes.
For better discrimination, we refer to these scenes (also called sub-datasets) as `video clips`, abbreviated as `clips`.
This project transforms existing dataset files of each `clip` with different annotation forms into a multi-line `csv` file, where each line includes:

- **Frame ID**: ID of the frame where the current agent appears;
- **Agent Name**: Name or ID the target agent;
- **A frame of Agents' *M-Dimensional Trajectory***: Include M records of real numbers to indicate the agent's current location and other information;
- **Agent Type**: Category of the target agent.

Each `clip` in the dataset needs to have a `csv` file corresponding to it that contains the above content.

## Clips' config files

The datasets we use need to include two kinds of files, including `data files` and `dataset config files`.
The `data files` are the `csv` files mentioned above, and the `data config files` include several `plist` files to illustrate some of the variables and configurations in the dataset split and each of the clips.

The config file of a specific video clip contains a `dict` that includes the following items:

- **annpath**, type=`string`: Path of the data `csv` file of this video clip;
- **dataset**, type=`string`: Name of the dataset that the video clip belongs to;
- **matrix**, type=`array`: An array of numbers to transform annotations with meters into pixels, and it is only used when drawing 2D visualized results on scene images;
- **name**, type=`string`: Name of the video clip;
- **order**, type=`array`: It is only used when drawing visualized results on 2D images to judge the x-y order of the dataset file;
- **paras**, type=`array`: It includes two numbers, where `paras[0]` is the sample interval in frames, and `paras[1]` is the frame rate of the video clip;
- **video_path**, type=`string`: Path of the video file of this clip.

You can take the config file `eth.plist` of the clip `eth` in dataset `ETH-UCY` as an example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>annpath</key>
    <string>./dataset_processed/ETH-UCY/eth/ann.csv</string>
    <key>dataset</key>
    <string>ETH-UCY</string>
    <key>matrix</key>
    <array>
        <real>17.667</real>
        <real>190.19</real>
        <real>10.338</real>
        <real>225.89</real>
    </array>
    <key>name</key>
    <string>eth</string>
    <key>order</key>
    <array>
        <integer>1</integer>
        <integer>0</integer>
    </array>
    <key>paras</key>
    <array>
        <integer>6</integer>
        <integer>25</integer>
    </array>
    <key>video_path</key>
    <string>./videos/eth.mp4</string>
</dict>
</plist>
```

## Dataset splits' config files


The config file of a dataset split contains a `dict` that includes the following items:

- **anntype**, type=`string`: Annotation type of the dataset;
- **dataset**, type=`string`: Name of the dataset;
- **dimension**, type=`integer`: Dimension of the trajectory;
- **scale**, type=`real`: Scaling factor when transforming the original data file;
- **scale_vis**, type=`real`: Scaling factor when drawing visualized results on 2D images;
- **test**, type=`array`: An array of clips to test the model;
- **train**, type=`array`: An array of clips to train the model;
- **type**, type=`string`: Annotation type; (It is now unused.)
- **val**, type=`array`: An array of clips to validate the model when training.

{: .box-note}
**Note:** Due to differences in settings, validation sets may not be included in the split of some datasets.
When creating data config files, validation sets are still needed, even though they may be the same as the test set.

You can take the config file of the **split** (NOT *clip*) `eth.plist` in dataset `ETH-UCY` as an example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>anntype</key>
    <string>coordinate</string>
    <key>dataset</key>
    <string>ETH-UCY</string>
    <key>dimension</key>
    <integer>2</integer>
    <key>scale</key>
    <real>1.0</real>
    <key>scale_vis</key>
    <real>1.0</real>
    <key>test</key>
    <array>
        <string>eth</string>
    </array>
    <key>train</key>
    <array>
        <string>hotel</string>
        <string>univ</string>
        <string>zara1</string>
        <string>zara2</string>
        <string>univ3</string>
        <string>unive</string>
        <string>zara3</string>
    </array>
    <key>type</key>
    <string>meter</string>
    <key>val</key>
    <array>
        <string>eth</string>
    </array>
</dict>
</plist>
```

## Organization of Dataset Files

Naturally, a dataset may have many `splits`, but these splits will map to the same `clip` files.
We store different dataset split files and data files in the following way, taking `ETH-UCY` as an example:

```none
/ (Storge root path)
|___dataset_configs
    |___ETH-UCY
        |___eth.plist       (⬅️ Here are all **split** config files)
        |___hotel.plist
        |___...
        |___subsets         (⬅️ It contains all **clip** config files)
            |___eth.plist
            |___hotel.plist
            |___...
|___dataset_processed
    |___ETH-UCY
        |___eth
            |___ann.csv     (⬅️ Transformed dataset annotation file in each **clip**)
        |___hotel
            |___ann.csv
        |___...
```
