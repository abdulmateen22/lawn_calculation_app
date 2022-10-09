import os
import cv2
from mrcnn import visualize
import mrcnn.model as modellib
from mrcnn.config import Config

import time
import tensorflow as tf

graph = tf.get_default_graph()








COCO_MODEL_PATH="weights/mask_rcnn_coco_0004.h5"
class BalloonConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "coco"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + balloon

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9


class InferenceConfig(BalloonConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


inference_config = InferenceConfig()
MODEL_DIR = "logs/"



# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference",
                          config=inference_config,
                          model_dir=MODEL_DIR)

model.load_weights(COCO_MODEL_PATH, by_name=True)
model.keras_model._make_predict_function()
# graph = tf.get_default_graph()



print("Loading weights from ", COCO_MODEL_PATH)






out_dir = 'test_results'
try:
    os.mkdir(out_dir)
except:
    pass



def detect(image_path):
    # file =  os.path.basename(image_path)
    # original_image = cv2.imread(image_path)
    file =str(time.strftime("%Y%m%d-%H%M%S"))
    original_image = image_path
    print(image_path.shape)
    if len(image_path.shape) > 2 and image_path.shape[2] == 4:
        # convert the image from RGBA2RGB
        original_image = cv2.cvtColor(image_path, cv2.COLOR_BGRA2BGR)
    results = model.detect([original_image], verbose=1)
    r = results[0]
    res_image = visualize.display_instances(original_image, r['rois'], r['masks'], r['class_ids'],['grass'], r['scores'], figsize=(8, 8))
    cv2.imwrite(f'{out_dir}/{file}.jpg', res_image)
    if  res_image is not None:
        return True
    else:
        return False


# detect('test/200.png')