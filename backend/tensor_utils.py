import os
import tensorflow as tf


def convert_image_to_tensor(image_path: str):
    """
    Converts JPG or PNG image file to TensorFlow tensor.

    Args:
        image_path (str): Absolute path to image

    Returns:
        image_tensor (tensor): Tensorflow tensor [x_res, y_res, 3]
    """

    image = tf.io.read_file(image_path)

    print(f"Converting image '{os.path.basename(image_path)}' to tensor")

    if image_path.lower().endswith((".jpeg", ".jpg")):
        image_tensor = tf.image.decode_jpeg(image, channels=3)
    elif image_path.lower().endswith(".png"):
        image_tensor = tf.image.decode_png(image, channels=3)
    else:
        raise Exception("Unsupported file type")

    print("- Done")

    return image_tensor


def resize_image_tensor(image_tensor, input_size):
    """
    Resizes image tensor to match required input size.
      Adds black bars to image to create a square output.

    Args:
        image_tensor (tensor): Tensorflow tensor.
        input_size (int, tuple): Size what the resized tensor should be.

    Returns:
        resized_image_tensor (tensor): TensorFlow tensor [1, input_size, input_size, 3]
    """
    print(f"Resizing tensor")

    resized_image_tensor = tf.expand_dims(image_tensor, axis=0)
    if isinstance(input_size, int):
        resized_image_tensor = tf.image.resize_with_pad(
            resized_image_tensor, input_size, input_size)
    elif isinstance(input_size, tuple):
        resized_image_tensor = tf.image.resize_with_pad(
            resized_image_tensor, input_size[0], input_size[1])
    else:
        raise Exception(f"input_size is not supported data type")

    print("- Done")

    return resized_image_tensor
