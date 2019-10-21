import argparse
import copy
from easydict import EasyDict as edict
import json
from logging import DEBUG
from logging import getLogger
from logging import StreamHandler
import os
import random

from file_corrector import FileCorrector

logger = getLogger(__name__)
handler = StreamHandler()
logger.setLevel(DEBUG)
logger.addHandler(handler)


def main(file_table, max_rate):
    _min = min(len(c.files) for c in file_table.contents)
    max_choices = int(_min * max_rate)
    logger.info(f'min = {_min}, max_rate = {max_rate}')

    _file_table = copy.deepcopy(file_table)
    for c in _file_table.contents:
        if len(c.files) < max_choices:
            sampled_files = c.files
            logger.debug(f'{c.dirname} has {len(c.files)} files to {len(c.files)}.')
        else:
            random.seed(0)  # init seed
            sampled_files = random.sample(c.files, max_choices)
            logger.debug(f'{c.dirname} has {len(c.files)} files to {max_choices}.')
        c.files = sampled_files
    return _file_table


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', required=True)
    parser.add_argument('--output_json', required=True)
    parser.add_argument('--max_rate', type=float, default=2.)
    parser.add_argument('--target_ext', default='.png')
    args = parser.parse_args()

    root_dir = args.root_dir
    max_rate = args.max_rate
    target_ext = args.target_ext
    output_json = args.output_json
    if os.path.splitext(output_json)[1] != '.json':
        raise Exception(f'output_json must be "*.json": {output_json}')

    fc = FileCorrector(root_dir, target_ext)
    file_table = edict(fc.correct())
    sample_file_table = main(file_table, max_rate)

    with open(output_json, 'w') as f:
        json.dump(sample_file_table, f, indent=4)
        logger.debug(f'output json to {output_json}')
