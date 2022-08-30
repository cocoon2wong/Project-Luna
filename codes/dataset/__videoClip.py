"""
@Author: Conghao Wong
@Date: 2022-08-01 15:42:08
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-30 09:22:45
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

import os

from ..utils import dir_check, load_from_plist, write_plist


class VideoClip():
    """
    VideoClip
    ---------
    Base structure for controlling each video dataset.

    Properties
    -----------------
    ```python
    >>> self.annpath        # dataset annotation file
    >>> self.dimension      # annotation dimension
    >>> self.matrix         # transfer matrix from real scales to pixels
    >>> self.name           # video clip name
    >>> self.paras          # [sample_step, frame_rate]
    >>> self.video_path     # video path    
    ```
    """

    # Dataset annotation files
    PROCESSED_FILE = 'ann.csv'
    SOURCE_FILE = None
    TARGET_FILE = './dataset_processed/{}/{}/' + PROCESSED_FILE

    # Saving paths
    BASE_DIR = './dataset_configs'
    CONFIG_FILE = os.path.join(BASE_DIR, '{}', 'subsets', '{}.plist')

    saveKeys = ['name', 'annpath', 'order',
                'paras', 'video_path',
                         'matrix', 'dataset']

    def __init__(self, name: str,
                 dataset: str,
                 annpath: str = None,
                 order: tuple[int, int] = None,
                 paras: tuple[int, int] = None,
                 video_path: str = None,
                 matrix: list[float] = None,
                 datasetInfo=None,
                 *args, **kwargs):

        self.__name = name
        self.__annpath = annpath
        self.__order = order
        self.__paras = paras
        self.__video_path = video_path
        self.__matrix = matrix
        self.__dataset = dataset

        self.datasetInfo = datasetInfo
        self.force_update = False

        self.TARGET_FILE = self.TARGET_FILE.format(self.dataset, self.name)
        self.CONFIG_FILE = self.CONFIG_FILE.format(self.dataset, self.name)

        # make dirs
        dirs = [self.TARGET_FILE, self.CONFIG_FILE]
        for d in dirs:
            _dir = os.path.dirname(d)
            dir_check(_dir)

    @property
    def dataset(self) -> str:
        """
        Name of the dataset.
        """
        return self.__dataset

    @property
    def name(self):
        """
        Name of the video clip.
        """
        return self.__name

    @property
    def annpath(self) -> str:
        """
        Path of the annotation file. 
        """
        return self.__annpath

    @property
    def order(self) -> list[int]:
        """
        X-Y order in the annotation file.
        """
        return self.__order

    @property
    def paras(self) -> tuple[int, int]:
        """
        [sample_step, frame_rate]
        """
        return self.__paras

    @property
    def video_path(self) -> str:
        """
        Path of the video file.
        """
        return self.__video_path

    @property
    def matrix(self) -> list[float]:
        """
        transfer weights from real scales to pixels.
        """
        return self.__matrix

    def transfer_annotations(self):
        raise NotImplementedError(
            'Please re-write this method when subclassing.')

    def get(self):
        plist_path = self.CONFIG_FILE

        if self.force_update or not os.path.exists(plist_path):
            dic = self.transfer_annotations()
            print(f'Transfer annotation file {self.TARGET_FILE} done.')
        else:
            dic = load_from_plist(plist_path)
            dic['datasetInfo'] = self.datasetInfo
            print(f'Load annotation file {self.TARGET_FILE} done.')

        self.__init__(**dic)
        return self

    def save_info(self):
        """
        Save dataset information into `plist` files.
        """
        values = [getattr(self, name) for name in self.saveKeys]
        dic = dict(zip(self.saveKeys, values))
        write_plist(dic, self.CONFIG_FILE)
        print(f'Successfully saved at {self.CONFIG_FILE}')
