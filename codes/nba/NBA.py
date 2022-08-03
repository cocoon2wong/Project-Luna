"""
@Author: Conghao Wong
@Date: 2022-08-01 18:45:05
@LastEditors: Conghao Wong
@LastEditTime: 2022-08-02 16:44:09
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

import os
import random

import py7zr

from NBA.codes.Game import EventError, Game

from .. import dataset
from ..utils import dir_check, load_from_plist
from .configs import *


class NBAClips(dataset.VideoClip):

    SOURCE_FILE = './NBA/metadata/{}.json'

    def __init__(self, name: str, dataset: str, annpath: str = None,
                 order: tuple[int, int] = None, paras: tuple[int, int] = None,
                 video_path: str = None, matrix: list[float] = None,
                 datasetInfo=None, *args, **kwargs):

        super().__init__(name, dataset, annpath, order, paras,
                         video_path, matrix, datasetInfo, *args, **kwargs)

        self.game_id = name.split('_')[0]
        self.event_id = int(name.split('_')[1])

        self.SOURCE_FILE = self.SOURCE_FILE.format(self.game_id)

    def transfer_annotations(self, game: Game):
        fname = self.TARGET_FILE
        config_dic = dict(name=self.name,
                          dataset=self.dataset,
                          annpath=self.TARGET_FILE,
                          order=CLIP_CONFIG['order'],
                          paras=CLIP_CONFIG['paras'],
                          video_path=CLIP_CONFIG['video_path'],
                          matrix=CLIP_CONFIG['weights'],
                          datasetInfo=self.datasetInfo)

        if os.path.exists(fname):
            print(f'Dataset file {fname} exists, skip.')
            return config_dic
        else:
            fdir = os.path.dirname(fname)
            dir_check(fdir)

        try:
            game = game.update(self.event_id)
        except EventError:
            return None

        event = game.event

        quarter_clock = QUARTER
        quarter_clock_ms = int(1000 * quarter_clock)

        lines = []
        line = '{},{},{},{},{},\n'

        try:
            event_time_len = event.moments[0].game_clock - \
                event.moments[-1].game_clock
            if event_time_len < MIN_EVENT_LEN:
                raise
        except:
            print(
                f'Event {self.event_id} from game {self.game_id} too short, skip.')
            return None

        for moment in event.moments:
            q = moment.quarter

            clock = moment.game_clock
            clock_ms = int(1000 * clock)

            real_clock_ms = q * quarter_clock_ms - clock_ms
            real_clock = real_clock_ms/1000.0

            frame_id = int(real_clock/FRAME_STEP)

            if frame_id % (SAMPLE_STEP / FRAME_STEP) != 0:
                continue

            for player in moment.players:
                _t = player.team.name
                _n = event.player_ids_dict[player.id][0]
                name = '{} {}'.format(_t, _n).replace(' ', '_')
                lines.append(line.format(frame_id, name,
                                         player.x/SCALE, player.y/SCALE,
                                         player.team.name))

        with open(fname, 'w+') as f:
            f.writelines(lines)

        print(f'Dataset file {fname} saved.')

        return config_dic

    def get(self, game: Game):
        plist_path = self.CONFIG_FILE

        if self.force_update or not os.path.exists(plist_path):
            dic = self.transfer_annotations(game)
            if dic is None:
                return None
        else:
            dic = load_from_plist(plist_path)

        self.__init__(**dic)
        return self


class NBADataset(dataset.Dataset):

    def __init__(self) -> None:

        super().__init__(name=DATASET,
                         type=TYPE,
                         scale=SCALE,
                         scale_vis=SCALE_VIS,
                         dimension=DIMENSION,
                         anntype=ANNTYPE)

        self.set_videoClip_type(NBAClips)

    def get_game_names(self):
        file_names = os.listdir(DATASET_DIR)
        zip_names = [f + ',\n' for f in file_names if f.endswith('7z')]
        random.shuffle(zip_names)

        with open(ALL_RANDOM_GAMES_FILE, 'w+') as f:
            f.writelines(zip_names)

        return ALL_RANDOM_GAMES_FILE

    def make_events(self, game_json_path: str, force_update=False):
        game = Game(game_json_path)
        game_name = game.game_name
        event_number = game.last_default_index

        event_count = 0
        clip_names = []
        for event_id in range(event_number):
            name = f'{game_name}_{event_id}'
            vc = self.VideoClipType(name=name, dataset=self.name,
                                    datasetInfo=self)
            vc.force_update = force_update

            if vc.get(game):
                event_count += 1
                self.clips.append(vc)
                clip_names.append(f'{game_name}_{event_id}')

        return event_count, clip_names

    def add_clips(self, game_names_file: str, force_update=False):

        with open(game_names_file, 'r') as f:
            zip_names = f.readlines()

        game_names = [n.split(',')[0][:-3] for n in zip_names]

        event_count = 0
        all_clip_names = []

        for game_name in game_names:
            if event_count > MAX_EVENT_NUMBER:
                break

            zip_path = SOURCE_ZIP_FILE.format(game_name)
            json_path = SOURCE_FILE.format(game_name)

            if not os.path.exists(json_path):
                save_path = os.path.dirname(json_path)

                try:
                    with py7zr.SevenZipFile(zip_path, mode='r') as zipfile:
                        zipfile.extractall(path=save_path)
                        unzipped_name = zipfile.getnames()[0].split('.json')[0]

                        os.rename(src=SOURCE_FILE.format(unzipped_name),
                                  dst=json_path)
                except:
                    continue

            newevent_count, clip_names = self.make_events(
                json_path, force_update)

            event_count += newevent_count
            all_clip_names += clip_names

        with open(ALL_EVENTS_FILE, 'w+') as f:
            f.writelines([c + ',\n' for c in all_clip_names])

    def get_splits(self):
        """
        Split from Simaug
        """
        event_names = [clip.name for clip in self.clips]
        random.shuffle(event_names)
        train_number = int(TRAIN_PERCENT * len(event_names))
        val_number = int(VAL_PERCENT * (len(event_names) - train_number))

        train_sets = event_names[0:train_number]
        val_sets = event_names[train_number:train_number+val_number]
        test_sets = event_names[train_number+val_number:]

        return [[train_sets, test_sets, val_sets, SPLIT_NAME]]
