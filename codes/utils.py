"""
@Author: Conghao Wong
@Date: 2022-08-01 15:53:37
@LastEditors: Conghao Wong
@LastEditTime: 2023-05-29 15:47:15
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

import os
import plistlib

SEG_IMG = 'segmentation_image'
RGB_IMG = 'rgb_image'


def dir_check(target_dir: str) -> str:
    """
    Used for check if the `target_dir` exists.
    It not exist, it will make it.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    return target_dir


def load_from_plist(path: str) -> dict:
    """
    Load plist files into python `dict` object.

    :param path: path of the plist file
    :return dat: a `dict` object loaded from the file
    """
    with open(path, 'rb') as f:
        dat = plistlib.load(f)

    return dat


def write_plist(value: dict, path: str):
    with open(path, 'wb+') as f:
        plistlib.dump(value, f)
