import os
import pytest
import shutil

import numpy as np

from backend.visualisation_utils import visualize_image_with_keypoints, numpy_array_to_img
from backend.tensor_utils import convert_image_to_tensor
from backend.file_handler import create_folders

dir_path = os.path.dirname(os.path.realpath(__file__))
temp_path = os.path.join(dir_path, "temp")

os.environ['CONFIG_NAME'] = 'unit_test'


class TestVisualisations:
    @pytest.fixture
    def setup_and_teardown(self):
        self._setup()
        yield
        self._teardown()

    def _setup(self):
        print("\nsetting up")
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        create_folders()

    def _teardown(self):
        print("tearing down")

    def test_keypoint_visualization_on_single_image(self, setup_and_teardown):
        filename = "test_image.png"
        filepath = os.path.join(dir_path, "fixtures", filename)

        image_tensor = convert_image_to_tensor(filepath)

        # Keypoint array created with MoveNet model tflite_movenet_lightning_f16
        keypoints_with_scores = np.array(
            [[[[0.33217365, 0.5726658, 0.4494615],
              [0.31439158, 0.5772979, 0.6838645],
              [0.31208035, 0.5512204, 0.5983896],
              [0.31852993, 0.5547738, 0.38557354],
              [0.31637684, 0.4976929, 0.6155093],
              [0.41426465, 0.549188, 0.5268066],
              [0.4061126, 0.43749478, 0.67215455],
              [0.50775003, 0.6594318, 0.6601538],
              [0.5105499, 0.52640384, 0.81059706],
              [0.42197028, 0.64408493, 0.5783226],
              [0.4168474, 0.6145565, 0.6359308],
              [0.6082694, 0.40747428, 0.6510321],
              [0.60762316, 0.31438535, 0.7702483],
              [0.64879423, 0.5663375, 0.6455827],
              [0.6788212, 0.43183458, 0.61457497],
              [0.8356959, 0.515922, 0.533018],
              [0.8902436, 0.3593879, 0.77834857]]]]
        )

        image_array = visualize_image_with_keypoints(
            image_tensor, keypoints_with_scores)

        img_byte_array = numpy_array_to_img(image_array)

        assert 814000 < len(img_byte_array) < 815000
