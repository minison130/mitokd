import argparse
import cv2
import os
from tqdm import tqdm

from dicom_ct_converter import DicomCTConverter


def get_convert_table(dcm_root, output_root):
    table = []
    target_exts = ['.dcm', '.DCM']
    for root, dirs, files in os.walk(dcm_root):
        if len(dirs) > 0:
            continue
        for f in files:
            if not os.path.splitext(f)[1] in target_exts:
                continue
            d = {}
            d['input_dcm'] = os.path.join(root, f)
            _relpath = os.path.relpath(root, start=dcm_root)
            d['output_dir'] = os.path.join(output_root, _relpath)
            table.append(d)
    return table


def make_png(dcmfile, output_dir, window):
    dc = DicomCTConverter(dcmfile)
    dc.set_window(window)
    im = dc.get_im_array()
    w = dc.get_window()
    filename = os.path.splitext(os.path.basename(dcmfile))[0]
    output_png = f'{filename}_c{str(w[0])}_w{str(w[1])}.png'
    output_path = os.path.join(output_dir, output_png)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cv2.imwrite(output_path, im)


def _set_window(center, width):
    if center is not None:
        center = int(center)
    if width is not None:
        width = int(width)
    return (center, width)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_root', required=True)
    parser.add_argument('-o', '--output_root', required=True)
    parser.add_argument('-wc', '--window_center', default=None)
    parser.add_argument('-ww', '--window_width', default=None)
    args = parser.parse_args()

    # handle arguments
    input_root = args.input_root
    output_root = args.output_root
    window = _set_window(args.window_center, args.window_width)

    # parse
    convert_table = get_convert_table(input_root, output_root)
    for ct in tqdm(convert_table):
        make_png(ct['input_dcm'], ct['output_dir'], window)
