from cerberus import Validator
import os
import sys
import unittest

sys.path.append('..')
from file_corrector import FileCorrector  # noqa: E402


class TestFileCorrector(unittest.TestCase):

    TEST_ROOT = './test_dir'

    def test_init(self):
        # normal
        root_dir = os.path.join(self.TEST_ROOT, 'normal_dir')
        FileCorrector(root_dir, '.txt')
        # error
        with self.assertRaises(FileNotFoundError):
            FileCorrector('hoge', '.txt')
        with self.assertRaises(ValueError):
            FileCorrector(self.TEST_ROOT, '.txt')
        with self.assertRaises(ValueError):
            FileCorrector(root_dir, 'txt')

    def test_get_files(self):
        # normal
        root_dir = os.path.join(self.TEST_ROOT, 'normal_dir')
        fc = FileCorrector(root_dir, '.txt')
        self.assertEqual(len(fc._get_files('00')), 10)
        self.assertEqual(len(fc._get_files('01')), 200)
        self.assertEqual(len(fc._get_files('02')), 400)
        self.assertEqual(len(fc._get_files('03')), 30)
        # error
        fc = FileCorrector(root_dir, '.png')
        with self.assertRaises(FileNotFoundError):
            fc._get_files('00')

    def test_correct(self):
        T, S, R = ['type', 'schema', 'required']
        v = Validator({
            'root': {T: 'string', R: True},
            'target_ext': {T: 'string', R: True},
            'contents': {
                T: 'list',
                R: True,
                S: {
                    T: 'dict',
                    R: True,
                    S: {
                        'dirname': {T: 'string', R: True},
                        'files': {
                            T: 'list',
                            R: True,
                            S: {
                                T: 'string',
                                R: True
                            }
                        }
                    }
                }
            }
        })
        root_dir = os.path.join(self.TEST_ROOT, 'normal_dir')
        fc = FileCorrector(root_dir, '.txt')
        d = fc.correct()
        v.validate(d)
        self.assertEqual(v.errors, {})


if __name__ == '__main__':
    unittest.main()
