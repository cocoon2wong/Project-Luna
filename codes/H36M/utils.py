"""
@Author: Conghao Wong
@Date: 2023-04-24 17:58:49
@LastEditors: Conghao Wong
@LastEditTime: 2023-04-24 18:45:30
@Description: file content
@Github: https://cocoon2wong.github.io
@Copyright 2023 Conghao Wong, All Rights Reserved.
"""

import os


class H36M():
    def __init__(self, annotation_path: str) -> None:
        """
        :param annotation_path: Root path of the unzipped annotation \
            files. For example, `'./Human3.6M/annot'`.
        """

        self.ann_path: str = annotation_path
        self.source_subsets, self.target_subsets = self.get_subsets()

    def get_subsets(self) -> tuple[list[str], list[str]]:
        all_sets = [f for f in os.listdir(self.ann_path) if f.startswith('s_')]
        target_sets = list(set([f.split('_subact')[0] for f in all_sets]))
        return all_sets, target_sets
    
    def get_ann_files_by_index(self, subject: int, action: int) -> list[str]:
        prefix = f's_{str(subject).zfill(2)}_act_{str(action).zfill(2)}_subact'
        return [os.path.join(self.ann_path, f, 'matlab_meta.txt') \
                    for f in self.source_subsets if f.startswith(prefix)]
    
    def get_subsets_by_index(self, subjects: list[int], actions: list[int]) -> list[str]:
        res = []
        for s in subjects:
            for a in actions:
                name = f's_{str(s).zfill(2)}_act_{str(a).zfill(2)}'
                if name in self.target_subsets:
                    res.append(name)
        
        return res
    