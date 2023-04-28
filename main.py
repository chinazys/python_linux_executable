import cv2
import time
import sys

from opencv.image_rotation.image_rotation import ImageRotationThread
from opencv.put_text.put_text import put_text
from opencv.window.window import OpenCVWindow
from shared.uint8_rgb_matrix import SharedUINT8RGBMatrix

TEST_IMAGE_PATH = 'images/test_image.jpg'
THREAD_TIMEOUT = 0.2
DELAY_BETWEEN_FRAMES_MS = 20

if __name__ == '__main__':
    test_image = cv2.imread(TEST_IMAGE_PATH)
    shared_image = SharedUINT8RGBMatrix(array=test_image)
    window = OpenCVWindow(frame=shared_image)

    rotated_image = test_image.copy()
    while True:
        for angle in range(1, 360):
            if not window.is_active():
                sys.exit()

            image_rotation_thread = ImageRotationThread(test_image, angle)
            image_rotation_thread.start()
            
            put_text(rotated_image, str(angle - 1))

            image_rotation_thread.join(timeout=THREAD_TIMEOUT)

            if image_rotation_thread.is_alive():
                raise Exception("Thread timeout")
        
            shared_image.set_array(rotated_image)

            rotated_image = image_rotation_thread.image.copy()
        
            OpenCVWindow.wait_between_frames()