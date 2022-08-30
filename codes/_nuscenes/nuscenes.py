"""
@Author: Conghao Wong
@Date: 2022-08-05 10:40:20
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-30 14:42:14
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

import numpy as np

from nuscenes import NuScenes
from nuscenes.utils.splits import create_splits_scenes

from .. import dataset
from .configs import *


class NuScenesClips(dataset.VideoClip):

    def __init__(self, name: str, dataset: str, annpath: str = None,
                 order: tuple[int, int] = None, paras: tuple[int, int] = None,
                 video_path: str = None, matrix: list[float] = None,
                 datasetInfo=None, *args, **kwargs):

        super().__init__(name, dataset, annpath, order, paras,
                         video_path, matrix, datasetInfo, *args, **kwargs)

        self.ds: NuScenes = self.datasetInfo.ds

    def transfer_annotations(self):
        dat = []
        scale = self.datasetInfo.scale

        scene_token = self.ds.field2token('scene', 'name', self.name)[0]
        scene = self.ds.get('scene', scene_token)

        sample = self.ds.get('sample', scene['first_sample_token'])
        frame_id = 0

        while sample['next']:
            ann_tokens = sample['anns']
            for ann_token in ann_tokens:
                ann = self.ds.get('sample_annotation', ann_token)
                category = ann['category_name']

                try:
                    attribute_token = ann['attribute_tokens'][0]
                    attribute = self.ds.get('attribute', attribute_token)
                    attribute_name = attribute['name']
                except:
                    continue

                if 'pedestrain' in category:
                    for s in ['stroller', 'wheelchair']:
                        if s in category:
                            continue

                elif 'vehicle' in category:
                    for s in ['bicycle', 'motorcycle']:
                        if s in category:
                            continue
                    if 'parked' in attribute_name:
                        continue

                else:
                    continue

                x, y, z = ann['translation'][:3]
                a, b, c = ann['size'][:3]
                r0, r1, r2, r3 = ann['rotation'][:4]

                dat.append([frame_id,
                            ann['instance_token'][:AGENT_IDLENGTH],
                            (x-a/2)/scale, (y-b/2)/scale, (z-c/2)/scale,
                            (x+a/2)/scale, (y+b/2)/scale, (z+c/2)/scale,
                            r0, r1, r2, r3,
                            category])

            # ego vehicle
            ego_data = self.ds.get('sample_data', sample['data']['CAM_FRONT'])
            ego_ann = self.ds.get('ego_pose', ego_data['ego_pose_token'])

            x, y, z = ego_ann['translation'][:3]
            a, b, c = [4, 1.7, 1.5]
            r0, r1, r2, r3 = ego_ann['rotation'][:4]

            dat.append([frame_id,
                        'ego',
                        (x-a/2)/scale, (y-b/2)/scale, (z-c/2)/scale,
                        (x+a/2)/scale, (y+b/2)/scale, (z+c/2)/scale,
                        r0, r1, r2, r3,
                        'CAM_FRONT'])

            sample = self.ds.get('sample', sample['next'])
            frame_id += 1

        dat = np.array(dat, dtype=str)
        with open(self.TARGET_FILE, 'w+') as f:
            f.writelines([','.join(item)+'\n' for item in dat])

        print('Transfer annotation file {} done.'.format(self.TARGET_FILE))

        return dict(name=self.name,
                    dataset=self.dataset,
                    annpath=self.TARGET_FILE,
                    order=CLIP_CONFIG['order'],
                    paras=CLIP_CONFIG['paras'],
                    video_path=CLIP_CONFIG['video_path'],
                    matrix=CLIP_CONFIG['weights'],
                    datasetInfo=self.datasetInfo)


class NuScenesDataset(dataset.Dataset):

    def __init__(self, version: str, miniSplit=False) -> None:

        self.version = version
        self.miniSplit = miniSplit
        self.ds = NuScenes(version=version, dataroot=DATAROOT)
        self.set_videoClip_type(NuScenesClips)

        super().__init__(name=DATASET,
                         type=TYPE,
                         scale=SCALE,
                         scale_vis=SCALE_VIS,
                         dimension=DIMENSION,
                         anntype=ANNTYPE)

    def get_splits(self):
        splits = create_splits_scenes()
        if self.miniSplit:
            s = [[splits['mini_train'],
                  splits['mini_val'],
                  splits['mini_val'],
                  'nuScenes_mini']]
        else:
            s = [[splits['train'],
                  splits['test'],
                  splits['val'],
                  'nuScenes_v1.0']]
        return s
