import argparse
import cv2
import glob
import os
from tqdm import tqdm

from dicom_ct_converter import DicomCTConverter
from convert import _set_window


def get_scout_convert_table(dcm_root, output_root,
                            scout_length_thresh=2):
    table = []
    target_exts = ['.dcm', '.DCM']
    for root, dirs, files in os.walk(dcm_root):
        if len(dirs) > 0:
            continue
        counts = 0
        for f in files:
            if os.path.splitext(f)[1] in target_exts:
                counts +=1
        if counts > scout_length_thresh:
            continue
        for f in files:
            if not os.path.splitext(f)[1] in target_exts:
                continue
            d = {}
            d['input_dcm'] = os.path.join(root, f)
            _relpath = os.path.relpath(root, start=dcm_root)
            d['output_dir'] = os.path.join(output_root)
            d['output_prefix'] = root.split('/')[-2]
            table.append(d)
    return table


def make_png(dcmfile, output_dir, output_prefix, window):
    dc = DicomCTConverter(dcmfile)
    dc.set_window(window)
    im = dc.get_im_array()
    w = dc.get_window()
    filename = os.path.splitext(os.path.basename(dcmfile))[0]
    output_png = f'{output_prefix}_c{str(w[0])}_w{str(w[1])}.png'
    output_path = os.path.join(output_dir, output_png)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cv2.imwrite(output_path, im)



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
    convert_table = get_scout_convert_table(input_root, output_root)
    for ct in tqdm(convert_table):
        make_png(ct['input_dcm'], ct['output_dir'], ct['output_prefix'], window)
