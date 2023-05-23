# CITS4402 Project : Automatic Calibration of a Holographic Acquisition Rig
by Joel Wildman (22984156), Jonathan Hartono (22976067), and Stefan Nio (23104714)

This project re-implements an automatic calibration procedure (developed by a UWA PhD student for a holographic acquisition rig ) and provide an intuitive interface that allows for the quick adjustment of algorithm hyperparameters and the visualization of 
results. The code offers a graphical user interface (GUI) developed using Tkinter, Python's Tk GUI Toolkit. 

## Getting started, Installation, and Running the script
Firstly, clone this repository onto your local machine.

```bash
git clone https://github.com/BunchOfCapital/cits4402_project.git
```

You can now use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies (contained in 'requirements.txt' file) by running the following command:

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

### Task 1: The Rough Detection

#### Function Signature
```python
cull_by_colour(image)
```
create a segmentation mask by filtering pixels based on color thresholds.
##### Parameters
- image: The input image to be masked
##### Returns
Returns the final mask


```python
cull_by_size(candidates, min_area, max_area)
```
to remove regions that do not fall within the specified area range.
##### Parameters
- candidates: a list of region candidates
- min_area: minumum range
- max_area: maximum range
##### Returns
Returns the new region candidates as a numpy array


```python
cull_by_roundness(candidates, axis_ratio)
```
This function removes regions that are too far from being round based on their roundness ratio.
##### Parameters
- candidates: a list of region candidates
- axis_ratio: roundness ratio to be compared to
##### Returns
Returns the new region candidates as a numpy array


```python
cull_by_neighbours(candidates, ellipse_threshold)
```
This function removes regions that do not form an ellipse with neighboring regions.
##### Parameters
- candidates: a list of region candidates
- ellipse_threshold: the ellipse threshold
##### Returns
Returns the new candidates and the candidate regions as NumPy arrays

### Task 1 Flow
#### Loading and Preprocessing
- The code starts by loading an image.
- The image is then blurred using a Gaussian filter with a kernel size of (11,11).
- The blurred image is converted from BGR color space to HSV color space using cv2.cvtColor.
 
#### Segmentation and Connected Components Analysis (CCA)
- The function cull_by_colour is called to create a segmentation mask by filtering pixels based on color thresholds.
- Connected components analysis (CCA) is performed on the segmentation mask using measure.label to label connected regions.

#### Filtering and Selection
- The code specifies minimum and maximum area thresholds (min_area and max_area) to exclude accidentally labeled objects.
- The function cull_by_size is used to remove regions that do not fall within the specified area range.
- The function cull_by_roundness is used to remove regions that are not round enough based on the axis ratio.
- The function cull_by_neighbours is used to remove regions that do not form an ellipse with neighboring regions. This function also returns the final selected candidates and their respective hexagonal regions.

#### Visualization
- The code visualizes the labeled regions over the original image using color.label2rgb and plt.imshow.
- It then iterates over the selected hexagonal regions and performs the following steps:
    1. Calculates the centroid of each hexagonal region using calculate_centroid.
    2. Adds a red circle at the centroid position using mpatches.Circle.
    3. Draws rectangles around each hexagonal region using mpatches.Rectangle.
    4. Annotates each hexagon with a unique identifier using plt.annotate.

### Task 2 : Targets analysis and refinement 
The calculateHexagon(image, hexagon, top_region) function in the provided code snippet is used to calculate the positions and colors of hexagonal regions in an image. The function takes an image, a list of hexagonal regions, and a top region as input. It returns the sorted hexagonal regions and a final string representing the color pattern of the hexagons.

#### Function Signature

```python
def calculateHexagon(image, hexagon, top_region):
```

#### Parameters
- image: The input image on which the hexagonal regions are detected.
- hexagon: A list of hexagonal regions detected in the image.
- top_region: The top region among the hexagonal regions.

#### Returns
The function returns a tuple containing the sorted hexagonal regions and a final string representing the color pattern of the hexagons. If any hexagon's color cannot be determined, the function returns False and a value of 1.

#### Function Flow
1. Initialize the sorted_hexagon list with six elements, all set to the top_region.
2. Determine the deepest hexagon region by sorting the hexagon list based on the centroid's x-coordinate and selecting the last element. Assign this region to sorted_hexagon[3].
3. Determine the positions of the other hexagons based on their centroid's y-coordinate in relation to the top_region.
4. Calculate the average hue of each hexagon region by summing the hue values of all pixels within the region and dividing by the number of pixels.
5. Based on the average hue, assign a color label ('G' for green or 'R' for red) to each hexagon in the hex_string list.
6. Concatenate the color labels in hex_string to the finalString to create the final string representing the color pattern of the hexagons.
7. If any hexagon's color could not be determined (indicated by '?' in hex_string), return False and a value of 1.
8. Return the sorted hexagonal regions (sorted_hexagon) and the final string (finalString).

#### More Functions
The code snippet also includes two additional functions:

**caculate_weight(point_i, average_intensity, max_i)**
This function calculates the weight for a given intensity point based on its distance from the average intensity and the maximum intensity. It takes three parameters: point_i, average_intensity, and max_i. It returns the weight value.

**calculate_centroid(region, image)**
This function calculates the centroid (x, y coordinates) of a given region within an image. It takes two parameters: region (a region of interest) and image (the input image). The function calculates the centroid by considering the weights of intensity values within the region and returns the centroid coordinates (x_centroid, y_centroid).

### Task 3 : Cameras Alignments
This task performs a series of operations to estimate camera poses and triangulate 3D points from multiple cameras. Displays the 3D position of the targets' points and the cameras as a 3D plot.

```python
def task3(list_cameras):
```

#### Parameters
- list_cameras: a list of cameras taking the image.

#### Function Flow
1. Initializes empty lists for camera_poses, image_points, and all_world_points.
2. Sets the reference camera pose as the identity matrix and appends it to camera_poses.
3. Extracts the image points from each camera in list_cameras and appends them to image_points.
4. Iterates over the remaining cameras (from index 1):
    - Extracts the camera parameters (focal length, principal point, distortion coefficients) from the reference camera (list_cameras[0]).
    - Constructs the camera matrix and distortion coefficients matrices.
    - Calls the corresponding_hexagons function to get the corresponding image points between the reference and current cameras.
    - Uses v2.solvePnP to estimate the rotation and translation vectors (rvec and tvec) of the current camera relative to the reference camera.
    - Converts the rotation vector to a rotation matrix using cv2.Rodrigues.
    - Combines the rotation matrix and translation vector to create the relative pose matrix.
    - Computes the absolute pose by multiplying the reference camera pose with the relative pose.
    - Appends the absolute pose to camera_poses.
    - Initializes an empty list world_points to store the triangulated 3D points.
    - Iterates over the reference image points:
        - Retrieves the corresponding feature points from all cameras using image_points.
        - Performs triangulation using cv2.triangulatePoints to estimate the 3D position of the feature point.
        - Normalizes the homogeneous coordinates of the 3D point.
        - Appends the normalized 3D point to world_points.
    - Appends world_points to all_world_points.
5. Calls the plot3d function to visualize the world points and camera poses.
