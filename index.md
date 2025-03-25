---
layout: page
title: Project-Luna 🌕
# table-of-contents: true
# subtitle: The basic setup steps to obtain dataset files used in this project
cover-img: /subassets/img/homepage.png
# tags: [guidelines]
comments: true
---
<!--
 * @Author: Conghao Wong
 * @Date: 2023-03-21 17:52:21
 * @LastEditors: Conghao Wong
 * @LastEditTime: 2024-10-08 15:27:46
 * @Description: file content
 * @Github: https://cocoon2wong.github.io
 * Copyright 2023 Conghao Wong, All Rights Reserved.
-->

## Abstract

This repository is used to transform original files from different trajectory prediction datasets into a uniform format for our trajectory prediction models' training and  evaluation.
Click the following buttons for more information and details of train/test/validation splits:

<div style="text-align: center;">
    <a class="btn btn-colorful btn-lg" href="https://github.com/cocoon2wong/Project-Luna">🛠️ Codes</a>
    <a class="btn btn-colorful btn-lg" href="./notes">⚠️ Dataset & Splits Notes</a>
    <br><br>
</div>

## How To Use

To start training or testing our trajectory prediction models, please click the following button to transform dataset files.

<div style="text-align: center;">
    <a class="btn btn-colorful btn-lg" href="./howToUse">💡 Transform Dataset Files</a>
    <br><br>
    <a class="btn btn-colorful btn-lg" href="./formats">💡 File Formats & Validate on Your Own Datasets</a>
    <br><br>
</div>

## Supported Models and Datasets

The code for this repository needs to be used along with a specific model's code repository.
It currently supports the following trajectory prediction models:

<div style="text-align: center;">
    <a class="btn btn-colorful btn-lg" href="https://github.com/cocoon2wong/E-Vertical">🔗 E-Vertical</a>
    <a class="btn btn-colorful btn-lg" href="https://github.com/cocoon2wong/SocialCircle">🔗 SocialCircle</a>
    <a class="btn btn-colorful btn-lg" href="https://github.com/cocoon2wong/SocialCirclePlus">🔗 SocialCirclePlus</a>
</div>

The following datasets are supported to train or test our trajectory prediction models:

- ***ETH*** [1] - ***UCY*** [2] Benchmark:
  - 2D Coordinate;
- ***Stanford Drone Dataset*** [3]:
  - 2D Coordinate;
  - 2D Bounding Box;
- ***nuScenes*** [4]:
  - 2D Coordinate;
  - 3D Bounding Box;
  - 3D Bounding Box with Rotation;
- ***NBA SportVU*** [5]:
  - 2D Coordinate;
- ***Human3.6M*** [6,7]:
  - 3D Human Skeleton (17 Points);
- *TBA*...

---

1. S. Pellegrini, A. Ess, K. Schindler, and L. Van Gool, “You’ll never walk alone: Modeling social behavior for multi-target tracking,” in 2009 IEEE 12th International Conference on Computer Vision. IEEE, 2009, pp. 261–268.
2. A. Lerner, Y. Chrysanthou, and D. Lischinski, “Crowds by example,” Computer Graphics Forum, vol. 26, no. 3, pp. 655–664, 2007.
3. A. Robicquet, A. Sadeghian, A. Alahi, and S. Savarese, “Learning social etiquette: Human trajectory understanding in crowded scenes,” in European conference on computer vision. Springer, 2016, pp. 549–565.
4. A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom, “nuscenes: A multimodal dataset for autonomous driving,” arXiv preprint arXiv:1903.11027, 2019.
5. K. Linou, D. Linou, and M. de Boer, “Nba player movements,” https://github.com/linouk23/NBA-Player-Movements, 2016.
6. C. Ionescu, D. Papava, V. Olaru, and C. Sminchisescu, “Human3.6m: Large scale datasets and predictive methods for 3d humansensing in natural environments,” IEEE transactions on patternanalysis and machine intelligence, vol. 36, no. 7, pp. 1325–1339, 2013.
7. C. S. Catalin Ionescu, Fuxin Li, “Latent structured models for human pose estimation,” in International Conference on Computer Vision, 2011.

<div style="text-align: center">🌕🌕🌕</div>
