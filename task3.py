from task2 import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from scipy.spatial.transform import Rotation as R
# To implement Task 3, which involves finding the positions of the targets and cameras in the rig using the measured points, you can follow these steps:

# Use the points measured in the previous steps to estimate the relative pose of each target and camera. You can use existing PnP solvers like estworldpose in MATLAB or solvePnP in OpenCV for this task. These functions take the 3D coordinates of the target points and their corresponding 2D projections in the images to estimate the camera pose.
# def estimate_camera_pose(target_points_3d, target_points_2d):
#     # Convert target_points_3d and target_points_2d to numpy arrays
#     target_points = np.array(target_points_3d)
#     image_points = np.array(target_points_2d)

#     # Construct camera matrix 
#     # TODO: find values in json file
#     camera_matrix = np.array([[fx, 0, cx],
#                               [0, fy, cy],
#                               [0, 0, 1]])
#     # ENDTODO

#     # Assume zero distortion coefficients
#     distortion_coefficients = np.zero((4,1))
    
#     # Use PnP solver (e.g., solvePnP in OpenCV) to estimate camera pose
#     retval, rvec, tvec = cv2.solvePnP(target_points, image_points, camera_matrix, distortion_coefficients)
    
#     # Returns camera pose (rotation and translation)
#     return rvec, tvec


# # First, a reference camera is selected, which local reference frame becomes the local 
# # reference frame for the holographic communication rig.
# def select_reference_camera(camera_poses):
#     reference_camera = camera_poses[0]
#     return reference_camera

# # Then, all targets detected in that camera are aligned into the
# # holographic communication rig by using PNP based on the local coordinates of each target, and
# # inverting the solution to get the pose of the target in the camera frame. 
# def align_targets_to_rig(reference_camera, target_points):
#     # Align target points detected in the reference camera to the rig
#     # using PnP solver and the reference camera's pose

#     rig_points_3d = []
#     rig_points_2d = []

#     for target_point in target_points:
#         # Convert target_point to local coordinates
#         local_coords = ...

#         # Estimate target pose in the reference camera frame using PnP solver
#         target_pose = estimate_camera_pose([local_coords], [target_point])

#         # Invert the target pose to obtain the pose of the target in the camera frame
#         target_in_camera_pose = np.array([np.linalg.inv(target_pose[0]), np.linalg.inv(target_pose[1])])

#         # Append target points and their projections to the rig
#         rig_points_3d.append(target_in_camera_pose)
#         rig_points_2d.append(target_point)

#     return rig_points_3d, rig_points_2d

# # Then, images with projection of the currently solved target
# # can be aligned on the rig frame of reference using PNP
# def align_images_to_rig(reference_camera, target_points):
#     # Align images to the rig using PnP solver and the reference camera's pose

#     rig_points_3d = []
#     rig_points_2d = []

#     for target_point in target_points:
#         # Convert target_point to local coordinates
#         local_coords = ...

#         # Estimate target pose in the reference camera frame using PnP solver
#         target_pose = estimate_camera_pose([local_coords], [target_point])

#         # Invert the target pose to obtain the pose of the target in the camera frame
#         target_in_camera_pose = np.array([np.linalg.inv(target_pose[0]), np.linalg.inv(target_pose[1])])

#         # Append target points and their projections to the rig
#         rig_points_3d.append(target_in_camera_pose)
#         rig_points_2d.append(target_point)

#     return rig_points_3d, rig_points_2d

# # The final solution is then obtained by using a global bundle adjustment solver derived 
# # from the one that was developed for the work on topographic mapping by Cledat et al., 2020
# def bundle_adjustment(camera_poses, target_poses, rig_pose):
#     return camera_poses, target_poses, rig_pose
def DLT(P1, P2, point1, point2):
 
    A = [point1[1]*P1[2,:] - P1[1,:],
         P1[0,:] - point1[0]*P1[2,:],
         point2[1]*P2[2,:] - P2[1,:],
         P2[0,:] - point2[0]*P2[2,:]
        ]
    A = np.array(A).reshape((4,4))
    #print('A: ')
    #print(A)
 
    B = A.transpose() @ A
    from scipy import linalg
    U, s, Vh = linalg.svd(B, full_matrices = False)
 
    print('Triangulated point: ')
    print(Vh[3,0:3]/Vh[3,3])
    return Vh[3,0:3]/Vh[3,3]

def task3(list_cameras):
    #list_camera[camera_id][0] =  configVals 
    #list_camera[camera_id][1] =  StringName List 
    #list_camera[camera_id][2] =  centroid of hexagon points  List 
    camera_poses = [] 
    image_points = []
    all_world_points = []
    reference_camera_pose = [np.eye(4)]
    camera_poses.append(reference_camera_pose)
    for camera_idx in range(len(list_cameras)):
        points = list_cameras[camera_idx][2]
        image_points.append(points)
    for camera_id in range(1, len(list_cameras)):
        f = list_cameras[0][0]["of"]["val"]
        cy = list_cameras[0][0]["cy"]["val"]
        cx = list_cameras[0][0]["cx"]["val"]

        k1 = list_cameras[0][0]["ok1"]["val"]
        k2 = list_cameras[0][0]["ok2"]["val"]
        k3 = list_cameras[0][0]["ok3"]["val"]
        p1 = list_cameras[0][0]["op1"]["val"]
        p2 = list_cameras[0][0]["op2"]["val"]

        ocx = list_cameras[0][0]["ocx"]["val"]
        ocy = list_cameras[0][0]["ocy"]["val"]

        f2 = list_cameras[1][0]["of"]["val"]
        cy2 = list_cameras[1][0]["cy"]["val"]
        cx2 = list_cameras[1][0]["cx"]["val"]

        k1_2 = list_cameras[1][0]["ok1"]["val"]
        k2_2 = list_cameras[1][0]["ok2"]["val"]
        k3_2 = list_cameras[1][0]["ok3"]["val"]
        p1_2 = list_cameras[1][0]["op1"]["val"]
        p2_2 = list_cameras[1][0]["op2"]["val"]

        ocx2 = list_cameras[1][0]["ocx"]["val"]
        ocy2 = list_cameras[1][0]["ocy"]["val"]


        #a rough manual estimation of the camera intrinsic matrix, without accounting for the distortion.
        #we don't know how to get the actual camera matrix :(

        camera_matrix = np.array([[f, 0, ocx], [0, f, ocy], [0, 0, 1]], dtype=np.float32)
        camera2_matrix =   np.array([[f2, 0, ocx2], [0, f2, ocy2], [0, 0, 1]], dtype=np.float32)
        dist_coeffs = np.array([k1, k2, p1, p2, k3], dtype=np.float32) 
        reference_image_points, current_image_points = corresponding_hexagons(list_cameras[0], list_cameras[camera_id])

        cam1_pose = np.concatenate([np.eye(3), [[0],[0],[0]]], axis = -1)
        print(cam1_pose)
        cam1_proj_mat = camera_matrix @ cam1_pose

        r1 = R.from_euler('x', 15, degrees=True)
        r2 = R.from_euler('y', -14, degrees=True)
        r3 = r2 * r1

        cam2_pose = np.concatenate([r3.as_matrix(), [[50],[5],[0]]], axis = -1)
        print(cam2_pose)
        cam2_proj_mat = camera_matrix @ cam2_pose

        p3ds = []

        for uv1, uv2 in zip(current_image_points, reference_image_points):
            point = DLT(cam1_proj_mat, cam2_proj_mat, uv1, uv2)
            p3ds.append(point)
        p3ds = np.array(p3ds)

        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(projection='3d')

        ax.scatter(p3ds[:,0], np.zeros(len(p3ds[:,0])), p3ds[:,2], )
        plt.show()




        #nothing beyond this point works, proceed at your own risk



        _, rvec, tvec = cv2.solvePnP(reference_image_points, current_image_points, camera_matrix, dist_coeffs, flags= cv2.SOLVEPNP_ITERATIVE)
        rmat, _ = cv2.Rodrigues(rvec)

        relative_pose = np.hstack((rmat, tvec))
        relative_pose = np.vstack((relative_pose, np.array([0, 0, 0, 1])))
        absolute_pose = np.dot(reference_camera_pose, relative_pose)
        camera_poses.append(absolute_pose)
        world_points = []

        for point_idx in range(len(reference_image_points)):
            # Extract the 2D image points for the current feature from all cameras
            feature_points = [image_points[camera_idx][point_idx] for camera_idx in range(len(list_cameras))]
            feature_points = np.array(feature_points, dtype=np.float32)

            # Perform triangulation to estimate the 3D position of the feature point
            _, _, point_3d = cv2.triangulatePoints(camera_poses[0][:3], camera_poses[1][:3], feature_points[0], feature_points[1])
            
            # Add the estimated 3D point to the list of world points
            world_points.append(point_3d[:3] / point_3d[3])  # Normalize homogeneous coordinates

        all_world_points.append(world_points)
    plot3d(all_world_points, camera_poses)


def corresponding_hexagons(reference_camera, current_camera):
    reference_image_points  = []
    current_image_points =[]

    for ind,name in enumerate(reference_camera[1]):
        if name in current_camera[1]:
            cind = current_camera[1].index(name)
            reference_image_points.append(reference_camera[2][ind]) 
            current_image_points.append(current_camera[2][cind])
    reference_image_points = np.array(reference_image_points, dtype=np.float32)
    current_image_points = np.array(current_image_points, dtype=np.float32)
    print(len(reference_image_points))
    print(len(current_image_points))
    print(current_image_points.shape)
    print(reference_image_points.shape)
    return reference_image_points, current_image_points



def plot3d (world_points , camera_poses):
    # Convert the world points and camera poses to numpy arrays
    world_points = np.array(world_points)
    camera_poses = np.array(camera_poses)

    # Create a new figure and set up 3D axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the world points
    ax.scatter(world_points[:, 0], world_points[:, 1], world_points[:, 2], c='b', marker='o', label='World Points')

    # Plot the camera positions
    ax.scatter(camera_poses[:, 0, 3], camera_poses[:, 1, 3], camera_poses[:, 2, 3], c='r', marker='s', s=100, label='Camera Poses')

    # Plot lines connecting the camera positions to the world points
    for i in range(len(camera_poses)):
        ax.plot([camera_poses[i, 0, 3], world_points[i, 0]], [camera_poses[i, 1, 3], world_points[i, 1]], [camera_poses[i, 2, 3], world_points[i, 2]], c='g')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Model')

    # Set axis limits and equal aspect ratio
    ax.set_xlim3d(-10, 10)  # Adjust the limits according to your scene
    ax.set_ylim3d(-10, 10)
    ax.set_zlim3d(-10, 10)
    ax.set_box_aspect([1, 1, 1])  # Set equal aspect ratio for all axes

    # Add a legend
    ax.legend()

    # Show the plotg
    plt.show()