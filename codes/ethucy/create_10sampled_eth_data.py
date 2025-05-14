"""
@Author: Conghao Wong
@Date: 2025-05-13 15:58:04
@LastEditors: Conghao Wong
@LastEditTime: 2025-05-14 16:19:53
@Github: https://cocoon2wong.github.io
@Copyright 2025 Conghao Wong, All Rights Reserved.
"""

import os
import shutil

import numpy as np
import scipy.interpolate

START_FRAME = None
FRAME_INTERVAL = 10
SAMPLE_INTERVAL = 2
DATA_SCALE = 2

ANN_FILE = 'ann.csv'
DATA_FOLDER = './dataset_processed/ETH-UCY/{}'
SPLIT_CONFIG_FILE = './dataset_configs/ETH-UCY/{}.plist'
CLIP_CONFIG_FILE = './dataset_configs/ETH-UCY/subsets/{}.plist'

CLIPS = ['eth', 'hotel', 'univ3', 'unive', 'univ', 'zara1', 'zara2', 'zara3']


def dir_check(target_dir: str) -> str:
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    return target_dir


def process_dataset_files(clip: str):
    old_folder = DATA_FOLDER.format(clip)
    new_folder = DATA_FOLDER.format(clip + '10')

    # Balance data scales, since agents in eth move rather faster
    # Coordinates in all other training sets are * 2
    coe = 1.0 if clip == 'eth' else DATA_SCALE

    with open(os.path.join(old_folder, ANN_FILE), 'r') as f:
        lines = f.readlines()

    agent_pos: dict[str, tuple[list, list]] = {}

    # Read all records
    for line in lines:
        _data = [d for d in line.split(',') if len(d)]
        _frame = int(_data[0])
        _id = _data[1]
        _x = float(_data[2]) * coe
        _y = float(_data[3]) * coe
        _type = _data[4]

        global START_FRAME
        if START_FRAME is None:
            START_FRAME = _frame

        if _id not in agent_pos.keys():
            agent_pos[_id] = ([], [])

        agent_pos[_id][0].append(_frame)
        agent_pos[_id][1].append([_x, _y])

    # Interpolate
    new_lines = []
    for _id, _data in agent_pos.items():
        _frames = np.array(_data[0])
        _pos = np.array(_data[1])
        _xs = _pos[:, 0]
        _ys = _pos[:, 1]

        _new_start = START_FRAME + \
            FRAME_INTERVAL * \
            int(np.floor((_frames[0] - START_FRAME) / FRAME_INTERVAL))
        _new_end = START_FRAME + \
            FRAME_INTERVAL * \
            int(np.ceil((_frames[-1] - START_FRAME) / FRAME_INTERVAL))

        # `SAMPLE_INTERVAL` are used to interpolate more training data
        # It should be used with `--step` arg when training
        # This arg is not currently used and is reserved for future usages
        _new_frames = np.arange(_new_start, _new_end + 1, SAMPLE_INTERVAL)
        _fx = scipy.interpolate.interp1d(
            _frames, _xs, fill_value='extrapolate')
        _fy = scipy.interpolate.interp1d(
            _frames, _ys, fill_value='extrapolate')

        _new_xs = _fx(_new_frames)
        _new_ys = _fy(_new_frames)

        for _new_frame, _new_x, _new_y in zip(
                _new_frames, _new_xs, _new_ys):
            new_lines.append(f'{_new_frame},{_id},{_new_x},{_new_y},' +
                             'Pedestrian,\n')

    # Prepare to copy all dataset files
    dir_check(new_folder)

    # Save as the new annotation file
    with open(os.path.join(new_folder, ANN_FILE), 'w+') as f:
        f.writelines(new_lines)

    # Copy other dataset files
    for file_name in os.listdir(old_folder):
        if ((file_name != ANN_FILE) and
                (not file_name.startswith('.'))):
            shutil.copyfile(source := os.path.join(old_folder, file_name),
                            target := os.path.join(new_folder, file_name))
            print(f'Copy file `{source}` -> `{target}` done.')


def process_clip_config_file(clip: str):
    old_clip_file = CLIP_CONFIG_FILE.format(clip)
    new_clip_file = CLIP_CONFIG_FILE.format(clip + '10')

    # Process the clip file
    with open(old_clip_file, 'r') as f:
        old_clip_lines = f.readlines()
        old_clip_lines = ''.join(old_clip_lines)

    old_interval = 6 if clip == 'eth' else 10

    old_clip_lines = old_clip_lines.replace(clip, clip + '10')
    old_clip_lines = old_clip_lines.replace(f'{clip}10.mp4', f'{clip}.mp4')
    old_clip_lines = old_clip_lines.replace(
        f'<integer>{old_interval}</integer>\n\t\t<integer>25</integer>',
        f'<integer>{SAMPLE_INTERVAL}</integer>\n\t\t<integer>25</integer>'
    )

    with open(new_clip_file, 'w+') as f:
        f.write(old_clip_lines)
    print(f'`{new_clip_file}` saved.')


def process_split_file(split_name: str):
    old_split_file = SPLIT_CONFIG_FILE.format(split_name)
    new_split_file = SPLIT_CONFIG_FILE.format(split_name + '10')

    # Process the split file
    with open(old_split_file, 'r') as f:
        old_split_lines = f.readlines()
        old_split_lines = ''.join(old_split_lines)

    for ds in CLIPS:
        # FIXME: Skip the hotel set since there are unknown issues
        # that lead to `nan` values when computing loss functions.
        # It means that the new split still uses the original hotel data.
        if ds == 'hotel':
            continue

        old_split_lines = old_split_lines.replace(ds + '<', ds + '10<')

    with open(new_split_file, 'w+') as f:
        f.write(old_split_lines)
    print(f'`{new_split_file}` saved.')


if __name__ == '__main__':
    for ds in CLIPS:
        process_dataset_files(ds)
        process_clip_config_file(ds)

    process_split_file('eth')
