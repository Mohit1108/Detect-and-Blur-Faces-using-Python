# Welcome to My Channel M Tech-G
import cv2
import numpy as np
from os.path import dirname, join

prototxt_path = join(dirname(__file__), "deploy.prototxt")
model_path = join(dirname(__file__), "res10_300x300_ssd_iter_140000_fp16.caffemodel")
# load Caffe model
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# read the desired image
image = cv2.imread("1.jpg")
# get width and height of the image
h, w = image.shape[:2]
# NOTE: gaussian blur kernel size depends on width and height of original image
kernel_width = (w // 7) | 1
kernel_height = (h // 7) | 1
# preprocess the image: resize and performs mean subtraction
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
# set the image into the input of the neural network
model.setInput(blob)
# perform inference and get the result
output = np.squeeze(model.forward())

for i in range(0, output.shape[0]):
    confidence = output[i, 2]
    # get the confidence
    # if confidence is above 40%, then blur the bounding box (face)
    if confidence > 0.4:
        # get the surrounding box Cordinates and upscale them to original image
        box = output[i, 3:7] * np.array([w, h, w, h])
        # convert to integers
        start_x, start_y, end_x, end_y = box.astype(int)
        # get the face image
        face = image[start_y: end_y, start_x: end_x]
        # apply gaussian blur to this face
        face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
        # put the blurred face into the original image
        image[start_y: end_y, start_x: end_x] = face
        cv2.imwrite('blurred-face-Image.jpg', image)
