import numpy as np

from animal_detection.app.backend.detection.serialization import numpy_arrays_to_lists
from animal_detection.app.backend.data.oxford_dataset import get_breeds_data


def raw_detections_to_clean_detections(data, boxes_count, score_threshold, image_height, image_width):
    indices = np.argsort(data['detection_scores'])[::-1]
    indices_good = indices[data['detection_scores'] > score_threshold]
    indices_good = indices_good[:boxes_count]
    scores = data['detection_scores'][indices_good]
    classes = data['detection_classes'][indices_good]
    boxes = data['detection_boxes'][indices_good]
    zipped_data = zip(scores, classes, boxes)
    data_clean = [get_object_as_dict(score, cl, box, image_height, image_width) for score, cl, box in zipped_data]
    return data_clean
    
def get_class_info_series(class_id):
    breeds_df = get_breeds_data()
    return breeds_df[breeds_df['class_id'] == class_id].iloc[0]
    
def class_id_to_label(class_id):
    # maybe replace with functionality from data/processing
    return get_class_info_series(class_id)['class_label']
    
    
def class_id_to_species(class_id):
    # maybe replace with functionality from data/processing
    return get_class_info_series(class_id)['species_label']


def get_object_as_dict(score, cl, box, image_height, image_width):
    return {
        'score': score,
        'class': class_id_to_label(cl),
        'species': class_id_to_species(cl),
        'coordinates': {
            'start': {
                'x': box[1] * image_width,
                'y': box[0] * image_height
            },
            'end': {
                'x': box[3] * image_width,
                'y': box[2] * image_height
            }
        }
    }