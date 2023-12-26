import json
import glob
import os
import numpy as np
from animal_detection.app.backend.detection.processing.preprocessing import prepare_get_paths_for_detection_id, get_detection_dir_path
from animal_detection.app.backend.detection.constants import *

class Detection:
    
    def __init__(self, metadata, detections_data_raw, detections_data_clean, original_image_file, result_image_file, image_ext, original_file_path) -> None:
        self.metadata = metadata
        self.detections_data_raw = detections_data_raw
        self.detections_data_clean = detections_data_clean
        self.original_image_file = original_image_file
        self.result_image_file = result_image_file
        self.image_ext = image_ext
        self.original_file_path = original_file_path


def read_detection(detection_id, read_all=False):
    image_ext = get_image_extension_for_detection(detection_id)
    paths = prepare_get_paths_for_detection_id(detection_id, image_ext)
    
    original_file_path, detections_raw_data_path, detections_clean_data_path, \
    detection_params_path, result_image_path = \
        paths['original_file_path'], paths['detections_raw_data_path'], paths['detections_clean_data_path'], \
        paths['detection_params_path'], paths['result_image_path']
    
    return Detection(
        read_json(detection_params_path),
        read_np(detections_raw_data_path) if read_all else None,
        read_json(detections_clean_data_path),
        read_image(original_file_path) if read_all else None,
        read_image(result_image_path) if read_all else None,
        image_ext,
        original_file_path
    )
    
    
def get_image_extension_for_detection(detection_id):
    image_path = glob.glob(os.path.join(get_detection_dir_path(detection_id), 'original_image*'))[0]
    return os.path.splitext(image_path)[1]


def read_json(path):
    with open(path, 'r') as file:
        return json.load(file)
    
def read_np(path):
    return np.load(path, allow_pickle=True)


def read_image(path):
    with open(path, "rb") as image:
        return image.read()


def get_all_detection_ids():
    existing_detections = glob.glob(os.path.join(DETECTIONS_PATH, '*'))
    return sorted([int(os.path.basename(d)) for d in existing_detections])