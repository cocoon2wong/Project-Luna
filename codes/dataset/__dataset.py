"""
@Author: Conghao Wong
@Date: 2022-08-01 15:34:30
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-30 14:45:49
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

import os

from ..utils import dir_check, write_plist
from .__videoClip import VideoClip


class Dataset():
    """
    Dataset
    -------
    Manage a full trajectory prediction dataset.
    A dataset may contains several video clips.
    """

    VideoClipType = VideoClip

    # Saving paths
    BASE_DIR = './dataset_configs'
    CONFIG_FILE = os.path.join(BASE_DIR, '{}', '{}.plist')

    def __init__(self, name: str,
                 type: str,
                 scale: float,
                 scale_vis: float,
                 dimension: int,
                 anntype: str) -> None:

        self.__name = name
        self.__type = type
        self.__scale = scale
        self.__scale_vis = scale_vis
        self.__dimension = dimension
        self.__anntype = anntype

        self.subsets: list[str] = []
        self.clips: list[VideoClip] = []
        self.CONFIG_FILE = self.CONFIG_FILE.format(self.name, '{}')

        config_dir = os.path.dirname(self.CONFIG_FILE)
        dir_check(config_dir)
        self.get_subset_list()

    def set_videoClip_type(self, new_type: type[VideoClip]):
        self.VideoClipType = new_type

    def add_clips(self, clips: list[str], force_update=False, datasetInfo=None):
        if datasetInfo is None:
            datasetInfo = self

        for clip in clips:
            vc = self.VideoClipType(name=clip, dataset=self.name,
                                    datasetInfo=datasetInfo)
            vc.force_update = force_update
            self.clips.append(vc.get())

    def save_clips_info(self):
        for clip in self.clips:
            clip.save_info()

    def get_splits(self):
        raise NotImplementedError(
            'Please re-write this method when subclassing.')

    def get_subset_list(self):
        for split in self.get_splits():
            for item in split[:-1]:
                for set in item:
                    if not set in self.subsets:
                        self.subsets.append(set)

        self.subsets.sort()

    def save_splits_info(self):
        for split in self.get_splits():
            dic = dict(train=split[0],
                       test=split[1],
                       val=split[2],
                       dataset=self.name,
                       scale=self.scale,
                       dimension=self.dimension,
                       scale_vis=self.scale_vis,
                       anntype=self.anntype,
                       type=self.type)

            write_plist(dic, p := self.CONFIG_FILE.format(split[-1]))
            print('Successfully saved at {}'.format(p))

    @property
    def name(self) -> str:
        """
        Name of the video dataset.
        For example, `ETH-UCY` or `SDD`.
        """
        return self.__name

    @property
    def type(self) -> str:
        """
        Annotation type of the dataset.
        For example, `'pixel'` or `'meter'`.
        """
        return self.__type

    @property
    def scale(self) -> float:
        """
        Global data scaling scale.
        """
        return self.__scale

    @property
    def scale_vis(self) -> float:
        """
        Video scaling when saving visualized results.
        """
        return self.__scale_vis

    @property
    def dimension(self) -> int:
        """
        Maximum dimension of trajectories recorded in this dataset.
        For example, `(x, y)` -> `dimension = 2`.
        """
        return self.__dimension

    @property
    def anntype(self) -> str:
        """
        Type of annotations.
        For example, `'coordinate'` or `'boundingbox'`.
        """
        return self.__anntype
