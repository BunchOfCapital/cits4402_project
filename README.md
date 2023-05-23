# CITS4402 Project : Automatic Calibration of a Holographic Acquisition Rig
by Joel Wildman (22984156), Jonathan Hartono (22976067), and Stefan Nio (23104714)

This project re-implements an automatic calibration procedure (developed by a UWA PhD student for a holographic acquisition rig ) and provide an intuitive interface that allows for the quick adjustment of algorithm hyperparameters and the visualization of 
results. The code offers a graphical user interface (GUI) developed using Tkinter, Python's Tk GUI Toolkit. 

## Getting started, Installation, and Running the script
Firstly, clone this repository onto your local machine.

```bash
git clone https://github.com/BunchOfCapital/cits4402_project.git
```

You have now successfully activated your virtual environment. You can now use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies (contained in 'requirements.txt' file) by running the following command:

```bash
python -m pip install -r requirements.txt
```

You can now start the 'main.py' script using Python:

```bash
python main.py
```

A GUI window will appear, allowing you to interact with the program

## Important Notes
- The project assumes that the input images are in the BGR color space.
- The main.py script depends on the calibrate.py, task2.py, and task3.py scripts for various image processing tasks.
- Make sure all the required dependencies are installed before running the project.

## Functionality
### Load Image
- Click on the "Load Image" button to choose an image file from your local system.
- The selected image will be displayed in the GUI.
### Task 1: Object Detection
- After loading an image, click on the "Task 1" button to perform a rough candidate targets detection.
The image will be processed to detect objects based on their color.
Detected objects will be highlighted with bounding boxes and labeled with numbers.
Additionally, circles will be drawn at the centroids of the detected objects.
The processed image will be displayed on the right side of the GUI.
