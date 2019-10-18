import os


class FileCorrector(object):

    def __init__(self, root_dir, target_ext):
        # error handling
        if not os.path.exists(root_dir):
            raise Exception(f'directory not exists: {root_dir}')
        # get dirs
        child_dirs = []
        for cd in os.listdir(root_dir):
            if not os.path.isdir(os.path.join(root_dir, cd)):
                continue
            if cd.startswith('.'):
                continue
            child_dirs.append(cd)
        # error handling
        if len(child_dirs) < 2:
            raise Exception(f'num of child dirs must be larger than 2: {child_dirs}')
        if not target_ext.startswith('.'):
            raise Exception(f'target_ext must be started with ".": {target_ext}')
        # init
        self.root_dir = root_dir
        self.child_dirs = child_dirs
        self.target_ext = target_ext

    def _get_files(self, dirname):
        files = []
        dpath = os.path.join(self.root_dir, dirname)
        for fname in os.listdir(dpath):
            fpath = os.path.join(dpath, fname)
            if not os.path.isfile(fpath):
                continue
            if os.path.splitext(fname)[1] == self.target_ext:
                files.append(fname)
        if len(files) == 0:
            raise Exception(f'there is no {self.target_ext} in {dpath}')
        return files

    def correct(self):
        cs = []
        for child_dir in self.child_dirs:
            files = self._get_files(child_dir)
            cs.append({
                'dirname': child_dir,
                'files': files
            })
        return {
            'root': self.root_dir,
            'target_ext': self.target_ext,
            'contents': cs
        }
