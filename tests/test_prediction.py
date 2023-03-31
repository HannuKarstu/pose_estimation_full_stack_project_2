import os
import pytest
import time

import numpy as np
import tensorflow as tf

from backend.pose_estimation_process import estimate_pose

dir_path = os.path.dirname(os.path.realpath(__file__))


class TestPoseEstimationProcess:
    def test_pose_estimation_process_with_single_image(self):
        filename = "test_image.png"
        filepath = os.path.join(dir_path, "fixtures", filename)

        # Tests each of the models
        model_names = [
            "blazepose",
            "tflite_movenet_lightning_f16",
            "tflite_movenet_thunder_f16",
            "tflite_movenet_lightning_int8",
            "tflite_movenet_thunder_int8",
            "movenet_lightning",
            "movenet_thunder"
        ]

        for model_name in model_names:
            print(f"Testing model {model_name}")
            start = time.time()

            keypoints_with_scores, image_tensor = estimate_pose(
                filepath, model_name)

            assert isinstance(keypoints_with_scores, np.ndarray)
            assert isinstance(image_tensor, tf.Tensor)

            # 17 keypoints
            assert len(keypoints_with_scores[0][0]) == 17

            # Y coordinate, X coordinate, confidence score
            assert len(keypoints_with_scores[0][0][0]) == 3
            print(f"- Done in {round(time.time() - start, 2)}")
