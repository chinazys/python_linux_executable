import cv2
import sys
import time
from multiprocessing import Process, Lock, Value

from shared.uint8_rgb_matrix import SharedUINT8RGBMatrix

class OpenCVWindow:
    WINDOW_NAME = 'window'
    DELAY_BETWEEN_FRAMES_MS = 20

    def is_active(self) -> bool:
        return self.window_is_active.value
    
    def wait_between_frames() -> None:
        time.sleep(OpenCVWindow.DELAY_BETWEEN_FRAMES_MS / 1e3)

    def __init__(self, frame: SharedUINT8RGBMatrix) -> None:
        (frame_height, frame_width, frame_depth) = frame.shape
        self.window_is_active = Value('b', True)

        window_refresh_process = Process(target=OpenCVWindow._window_refresh_func, args=(frame.shm_id, frame_width, frame_height, frame.lock, self.window_is_active,))
        window_refresh_process.start()

    def _window_refresh_func(frame_shm_id: str, frame_width: int, frame_height: int, frame_lock: Lock, window_is_active: Value) -> None:
        frame = SharedUINT8RGBMatrix(shm_id=frame_shm_id, dimensions=(frame_width, frame_height), lock=frame_lock)
        
        while True:
            cv2.imshow(OpenCVWindow.WINDOW_NAME, frame.get_array())
            
            key = cv2.waitKey(1) & 0xff

            if key == 27: # escape
                window_is_active.value = False
                cv2.destroyAllWindows()
                sys.exit()
            
            OpenCVWindow.wait_between_frames()