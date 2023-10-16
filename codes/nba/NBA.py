"""
@Author: Conghao Wong
@Date: 2022-08-01 18:45:05
@LastEditors: Conghao Wong
@LastEditTime: 2023-10-16 16:17:51
@Description: file content
@Github: https://github.com/cocoon2wong
@Copyright 2022 Conghao Wong, All Rights Reserved.
"""

import os
import random

import py7zr
from tqdm import tqdm

from NBA.codes.Game import EventError, Game

from .. import dataset
from ..utils import RGB_IMG, dir_check, load_from_plist
from .configs import *


class NBAClips(dataset.VideoClip):

    SOURCE_FILE = './NBA/metadata/{}.json'
    other_files = {RGB_IMG: './videos/NBA_court.png'}

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
        line = '{},{},{},{},{}\n'

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

            # Add players
            for player in moment.players:
                name = event.player_ids_dict[player.id][0]
                lines.append(line.format(frame_id, name,
                                         player.x/SCALE, player.y/SCALE,
                                         player.team.name))

            # Add the ball
            ball = moment.ball
            lines.append(line.format(frame_id, 'Ball',
                                     ball.x/SCALE, ball.y/SCALE, 'Ball'))

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
        self.event_list_file = os.path.join(self.BASE_DIR, self.name,
                                            ALL_EVENTS_FILE_NAME)
        self.games: dict[str, Game] = {}

    def get_game_names(self):
        file_names = os.listdir(DATASET_DIR)
        zip_names = [f + ',\n' for f in file_names if f.endswith('7z')]
        random.shuffle(zip_names)

        with open(ALL_RANDOM_GAMES_FILE, 'w+') as f:
            f.writelines(zip_names)

        return ALL_RANDOM_GAMES_FILE

    def get_enevt_names(self, game_json_path: str):
        game = Game(game_json_path)
        game_name = game.game_name
        event_number = game.last_default_index

        if not game_name in self.games.keys():
            self.games[game_name] = game

        valid_event_names = []
        for event_id in range(event_number):
            game.update(event_id)
            event = game.event

            try:
                event_time_len = event.moments[0].game_clock - \
                    event.moments[-1].game_clock
                if event_time_len < MIN_EVENT_LEN:
                    raise
            except:
                # print(f'Event {event_id} from game ' +
                #       f'{game_name} too short, skip.')
                continue

            valid_event_names.append(f'{game_name}_{event_id}')

        return valid_event_names

    def get_all_event_names(self, game_names_file: str):
        with open(game_names_file, 'r') as f:
            zip_names = f.readlines()

        game_names = [n.split(',')[0][:-3] for n in zip_names]
        random.shuffle(game_names)

        all_event_names = []
        for game_name in (t := tqdm(game_names[:MAX_VISITED_GAMES],
                                    desc='Visiting games...')):
            zip_path = SOURCE_ZIP_FILE.format(game_name)
            json_path = SOURCE_FILE.format(game_name)

            if not os.path.exists(json_path):
                save_path = os.path.dirname(json_path)

                try:
                    t.set_postfix_str(f'Unzipping `{zip_path}`...')
                    with py7zr.SevenZipFile(zip_path, mode='r') as zipfile:
                        zipfile.extractall(path=save_path)
                        unzipped_name = zipfile.getnames()[0].split('.json')[0]

                        os.rename(src=SOURCE_FILE.format(unzipped_name),
                                  dst=json_path)
                except:
                    continue

            event_names = self.get_enevt_names(json_path)
            all_event_names += event_names

        with open(self.event_list_file, 'w+') as f:
            f.writelines([c + ',\n' for c in all_event_names])

        return all_event_names

    def add_clips(self, game_names_file: str, force_update=False):
        if not force_update and os.path.exists(self.event_list_file):
            print(f'Events file `{self.event_list_file}` exists. ' +
                  'Stop making dataset files from original data.')

            with open(self.event_list_file, 'r') as f:
                lines = f.readlines()

            event_names = [e.split(',')[0] for e in lines]

        else:
            print('Start sampling games ...')
            event_names = self.get_all_event_names(game_names_file)

        random.shuffle(event_names)
        for event_name in event_names[:MAX_EVENT_NUMBER]:
            vc = self.VideoClipType(event_name,
                                    dataset=self.name,
                                    datasetInfo=self)
            vc.force_update = force_update

            game_name = vc.game_id
            if not game_name in self.games.keys():
                self.games[game_name] = Game(SOURCE_FILE.format(game_name))

            if vc.get(self.games[game_name]):
                self.clips.append(vc)

    def get_splits(self):
        """
        50K (about) trajectories in total, 65% for training.
        """
        event_names = [clip.name for clip in self.clips]
        random.shuffle(event_names)

        train_number = int(TRAIN_PERCENT * len(event_names))
        val_number = int(VAL_PERCENT * (len(event_names) - train_number))

        train_sets = event_names[0:train_number]
        val_sets = event_names[train_number:train_number+val_number]
        test_sets = event_names[train_number+val_number:]

        return [[train_sets, test_sets, val_sets, SPLIT_NAME]]
