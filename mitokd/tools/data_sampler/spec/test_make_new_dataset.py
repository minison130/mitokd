from easydict import EasyDict as edict
import os
import shutil
import sys
import unittest

sys.path.append('..')
from down_sampler import main  # noqa: E402
from file_corrector import FileCorrector  # noqa: E402
from make_new_dataset import make_new_dataset  # noqa: E402


class TestMakeDataset(unittest.TestCase):

    TEST_ROOT = './test_dir'
    _max_rate = 2.0

    def test_main(self):
        root_dir = os.path.join(self.TEST_ROOT, 'normal_dir')
        fc = FileCorrector(root_dir, '.txt')
        d = main(edict(fc.correct()), self._max_rate)
        _target_root = './new_target'
        make_new_dataset(edict(d), _target_root)
        fc = FileCorrector(_target_root, '.txt')
        self.assertEqual(len(fc._get_files('00')), 10)
        self.assertEqual(len(fc._get_files('01')), 20)
        self.assertEqual(len(fc._get_files('02')), 20)
        self.assertEqual(len(fc._get_files('03')), 20)
        shutil.rmtree(_target_root)


if __name__ == '__main__':
    unittest.main()
