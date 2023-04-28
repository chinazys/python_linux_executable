import cv2
import numpy as np
from threading import Thread

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
FONT_THICKNESS = 2
TEXT_COLOR = (0, 255, 0)

def put_text(image: np.ndarray, text: str) -> None:
    (image_height, image_width, image_depth) = image.shape
    (text_width, text_height) = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICKNESS)[0]

    textX = (image_width - text_width) // 2
    textY = (image_height + text_height) // 2

    cv2.putText(image, text, (textX, textY), FONT, FONT_SCALE, TEXT_COLOR, FONT_THICKNESS)