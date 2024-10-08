---
layout: page
add-md-links: true
title: Transform Dataset Files
# cover-img: /assets/img/2022-03-03/cat.jpeg
---
<!--
 * @Author: Conghao Wong
 * @Date: 2023-03-21 17:52:21
 * @LastEditors: Conghao Wong
 * @LastEditTime: 2024-10-08 16:42:15
 * @Description: file content
 * @Github: https://cocoon2wong.github.io
 * Copyright 2023 Conghao Wong, All Rights Reserved.
-->

## Abstract

This dataset repository acts as a submodule within the prediction model's code repository.
Since it doesn't include our processed dataset files, you'll need to run these commands before using any of our trajectory prediction model's code repositories.
These commands should only be executed once for each code repository.
Before running the operations, make sure you're in the correct repository folder.

## Step 1: Initialize the dataset repo

You can run the following commands to initializ this dataset repo in any of our code repos.
After initializing, navigate to the root path of the **dataset repo**.

1. If you have cloned the **code repository** with `git clone` command, you can initialize this dataset repo in the **code repo** (for example, E-Vertical, SocialCircle) by the following command:

    ```bash
    git submodule update --init --recursive
    cd dataset_original
    ```

2. Or you can clone  this **dataset repo** separately, and put it into any paths:

    ```bash
    git clone https://github.com/cocoon2wong/Project-Luna.git
    cd Project-Luna
    ```

Make sure that you are now in the **dataset repo**.

## Step 2: Transform Dataset Files

Researchers have created various data formats and APIs for users to train or test models on their proposed datasets.
To make these dataset files compatible with our training structure, you'll need to run these commands.

{: .box-warning}
**⚠️ Warning:** Make sure you have navigated to the root path of this **dataset repo** before running the following steps.

{: .box-note}
**ℹ️ Note:** For the settings and details about datasets and splits, please refer to [this page](../notes).

### (a) ETH-UCY and SDD

Dataset files of ETH-UCY benchmark and Stanford Drone Dataset have been uploaded to this dataset repo in `./ethucy` and `./sdd`.
You can run the following command to transform them into our new format:

```bash
python main_ethucysdd.py
```

### (b) nuScenes

Developers of the nuScenes dataset have provided a complete set of Python user interfaces for using their dataset files.
We have include their original codes (forked as [https://github.com/cocoon2wong/nuscenes-devkit](https://github.com/cocoon2wong/nuscenes-devkit)) as a `submodule` in this repo.
Due to the file size limitations and copyright reasons, you may need to first head over to [their home page](https://nuscenes.org/nuscenes) to download the full dataset file (full dataset, v1.0).

After downloading, please unzip the file and place the two folders inside into this **dataset repo**, including `v1.0-trainval` and `maps`, into `./nuscenes-devkit/data/sets/nuscenes/`.
(If the folder does not exist, please create them accordingly.)

Then, run the following command to finish transforming:

```bash
python main_nuscenes.py
```

### (c) NBA SportVU

Developers of the NBA dataset have also provided their original codes, which we have forked as [https://github.com/cocoon2wong/NBA-Player-Movements](https://github.com/cocoon2wong/NBA-Player-Movements) and made into a `submodule`.

Due to the size limitations and copyright reasons, we have omitted these original dataset files.
Before making the transformed NBA dataset files, you need to download their original
dataset files (636 `7z` files in total from their original repo [https://github.com/linouk23/NBA-Player-Movements](https://github.com/linouk23/NBA-Player-Movements) in the `data` directory, like `10.30.2015.UTA.at.PHI`), then put all of them into `dataset_original/NBA/metadata` (please create the folders manually).

Then, run the following command to finish transforming:

```bash
python main_nba.py
```

### (d) Human3.6M

Due to license restrictions, you may need to register for an account and download the dataset file from [their official website](http://vision.imar.ro/human3.6m/description.php).
In detail, you need to download their annotation file (named `HM36_annot.zip`), then unzip it and put the unzipped folder `annot` into `Human3.6M/`.
(If the folder does not exist, please create it manually.)

Then, run the following command to finish transforming.

```bash
python main_h36m.py
```

## Step 3: Create Soft Links

Run the following commands to create soft links so that the created files can be read directly by the training codes.
Before running, make sure that you are now in the **dataset repo** inside the **code repo**.

```bash
cd ..
ln -s dataset_original/dataset_processed ./
ln -s dataset_original/dataset_configs ./
```

Here, `dataset_original` is the default name of this **dataset repo** that plays as a `submodule` in some **code repo**.
If you have cloned this **dataset repo** manually, please change the corresponding paths to make sure that the `source path` of the soft link points to the `dataset_processed` and the `dataset_configs` folders inside the **dataset repo**, and the `target path` of the soft link points to the **code repo**.

## Step 4: Check the Linked Files

After running all the above commands, your **code repo** should contain these folders:

```xml
/ (Code repo's root path)
|____...
|____dataset_configs
|____dataset_original (Optional)
|____dataset_processed
|____...
```

If these folders do not appear, please check the above contents carefully.
Good Luck!
