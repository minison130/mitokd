import dicom2nifti
from dicom2nifti.exceptions import ConversionValidationError
from logging import getLogger
import os

logger = getLogger(__name__)


def convert(original_dicom_directory, output_file,
            reorient_nifti=True):
    try:
        __func = dicom2nifti.dicom_series_to_nifti
        __func(original_dicom_directory,
               output_file,
               reorient_nifti=reorient_nifti)
    except ConversionValidationError as e:
        logger.error('[FAILD]{}:{}'.format(str(e), original_dicom_directory))
    except Exception as e:
        raise e


def convert_dcm(dcm_dir, output_file):
    output_filename = os.path.basename(output_file)
    if os.path.splitext(output_filename)[1] != '.nii':
        raise Exception('output extension must be ".nii"')
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    convert(dcm_dir, output_file)
    logger.debug('convert {} to {}'.format(dcm_dir, output_file))


def convert_dcm_batch(dcm_root, output_root):
    for root, dirs, files in os.walk(dcm_root):
        if len(dirs) != 0:
            continue
        for fi in files:
            if os.path.splitext(fi)[1] == '.dcm':
                break
        else:
            continue
        dcm_dir = root
        relative_dir = os.path.relpath(dcm_dir, start=dcm_root)
        output_file = os.path.join(output_root, relative_dir + '.nii')
        convert_dcm(dcm_dir, output_file)
