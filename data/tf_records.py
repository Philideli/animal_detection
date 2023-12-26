import tensorflow as tf
import os
import io
from object_detection.utils import dataset_util
from PIL import Image
import traceback


class TFRecordsGenerator:
    # the format of provided data to generate examples should be:
    # {
    #   filename: "x.png",
    #   objects: [
    #       {
    #           'label_id': 27,
    #           'label_name': 'RFIDSCANNER',
    #           'x': 220.0,
    #           'y': 29.0,
    #           'width': 117.0,
    #           'height': 90.0
    #       },
    #       {...}
    #   ]
    # }
    IMAGE_FILENAME = 'filename'
    IMAGE_OBJECTS = 'objects'
    IMAGE_OBJ_LABEL_ID = 'label_id'
    IMAGE_OBJ_LABEL_NAME = 'label_name'
    IMAGE_OBJ_X = 'x'
    IMAGE_OBJ_Y = 'y'
    IMAGE_OBJ_WIDTH = 'width'
    IMAGE_OBJ_HEIGHT = 'height'

    def __init__(self, images_path=None):
        self.images_path = os.path.abspath(images_path) if images_path else None
        self.tf_examples = []

    def add_tf_example(self, image_data, use_images_path=True):
        image_path = image_data[TFRecordsGenerator.IMAGE_FILENAME]
        if use_images_path:
            image_path = os.path.abspath(os.path.join(self.images_path, image_path))
        objects = image_data[TFRecordsGenerator.IMAGE_OBJECTS]

        # noinspection PyBroadException
        try:
            with tf.io.gfile.GFile(image_path, 'rb') as image_file:
                encoded_image = image_file.read()
            encoded_image_io = io.BytesIO(encoded_image)
            image = Image.open(encoded_image_io)
        except Exception:
            traceback.print_exc()
            return False

        img_width, img_height = image.size

        filename, extension = os.path.splitext(image_path)
        filename, extension = filename.encode('UTF-8'), extension.encode('UTF-8')

        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []
        classes_text = []
        classes = []

        for obj in objects:
            xmin = obj[TFRecordsGenerator.IMAGE_OBJ_X]
            ymin = obj[TFRecordsGenerator.IMAGE_OBJ_Y]
            obj_width = obj[TFRecordsGenerator.IMAGE_OBJ_WIDTH]
            obj_height = obj[TFRecordsGenerator.IMAGE_OBJ_HEIGHT]
            class_text = obj[TFRecordsGenerator.IMAGE_OBJ_LABEL_NAME]
            class_id = obj[TFRecordsGenerator.IMAGE_OBJ_LABEL_ID]
            xmins += [xmin / img_width]
            ymins += [ymin / img_height]
            xmaxs += [(xmin + obj_width) / img_width]
            ymaxs += [(ymin + obj_height) / img_height]
            classes_text += [class_text.encode('UTF-8')]
            classes += [class_id]

        tf_example = tf.train.Example(features=tf.train.Features(feature={
            'image/height': dataset_util.int64_feature(img_height),
            'image/width': dataset_util.int64_feature(img_width),
            'image/filename': dataset_util.bytes_feature(filename),
            'image/source_id': dataset_util.bytes_feature(filename),
            'image/encoded': dataset_util.bytes_feature(encoded_image),
            'image/format': dataset_util.bytes_feature(extension),
            'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
            'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes),
        }))
        self.tf_examples += [tf_example]
        return True

    def add_tf_examples(self, images_data, use_images_path=True):
        for img in images_data:
            # make shallow copies!
            image_data = {}
            filename = img[TFRecordsGenerator.IMAGE_FILENAME]
            if use_images_path:
                # images_paths contain relative paths to images so that
                # the absolute path to images is self.images_path/images_paths[i]
                filename = os.path.abspath(os.path.join(self.images_path, filename))
            image_data[TFRecordsGenerator.IMAGE_FILENAME] = filename
            objects = img[TFRecordsGenerator.IMAGE_OBJECTS]
            image_data[TFRecordsGenerator.IMAGE_OBJECTS] = objects
            if not self.add_tf_example(image_data, False):
                return False
        return True

    def clear_tf_examples(self):
        self.tf_examples = []

    def write_records(self, write_path):
        try:
            dirname = os.path.dirname(write_path)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            with tf.io.TFRecordWriter(write_path) as writer:
                for example in self.tf_examples:
                    writer.write(example.SerializeToString())
        except (IOError, ValueError, OSError):
            traceback.print_exc()
            return False
        else:
            return True

