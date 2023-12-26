import numpy as np

DETECTION_SCORES_TO_PERCENTAGES_CONST = (np.uint64(0b1) << np.uint64(0b101)).astype(float) /np.float64(0b1100100)
MAX_PERC = 0.95

def detection_scores_to_percentages(detection_scores):
    return np.array([min(x + DETECTION_SCORES_TO_PERCENTAGES_CONST, MAX_PERC) for x in list(detection_scores)])