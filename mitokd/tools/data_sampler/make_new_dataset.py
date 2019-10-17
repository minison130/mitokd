import argparse
from easydict import EasyDict as edict
import json
from logging import DEBUG
from logging import getLogger
from logging import StreamHandler
import os
import shutil

logger = getLogger(__name__)
handler = StreamHandler()
logger.setLevel(DEBUG)
logger.addHandler(handler)


def make_new_dataset(table, target_root):
    for c in table.contents:
        logger.debug(f'== {c.dirname} ==')
        rdir = os.path.join(table.root, c.dirname)
        tdir = os.path.join(target_root, c.dirname)
        os.makedirs(tdir)
        for fl in c.files:
            rf = os.path.join(rdir, fl)
            tf = os.path.join(tdir, fl)
            shutil.copyfile(rf, tf)
            logger.debug(f'copy {fl}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_json', required=True)
    parser.add_argument('--target_root', required=True)
    args = parser.parse_args()

    input_json = args.input_json
    target_root = args.target_root

    if os.path.exists(target_root):
        raise Exception(f'target_root must be unexisted. {target_root}')

    sample_table = edict(json.load(open(input_json, 'r')))
    make_new_dataset(sample_table, target_root)
