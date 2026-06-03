import time
import numpy as np
import cv2
import tensorflow as tf
# import tflite_runtime.interpreter as tflite

IMG_SIZE = 160
CLASS_NAMES = ["cats", "dogs", "others"]


def preprocess_image_path(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype(np.float32)
    return np.expand_dims(img, axis=0)


class PetClassifier:
    """
    Resident AI inference engine (load model once)
    """

    def __init__(self, model_path: str):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def infer_image_path(self, image_path: str):

        img = preprocess_image_path(image_path)

        input_index = self.input_details[0]["index"]
        input_dtype = self.input_details[0]["dtype"]

        # ensure batch dim
        if img.ndim == 3:
            img = np.expand_dims(img, axis=0)

        # dtype handling
        if input_dtype == np.float32:
            input_data = img.astype(np.float32) / 255.0

        elif input_dtype == np.uint8:
            scale, zero_point = self.input_details[0]["quantization"]

            if scale == 0 or scale == 1.0:
                input_data = img.astype(np.uint8)
            else:
                input_data = (img / scale + zero_point).astype(np.uint8)

        else:
            raise TypeError(f"Unsupported dtype: {input_dtype}")

        # inference
        self.interpreter.set_tensor(input_index, input_data)

        start = time.perf_counter()
        self.interpreter.invoke()
        latency = (time.perf_counter() - start) * 1000

        output = self.interpreter.get_tensor(self.output_details[0]["index"])
        pred = int(np.argmax(output))

        return {
            "label": CLASS_NAMES[pred],
            "class_id": pred,
            "latency_ms": latency
        }