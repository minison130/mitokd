from easydict import EasyDict as edict
import os
import sys
import unittest

sys.path.append('..')
from down_sampler import main  # noqa: E402
from file_corrector import FileCorrector  # noqa: E402


class TestDownSampler(unittest.TestCase):

    TEST_ROOT = './test_dir'

    def test_main(self):
        root_dir = os.path.join(self.TEST_ROOT, 'normal_dir')
        fc = FileCorrector(root_dir, '.txt')
        _max_rate = 2.0
        d = main(file_table=edict(fc.correct()), max_rate=_max_rate)
        lengths = []
        for cnt in d.contents:
            lengths.append(len(cnt.files))
        _min = min(lengths)
        for lgt in lengths:
            self.assertTrue(lgt <= int(_min * _max_rate))


if __name__ == '__main__':
    unittest.main()
