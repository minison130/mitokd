import argparse
from util import convert_dcm_batch


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dcm_root', required=True)
    parser.add_argument('--output_root', required=True)
    args = parser.parse_args()

    dcm_root = args.dcm_root
    output_root = args.output_root

    convert_dcm_batch(dcm_root, output_root)
