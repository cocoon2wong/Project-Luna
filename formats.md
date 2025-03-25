---
layout: page
table-of-contents: true
title: File Formats & Validate on Your Own Datasets
---
<!--
 * @Author: Conghao Wong
 * @Date: 2024-10-08 15:22:35
 * @LastEditors: Conghao Wong
 * @LastEditTime: 2025-03-25 14:35:24
 * @Github: https://cocoon2wong.github.io
 * Copyright 2024 Conghao Wong, All Rights Reserved.
-->

## Organization of Dataset Files

A dataset can have multiple video clips (or subsets), and the way we split these clips into different train, test, and validation sets is the corresponding split.
This means that a dataset can have multiple splits, but these splits will all refer to the same clip files.
Our processed dataset files have two main parts: the data files in the `./dataset_processed` folder and the config files in the `./dataset_configs` folder.
We store different dataset split files and data files in the following way, using `ETH-UCY` as an example:

```html
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

You can also organize data files and config files in the same way to test or train models on your own datasets.
A dataset contains at least three kinds of files, `split file`s, `clip file`s, and `data file`s.
The formats of these files will be introduced below.

## Format of a Split File

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

> [!NOTE]
> Due to differences in settings, validation sets may not be included in the split of some datasets.
> When creating data config files, validation sets are still needed, even though they may be the same as the test set.

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

## Format of a Clip File

A `clip file` is also a `plist` file that save some of the variables and configurations in each of the video clips.
It contains a `dict` that includes the following items:

- **annpath**, type=`string`: Path of the data `csv` file of this video clip;
- **dataset**, type=`string`: Name of the dataset that the video clip belongs to;
- **matrix**, type=`array`: An array of numbers to transform annotations with meters into pixels, and it is only used when drawing 2D visualized results on scene images;
- **name**, type=`string`: Name of the video clip;
- **order**, type=`array`: ~~It is only used when drawing visualized results on 2D images to judge the x-y order of the dataset file.~~ **This item is now DEPRECATED, please leave it a null array**;
- **other_files**: *(Optional)* Other paths of the related files, like the static RGB images or segmentaton maps of the video clip;
- **paras**, type=`array`: It includes two numbers, where `paras[0]` is the sample interval in frames, and `paras[1]` is the frame rate of the video clip;
- **video_path**, type=`string`: Path of the video file of this clip.

You can take the config file `zara1.plist` of the video clip `zara1` in dataset `ETH-UCY` as an example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>annpath</key>
    <string>./dataset_processed/ETH-UCY/zara1/ann.csv</string>
    <key>dataset</key>
    <string>ETH-UCY</string>
    <key>matrix</key>
    <array>
        <real>-42.54748107</real>
        <real>580.5664891</real>
        <real>47.29369894</real>
        <real>3.196071003</real>
    </array>
    <key>name</key>
    <string>zara1</string>
    <key>order</key>
    <array>
        <integer>0</integer>
        <integer>1</integer>
    </array>
    <key>other_files</key>
    <dict>
        <key>rgb_image</key>
        <string>./dataset_processed/ETH-UCY/zara1/ref.png</string>
        <key>segmentation_image</key>
        <string>./dataset_processed/ETH-UCY/zara1/seg.png</string>
    </dict>
    <key>paras</key>
    <array>
        <integer>10</integer>
        <integer>25</integer>
    </array>
    <key>video_path</key>
    <string>./videos/zara1.mp4</string>
</dict>
</plist>
```

## Format of a Data File

We transform existing dataset files of each `clip` with different annotation formats into a multi-line `csv` file, where each line includes:

- **Frame ID**: ID of the frame where the current agent appears;
- **Agent Name**: Name or ID the target agent;
- **A frame of Agents' *M-Dimensional Trajectory***: Include M records of real numbers to indicate the agent's current location and other information;
- **Agent Type**: Category of the target agent.

Especially, the *M-Dimensional Trajectory* term may change over different `anntype` settings within the corresponding `split file`.
For 2D Coordinate cases (`anntype==coordinate`), it contains two numbers, `x` and `y`.
For 2D Bounding Box cases (`anntype==boundingbox`), it contains four numbers, `x_left`, `y_left`, `x_right`, `y_right`.

Each `clip` in the dataset needs to have a `csv` file corresponding to it that contains the above content.
Take the `zara1.csv` file of the `zara1` clip (2D coordinate) as an example, it contains

```xml
0,1,3.9379,13.449,Pedestrain,
0,2,4.4391,13.343,Pedestrain,
0,3,4.4391,11.912,Pedestrain,
0,4,5.1551,11.828,Pedestrain,
0,5,4.4152,8.7133,Pedestrain,
...
```

Take the `bookstore0.csv` (SDD, 2D bounding box) as an example, it contains

```xml
10064,0,10.51,1.99,10.83,2.27,"Biker"
10065,0,10.49,1.99,10.81,2.27,"Biker"
10066,0,10.47,2.01,10.78,2.29,"Biker"
10067,0,10.44,2.03,10.76,2.31,"Biker"
10068,0,10.42,2.03,10.74,2.31,"Biker"
...
```
