import os

from animal_detection.app.backend.detection.constants import CACHE_PATH

def get_full_path(filename):
    return os.path.join(CACHE_PATH, filename)


def remove_file(filename):
    path = get_full_path(filename)
    if os.path.exists(path):
        os.remove(path)
        
        
def write_bytes(filename, file):
    path = get_full_path(filename)
    with open(path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)