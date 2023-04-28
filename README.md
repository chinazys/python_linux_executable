# Python Executable for Linux

## Objective 
Create a tool for converting of a Python application into a standalone Linux (Raspbian) executable, allowing to distribute the code and run it without installation of any additional dependencies. 

## Test project

### Overview
The recommened test project is available within this repository. It is simple yet representative example of Python application, that can be used to verify the tool's ability to correctly bundle all required packages and dependencies into a standalone executable.

### Demo
The single window app displays a continiously rotating icon with the rotation degrees counter in the center:
![](demo/demo.gif)

[main.py](main.py) is the entry application entry point of the application. To exexute the script, run
```console
pi/test/project/location:~$ python3 main.py
```
### How does it work
1. Read the image from [image/test_image.jpg](images/test_image.jpg) and save it as a NumPy array
2. Copy the previously created NumPy array and write it into [multiprocessing.shared_memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html), so that its state could be shared among processes. See [shared/uint8_rgb_matrix.py](shared/uint8_rgb_matrix.py) for implementation.
3. Start a separate process, that uses [OpenCV window](opencv/window/window.py) to display the image from the shared NumPy array, created at step 2.
4. In the main process:
    
    0. Exit if ESC key was pressed 
    1. [Rotate image](opencv/image_rotation/image_rotation.py) at the current angle in a separate thread
    2. Simultaneously, [put text](opencv/put_text/put_text.py) with the current angle counter in the center of the previously rotated image.
    3. Save the image obtained at step 4.2 into the shared Numpy array, created at step 2, so that it can be displayed with OpenCV Window.

## Notes
The straight-forward way of creating the binary with [pyinstaller](https://pyinstaller.org/en/stable/) is not acceptable due to the known issues with [multiprocessing](https://docs.python.org/3/library/multiprocessing.html), see [#4110](https://github.com/pyinstaller/pyinstaller/issues/4110), [#4159](https://github.com/pyinstaller/pyinstaller/issues/4159), [#4190](https://github.com/pyinstaller/pyinstaller/issues/4190). 

Using of [cython](https://cython.org/)-alike packages or cython-pyinstaller combination is more preferable in terms of reverse-engineering protection. 