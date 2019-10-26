import numpy as np
import pydicom


class ModalityException(Exception):
    pass


class DicomCTConverter(object):

    def __init__(self, dcm_file):
        self.dcm_file = dcm_file
        self.ds = pydicom.read_file(dcm_file)
        _md = self.ds.Modality
        if _md != 'CT':
            raise ModalityException(f'Unsupported modality: {_md}')
        self.window_center = self.ds.WindowCenter
        self.window_width = self.ds.WindowWidth

    def set_window(self, w):
        """Args: (window_center, window_width)"""
        if w[0] is not None:
            self.window_center = w[0]
        if w[1] is not None:
            self.window_width = w[1]

    def get_window(self):
        return self.window_center, self.window_width

    def get_file_dataset(self):
        return self.ds

    def get_pixel_max_min(self):
        im = self.ds.pixel_array
        return np.max(im), np.min(im)

    def get_im_array(self):
        im = self.ds.pixel_array.astype(np.float)
        # windowing
        _window_min = self.window_center - (self.window_width / 2)
        im -= _window_min
        im /= self.window_width
        im[im > 1] = 1
        im[im < 0] = 0
        # to be 8bit
        im *= 255
        im = im.astype(np.uint8)
        return im
