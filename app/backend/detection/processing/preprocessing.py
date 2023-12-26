import os
import glob

from animal_detection.app.backend.detection.constants import *

def get_new_detection_id():
    if not os.path.exists(DETECTIONS_PATH):
        os.makedirs(DETECTIONS_PATH)
    
    detections_ids = get_all_detection_ids()
    count = len(detections_ids)
    if (count >= 1) and (count <= 1000):
        detection_id = detections_ids[-1] + 1
    elif count == 0:
        detection_id = 1
    else:
        raise IndexError
    return detection_id

def get_detection_dir_path(detection_id):
    return os.path.join(DETECTIONS_PATH, str(detection_id))


def get_original_image_path(detection_id, image_ext):
    detection_path = get_detection_dir_path(detection_id)
    return os.path.join(detection_path, ORIGINAL_IMAGE_FILE_NAME_NO_EXTENSION + image_ext)


def prepare_get_paths_for_detection_id(detection_id, image_ext):
    detection_path = os.path.join(DETECTIONS_PATH, str(detection_id))
    original_file_path = os.path.join(detection_path, ORIGINAL_IMAGE_FILE_NAME_NO_EXTENSION + image_ext)
    detections_raw_data_path = os.path.join(detection_path, DETECTIONS_RAW_DATA_FILE_NAME)
    detections_clean_data_path = os.path.join(detection_path, DETECTIONS_CLEANED_DATA_FILE_NAME)
    detection_params_path = os.path.join(detection_path, DETECTION_META_DATA_FILE_NAME)
    result_image_path = os.path.join(detection_path, RESULT_IMAGE_FILE_NAME_NO_EXTENSION + image_ext)
    
    if not os.path.isdir(detection_path):
        os.makedirs(detection_path)
    
    return {
        'detection_path': detection_path,
        'original_file_path': original_file_path,
        'detections_raw_data_path': detections_raw_data_path,
        'detections_clean_data_path': detections_clean_data_path,
        'detection_params_path': detection_params_path,
        'result_image_path': result_image_path
    }
    
    
def get_all_detection_ids():
    existing_detections = glob.glob(os.path.join(DETECTIONS_PATH, '*'))
    return sorted([int(os.path.basename(d)) for d in existing_detections])


def extract_params_from_request(request_object):
    boxes_count = int(request_object['boxes_count']) if 'boxes_count' in request_object else BOXES_COUNT_DEFAULT
    score_threshold = float(request_object['score_threshold']) if 'score_threshold' in request_object else SCORE_THRESHOLD_DEFAULT
    return boxes_count, score_threshold