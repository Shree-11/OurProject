import cv2
import numpy as np

def preprocess_image(image_file):
    # Check if the file object has a read() method
    if hasattr(image_file, 'read'):
        image = np.fromstring(image_file.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    else:
        # Load the image using OpenCV
        image = cv2.imread(image_file)

    # Resize the image to the expected input shape of the model
    image = cv2.resize(image, (224, 224))

    # Scale the pixel values to the range [0, 1]
    image = image.astype('float32') / 255.0

    # Add an extra dimension to represent the batch size (required by Keras)
    image = np.expand_dims(image, axis=0)

    return image
