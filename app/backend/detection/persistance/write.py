import json
import os
import numpy as np
import shutil
import cv2
import datetime
from animal_detection.app.backend.detection.processing.preprocessing import prepare_get_paths_for_detection_id, get_detection_dir_path
from animal_detection.app.backend.detection.processing.postprocessing import raw_detections_to_clean_detections

def write_detection(image_original_request_file, detections_np, image_result_array, detection_id, boxes_count=1, score_threshold=0.2):
    image_ext = os.path.splitext(image_original_request_file.name)[1]
    paths = prepare_get_paths_for_detection_id(detection_id, image_ext)
    
    original_file_path, detections_raw_data_path, detections_clean_data_path, \
    detection_params_path, result_image_path = \
        paths['original_file_path'], paths['detections_raw_data_path'], paths['detections_clean_data_path'], \
        paths['detection_params_path'], paths['result_image_path']
        
    write_detection_metadata(detection_params_path, image_result_array, boxes_count, score_threshold, image_original_request_file.name)
    write_original_image_file(original_file_path, image_original_request_file)
    write_raw_detections_data(detections_raw_data_path, detections_np)
    write_clean_detection_data(detections_clean_data_path, detections_np, image_result_array, boxes_count, score_threshold)
    write_result_image(result_image_path, image_result_array)


def write_detection_metadata(detection_params_path, image_array, boxes_count, score_threshold, filename):
    with open(detection_params_path, 'w+') as destination:
        result = {
            'boxes_count': boxes_count,
            'score_threshold': score_threshold,
            'image_height': image_array.shape[0],
            'image_width': image_array.shape[1],
            'timestamp': int(datetime.datetime.now().timestamp()),
            'filename': filename
        }
        json.dump(result, destination)


def write_original_image_file(original_file_path, image_request_file):
    with open(original_file_path, "wb+") as destination:
        for chunk in image_request_file.chunks():
            destination.write(chunk)


def write_raw_detections_data(detections_raw_data_path, detections_np):
    np.save(detections_raw_data_path, detections_np)

    
def write_clean_detection_data(detections_clean_data_path, detections_raw_np, image_result_array, boxes_count, score_threshold):
    clean_detections = raw_detections_to_clean_detections(detections_raw_np, boxes_count, score_threshold, image_result_array.shape[0], image_result_array.shape[1])
    with open(detections_clean_data_path, 'w+') as destination:
        json.dump(clean_detections, destination)

        
def write_result_image(result_image_path, image_result_array):
    cv2.imwrite(result_image_path, image_result_array)


def delete_detection(detection_id):
    dir = get_detection_dir_path(detection_id)
    if (os.path.isdir(dir)):
        shutil.rmtree(dir)
