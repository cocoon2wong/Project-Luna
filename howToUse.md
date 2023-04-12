---
layout: page
title: Steps to Initialize Dataset Files
# cover-img: /assets/img/2022-03-03/cat.jpeg
---
<!--
 * @Author: Conghao Wong
 * @Date: 2023-03-21 17:52:21
 * @LastEditors: Conghao Wong
 * @LastEditTime: 2023-04-12 09:20:28
 * @Description: file content
 * @Github: https://cocoon2wong.github.io
 * Copyright 2023 Conghao Wong, All Rights Reserved.
-->

Since the code in this repository does not contain dataset files, you need to execute some of the following commands before you run the code for the first time, otherwise the program will not run correctly.
These commands only need to be executed once for each code repo.

## Steps

### Step 1: Initialize the dataset repo

---

As this repository contains only codes, you may need to download the original dataset files first.

1. If you have cloned the code repository with `git clone` command, you can initialize the dataset files by the following command:

    ```bash
    git submodule update --init --recursive
    ```

2. Or you can just download this dataset repo [here](https://github.com/cocoon2wong/Project-Luna), rename it into `dataset_original` and put it into the root path of the code repo.
    (For example, `Vertial/dataset_original`.)
    After downloading, you still need to initialize the dataset repo by running

    ```bash
    git submodule update --init --recursive
    ```

After initializing, navigate to the root path of the *dataset repo*:

```bash
cd dataset_original
```

### Step 2: Transform Dataset Files

---

Different researchers have built different read and use APIs for different datasets.
In order for these different dataset files to be used in our training structure, you need to run the following commands to transform them.

{: .box-note}
**Note:** Make sure you have navigated to the root path of the dataset repo before running the following steps.

{: .box-note}
**Note:** For dataset split and settings, please refer to [HERE](/Project-Luna/notes).

#### (a) ETH-UCY and SDD

Dataset files of ETH-UCY benchmark and Stanford Drone Dataset have been uploaded to our [dataset repo](https://github.com/cocoon2wong/Project-Luna).
You can run the following command to transform them easily:

```bash
python main_ethucysdd.py
```

#### (b) nuScenes

Researchers of the nuScenes dataset have provide a complete set of python user interfaces for using their dataset files.
Due to the file size limit, you may need to first head over to [their home page](https://nuscenes.org/nuscenes) to download the full dataset file (full dataset, v1.0).

After downloading, please unzip the file and place the two folders inside, including `v1.0-trainval` and `maps`, into `nuscenes-devkit/data/sets/nuscenes/`.
(If the folder does not exist, please create them accordingly.)

Then, run the following command to finish transforming.

```bash
python main_nuscenes.py
```

### Step 3: Create Soft Links

---

Run the following commands to create soft links so that the created files can be read directly by the training codes.

```bash
cd ..
ln -s dataset_original/dataset_processed ./
ln -s dataset_original/dataset_configs ./
```

### Step 4: Check the Linked Files

---

After running all the above commands, your training repo should contain these folders:

```
/ (Training repo's root path)
|____...
|____dataset_configs
|____dataset_original
|____dataset_processed
|____...
```

If these folders do not appear, please check the above contents carefully.
Good Luck!