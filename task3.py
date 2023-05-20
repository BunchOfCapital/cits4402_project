from task2 import *
import numpy as np
# To implement Task 3, which involves finding the positions of the targets and cameras in the rig using the measured points, you can follow these steps:

# Use the points measured in the previous steps to estimate the relative pose of each target and camera. You can use existing PnP solvers like estworldpose in MATLAB or solvePnP in OpenCV for this task. These functions take the 3D coordinates of the target points and their corresponding 2D projections in the images to estimate the camera pose.
def estimate_camera_pose(target_points_3d, target_points_2d):
    # Convert target_points_3d and target_points_2d to numpy arrays
    target_points = np.array(target_points_3d)
    image_points = np.array(target_points_2d)

    # Construct camera matrix 
    # TODO: find values in json file
    camera_matrix = np.array([[fx, 0, cx],
                              [0, fy, cy],
                              [0, 0, 1]])
    # ENDTODO

    # Assume zero distortion coefficients
    distortion_coefficients = np.zero((4,1))
    
    # Use PnP solver (e.g., solvePnP in OpenCV) to estimate camera pose
    retval, rvec, tvec = cv2.solvePnP(target_points, image_points, camera_matrix, distortion_coefficients)
    
    # Returns camera pose (rotation and translation)
    return rvec, tvec


# First, a reference camera is selected, which local reference frame becomes the local 
# reference frame for the holographic communication rig.
def select_reference_camera(camera_poses):
    reference_camera = camera_poses[0]
    return reference_camera

# Then, all targets detected in that camera are aligned into the
# holographic communication rig by using PNP based on the local coordinates of each target, and
# inverting the solution to get the pose of the target in the camera frame. 
def align_targets_to_rig(reference_camera, target_points):
    # Align target points detected in the reference camera to the rig
    # using PnP solver and the reference camera's pose

    rig_points_3d = []
    rig_points_2d = []

    for target_point in target_points:
        # Convert target_point to local coordinates
        local_coords = ...

        # Estimate target pose in the reference camera frame using PnP solver
        target_pose = estimate_camera_pose([local_coords], [target_point])

        # Invert the target pose to obtain the pose of the target in the camera frame
        target_in_camera_pose = np.array([np.linalg.inv(target_pose[0]), np.linalg.inv(target_pose[1])])

        # Append target points and their projections to the rig
        rig_points_3d.append(target_in_camera_pose)
        rig_points_2d.append(target_point)

    return rig_points_3d, rig_points_2d

# Then, images with projection of the currently solved target
# can be aligned on the rig frame of reference using PNP
def align_images_to_rig(reference_camera, target_points):
    # Align images to the rig using PnP solver and the reference camera's pose

    rig_points_3d = []
    rig_points_2d = []

    for target_point in target_points:
        # Convert target_point to local coordinates
        local_coords = ...

        # Estimate target pose in the reference camera frame using PnP solver
        target_pose = estimate_camera_pose([local_coords], [target_point])

        # Invert the target pose to obtain the pose of the target in the camera frame
        target_in_camera_pose = np.array([np.linalg.inv(target_pose[0]), np.linalg.inv(target_pose[1])])

        # Append target points and their projections to the rig
        rig_points_3d.append(target_in_camera_pose)
        rig_points_2d.append(target_point)

    return rig_points_3d, rig_points_2d

# The final solution is then obtained by using a global bundle adjustment solver derived 
# from the one that was developed for the work on topographic mapping by Cledat et al., 2020
def bundle_adjustment(camera_poses, target_poses, rig_pose):
    return camera_poses, target_poses, rig_pose

