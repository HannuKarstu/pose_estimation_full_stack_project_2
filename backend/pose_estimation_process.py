from backend.model_utils import select_model, convert_blazepose_results_to_movenet_keypoints_with_scores
from backend.tensor_utils import convert_image_to_tensor, resize_image_tensor


def estimate_pose(filepath, model_name):
    image_tensor = convert_image_to_tensor(filepath)

    keypoint_detector, input_size = select_model(
        model_name)

    if "movenet" in model_name:
        resized_image_tensor = resize_image_tensor(
            image_tensor, input_size)
        keypoints_with_scores = keypoint_detector(resized_image_tensor)
    elif "blazepose" in model_name:
        blazepose_results = keypoint_detector(filepath)
        keypoints_with_scores = convert_blazepose_results_to_movenet_keypoints_with_scores(
            blazepose_results)

    return keypoints_with_scores, image_tensor
