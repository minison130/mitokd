import argparse
from util import convert_dcm


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dcm_dir', required=True)
    parser.add_argument('--output_file', required=True)
    args = parser.parse_args()

    dcm_dir = args.dcm_dir
    output_file = args.output_file
    convert_dcm(dcm_dir, output_file)
