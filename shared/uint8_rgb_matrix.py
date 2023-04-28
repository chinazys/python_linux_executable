import random
import string
import numpy as np
from multiprocessing import shared_memory, Lock

class SharedUINT8RGBMatrix:
    DTYPE = np.uint8
    COLOR_CHANNELS_DEPTH = 3

    def _generate_id(length=8) -> str:
        return ''.join(random.choice(string.ascii_letters) for i in range(length))
        
    def __init__(self, array: np.ndarray = None, shm_id: str = None, dimensions: list = None, lock: Lock = None) -> None:
        create_array = not array is None
        load_array = not shm_id is None and not dimensions is None and not lock is None
        assert create_array ^ load_array, "Invalid SharedUINT8RGBMatrix constructor"

        if create_array:
            self.shm_id = SharedUINT8RGBMatrix._generate_id()
            self.shm = shared_memory.SharedMemory(name=self.shm_id, create=True, size=array.nbytes)
            self.shape = array.shape
            self.lock = Lock()
        if load_array:
            self.shm_id = shm_id
            self.shm = shared_memory.SharedMemory(name=self.shm_id)
            (width, height) = dimensions
            self.shape = (height, width, self.COLOR_CHANNELS_DEPTH)
            self.lock = lock
        
        self.array = np.ndarray(shape=self.shape, dtype=self.DTYPE, buffer=self.shm.buf)
        
        if create_array:
            self.array[...] = array
    
    def set_array(self, array) -> None:
        self.lock.acquire()
        self.array[...] = array
        self.lock.release()

    def get_array(self) -> np.ndarray:
        self.lock.acquire()
        array = self.array[...]
        self.lock.release()

        return array