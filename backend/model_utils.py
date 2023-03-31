import os
import requests
import cv2

import numpy as np
import mediapipe as mp
import tensorflow as tf
import tensorflow_hub as hub

dir_path = os.path.dirname(os.path.realpath(__file__))
MODELS_DIR = os.path.join(dir_path, "models")

SUPPORTED_MODELS = [
    "blazepose",
    "tflite_movenet_lightning_f16",
    "tflite_movenet_thunder_f16",
    "tflite_movenet_lightning_int8",
    "tflite_movenet_thunder_int8",
    "movenet_lightning",
    "movenet_thunder"
]


def model_downloader(
    url: str,
    model_name: str,
    model_download_folder: str = MODELS_DIR
):
    """
    Function for downloading models

    Args:
        url (str): Url from which to download
        model_name (str): Model name including the file extension.
        model_download_dir (str): Default MODELS_DIR. Directory to which download.

    Returns:
        filepath (str): Path of downloaded model.

    """
    filepath = os.path.join(model_download_folder, model_name)

    if not os.path.isfile(filepath):
        print(f"- Downloading model '{model_name}' from {url}")

        if not os.path.exists(model_download_folder):
            os.makedirs(model_download_folder)

        with open(filepath, "wb") as f:
            f.write(requests.get(url, timeout=30).content)
    else:
        print(f"- Model '{model_name}' found.")

    return filepath


def select_model(model_name: str):
    print(f"Selecting keypoint detector for model '{model_name}'.")

    if model_name not in SUPPORTED_MODELS:
        raise Exception(f"- Model name '{model_name}' not supported")

    if "movenet" in model_name:
        keypoint_detector, input_size = select_movenet_model(model_name)
    elif "blazepose" in model_name:
        keypoint_detector, input_size = select_blazepose_model()

    return keypoint_detector, input_size


def select_movenet_model(model_name: str):
    """
    Function by TensorFlow team. Modifications by me.

    Selects and downloads the model if not found on local disk.
      Chooses correct input_size and returns suitable keypoint_detector function.

    Args:
        model_name (str): Name of MoveNet model.

    Returns:
        keypoint_detector (function): Function which returns keypoints_with_scores 
          from input image tensor
        input_size (int): Input tensor size for the model.
    """

    if "tflite" in model_name:
        if "movenet_lightning_f16" in model_name:
            url = "https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/float16/4?lite-format=tflite"
            input_size = 192
        elif "movenet_thunder_f16" in model_name:
            url = "https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/float16/4?lite-format=tflite"
            input_size = 256
        elif "movenet_lightning_int8" in model_name:
            url = "https://tfhub.dev/google/lite-model/movenet/singlepose/lightning/tflite/int8/4?lite-format=tflite"
            input_size = 192
        elif "movenet_thunder_int8" in model_name:
            url = "https://tfhub.dev/google/lite-model/movenet/singlepose/thunder/tflite/int8/4?lite-format=tflite"
            input_size = 256
        else:
            raise ValueError("Unsupported model name: %s" % model_name)

        model_filename = f"{model_name}.tflite"
        model_path = model_downloader(url, model_filename)

        # Initialize the TFLite interpreter
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()

        def keypoint_detector(input_image):
            """Runs detection on an input image.

            Args:
              input_image: A [1, height, width, 3] tensor represents the input image
                pixels. Note that the height/width should already be resized and match the
                expected input resolution of the model before passing into this function.

            Returns:
              keypoints_with_scores [1, 1, 17, 3] (float numpy array): representing the predicted keypoint
                coordinates and scores.
            """
            print(f"Estimating pose")

            # TF Lite format expects tensor type of uint8.
            input_image = tf.cast(input_image, dtype=tf.uint8)
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            interpreter.set_tensor(
                input_details[0]['index'], input_image.numpy())
            # Invoke inference.
            interpreter.invoke()
            # Get the model prediction.
            keypoints_with_scores = interpreter.get_tensor(
                output_details[0]['index'])

            print("- Done")

            return keypoints_with_scores

    else:
        if "movenet_lightning" in model_name:
            module = hub.load(
                "https://tfhub.dev/google/movenet/singlepose/lightning/4")
            input_size = 192
        elif "movenet_thunder" in model_name:
            module = hub.load(
                "https://tfhub.dev/google/movenet/singlepose/thunder/4")
            input_size = 256
        else:
            raise ValueError("Unsupported model name: %s" % model_name)

        def keypoint_detector(input_image):
            """Runs detection on an input image.

            Args:
              input_image: A [1, height, width, 3] tensor represents the input image
                pixels. Note that the height/width should already be resized and match the
                expected input resolution of the model before passing into this function.

            Returns:
              keypoints_with_scores [1, 1, 17, 3] (float numpy array): representing the predicted keypoint
                coordinates and scores.
            """
            model = module.signatures['serving_default']

            # SavedModel format expects tensor type of int32.
            input_image = tf.cast(input_image, dtype=tf.int32)
            # Run model inference.
            outputs = model(input_image)
            # Output is a [1, 1, 17, 3] tensor.
            keypoints_with_scores = outputs['output_0'].numpy()
            return keypoints_with_scores

    return keypoint_detector, input_size


def select_blazepose_model():
    """
    Selects Blazepose model.

    Returns:
        keypoint_detector (function): Function which returns keypoints_with_scores 
          from input image.
    """

    def keypoint_detector(image_path):
        """
        Detects keypoints from input image
        Converting image to tensor before inference not required with BlazePose.
        Image will be converted to square shape before inference.

        Args:
            image_path (str): Absolute path to image

        Returns:
            results (Mediapipe pose process): Object containing the keypoints 
              and scores for 33 keypoints.
        """

        def split(number, k):
            number = int(number)
            d, r = divmod(number, k)
            return [d+1]*r + [d]*(k-r)

        def add_padding(image):
            height = image.shape[0]
            width = image.shape[1]

            if height >= width:
                padding = height - width
                left, right = split(padding, 2)
                top, bottom = 0, 0
            else:
                padding = width - height
                top, bottom = split(padding, 2)
                left, right = 0, 0

            image = cv2.copyMakeBorder(
                image, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])

            return image

        mp_pose = mp.solutions.pose

        with mp_pose.Pose(
                static_image_mode=True,
                model_complexity=2,
                enable_segmentation=True,
                min_detection_confidence=0.5) as pose:
            print(f"Estimating pose")
            image = cv2.imread(image_path)
            image = add_padding(image)

            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            print("- Done")

        return results

    return keypoint_detector, None


MOVENET_TO_BLAZEPOSE_DICT = {
    # Keys: MoveNet - Values: BlazePose
    0: 0,     # 'nose'
    1: 2,     # 'left_eye'
    2: 5,     # 'right_eye'
    3: 7,     # 'left_ear'
    4: 8,     # 'right_ear'
    5: 11,    # 'left_shoulder'
    6: 12,    # 'right_shoulder'
    7: 13,    # 'left_elbow'
    8: 14,    # 'right_elbow'
    9: 15,    # 'left_wrist'
    10: 16,   # 'right_wrist'
    11: 23,   # 'left_hip'
    12: 24,   # 'right_hip'
    13: 25,   # 'left_knee'
    14: 26,   # 'right_knee'
    15: 27,   # 'left_ankle'
    16: 28    # 'right_ankle'
}


def convert_blazepose_results_to_movenet_keypoints_with_scores(results):
    """
    Convert BlazePose results to similar format as MoveNet's output keypoints_with_scores.

    Args:
        results (Mediapipe pose process): Object containing the keypoints 
          and scores for 33 keypoints.

    Returns:
        keypoints_with_scores [1, 1, 17, 3] (float numpy array): representing the predicted keypoint
          coordinates and scores.
    """
    print("Converting results")
    converted = []

    for key, value in MOVENET_TO_BLAZEPOSE_DICT.items():
        # y = 0 top, 1 bottom
        # x = 0 left, 1 right

        if results and results.pose_landmarks:
            y = results.pose_landmarks.landmark[value].y
            x = results.pose_landmarks.landmark[value].x
            confidence = results.pose_landmarks.landmark[value].visibility
        else:
            y, x, confidence = -1.0, -1.0, 0.0

        converted.append([y, x, confidence])

    keypoints_with_scores = np.array([[converted]])

    print(f"- Done")

    return keypoints_with_scores
