import cv2
import numpy as np
from threading import Thread

def rotate_image(image: np.ndarray, angle: int) -> np.ndarray:
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rotation_matrix = cv2.getRotationMatrix2D(image_center, angle, 1.0)

    return cv2.warpAffine(image, rotation_matrix, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))

class ImageRotationThread(Thread):
    def __init__(self, image: np.ndarray, angle: int) -> None:
        Thread.__init__(self)
        self.image = image
        self.angle = angle

    def run(self) -> None:
        self.image = rotate_image(self.image, self.angle)