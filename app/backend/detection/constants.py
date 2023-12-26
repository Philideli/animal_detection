import os

from animal_detection.app.backend.breed_detection.settings import PERSISTENCE_PATH, CACHE_PATH as CACHE_PATH_ORIGINAL

DETECTIONS_PATH = os.path.join(PERSISTENCE_PATH, 'detections')
CACHE_PATH = CACHE_PATH_ORIGINAL
ORIGINAL_IMAGE_FILE_NAME_NO_EXTENSION = 'original_image'
RESULT_IMAGE_FILE_NAME_NO_EXTENSION = 'result_image'
DETECTIONS_RAW_DATA_FILE_NAME = 'detections_data_raw.npy'
DETECTIONS_CLEANED_DATA_FILE_NAME = 'detections_data.json'
DETECTION_META_DATA_FILE_NAME = 'metadata.json'

BOXES_COUNT_DEFAULT = 1
SCORE_THRESHOLD_DEFAULT = 0.2