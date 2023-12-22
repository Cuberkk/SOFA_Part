import numpy as np
import open3d as o3d
import cv2
import os
import sys
from sys import platform
from harvesters.core import Harvester
import threading
import time

def point_cloud_check(point_cloud_component):
    
    pointcloud = np.zeros((point_cloud_component.height * point_cloud_component.width, 3))
    if point_cloud_component.width > 0 and point_cloud_component.height > 0:
        pointcloud = point_cloud_component.data.reshape(point_cloud_component.height * point_cloud_component.width, 3).copy()
    else:
        print("PointCloud is empty!")
        
    return pointcloud

def texture_check(texture_grey_component , texture_rgb_component , point_cloud_component):
    
    texture = np.zeros((texture_grey_component.height, texture_grey_component.width))
    texture_rgb = np.zeros((point_cloud_component.height * point_cloud_component.width, 3))
    if texture_grey_component.width > 0 and texture_grey_component.height > 0:
        texture = texture_grey_component.data.reshape(texture_grey_component.height, texture_grey_component.width, 1).copy()
        texture_rgb[:, 0] = np.reshape(texture, -1)
        texture_rgb[:, 1] = np.reshape(texture, -1)
        texture_rgb[:, 2] = np.reshape(texture, -1)
    elif texture_rgb_component.width > 0 and texture_rgb_component.height > 0:
        texture = texture_rgb_component.data.reshape(texture_rgb_component.height, texture_rgb_component.width, 3).copy()
        texture_rgb[:, 0] = np.reshape(1/65536 * texture[:, :, 0], -1)
        texture_rgb[:, 1] = np.reshape(1/65536 * texture[:, :, 1], -1)
        texture_rgb[:, 2] = np.reshape(1/65536 * texture[:, :, 2], -1)
    else:
        print("TextureRGB is empty!")
        
    return texture_rgb

def Layer_1st(pointcloud):
    
    pointcloud_1st_edition = pointcloud.copy()
    pointcloud_1st_edition[np.logical_or(pointcloud_1st_edition[: , 0] < 45 , pointcloud_1st_edition[: , 0] > 65)] = 0 #Filt with X position data
    pointcloud_1st_edition[np.logical_or(pointcloud_1st_edition[: , 1] < 130 , pointcloud_1st_edition[: , 1] > 140)] = 0 #Filt with Y position data
    pointcloud_1st_edition[np.logical_or(pointcloud_1st_edition[: , 2] < 85, pointcloud_1st_edition[: , 2] > 110)] = 0 #Filt with Z position data
    
    return pointcloud_1st_edition

def Layer_2nd(texture_rgb , pointcloud_1st_edition):
    
    texture_greyscale_1st = texture_rgb.copy()
    texture_greyscale_1st[np.all(pointcloud_1st_edition == 0, axis = 1)] = 0
        
    texture_greyscale_2nd = texture_greyscale_1st.copy()
    texture_greyscale_2nd[(texture_greyscale_2nd[: , 0] > 275)] = 0 #Filt with greyscale channel information
    
    return texture_greyscale_2nd

def vertex_selection(pointcloud_2nd_edition):
    
    x_max = np.max(pointcloud_2nd_edition[: , 0])
    z_max = np.max(pointcloud_2nd_edition[: , 2])                    
    pointcloud_non_zero_x = pointcloud_2nd_edition[pointcloud_2nd_edition[: , 0] != 0][: , 0]
    x_min = np.min(pointcloud_non_zero_x)
    pointcloud_non_zero_y = pointcloud_2nd_edition[pointcloud_2nd_edition[: , 1] != 0][: , 1]
    y_min = np.min(pointcloud_non_zero_y)
    pointcloud_non_zero_z = pointcloud_2nd_edition[pointcloud_2nd_edition[: , 2] != 0][: , 2]
    z_min = np.min(pointcloud_non_zero_z)
    print("x_max:", x_max, "\nx_min:", x_min, "\ny_min:", y_min, "\nz_max:", z_max, "\nz_min", z_min)
    
    target_point_lower_left = np.array([x_max, y_min, z_min])
    target_point_upper_left = np.array([x_min, y_min, z_min])
    target_point_lower_right = np.array([x_max, y_min, z_max])
    target_point_upper_right = np.array([x_min, y_min, z_max])
    
    distance_lower_left = np.linalg.norm(pointcloud_2nd_edition - target_point_lower_left, axis=1)
    nearest_index_lower_left = np.argmin(distance_lower_left)
    nearest_point_lower_left = pointcloud_2nd_edition[nearest_index_lower_left]
    
    distance_upper_left = np.linalg.norm(pointcloud_2nd_edition - target_point_upper_left, axis=1)
    nearest_index_upper_left = np.argmin(distance_upper_left)
    nearest_point_upper_left = pointcloud_2nd_edition[nearest_index_upper_left]
    
    distance_lower_right = np.linalg.norm(pointcloud_2nd_edition - target_point_lower_right, axis=1)
    nearest_index_lower_right = np.argmin(distance_lower_right)
    nearest_point_lower_right = pointcloud_2nd_edition[nearest_index_lower_right]
    
    distance_upper_right = np.linalg.norm(pointcloud_2nd_edition - target_point_upper_right, axis=1)
    nearest_index_upper_right = np.argmin(distance_upper_right)
    nearest_point_upper_right = pointcloud_2nd_edition[nearest_index_upper_right]                    
    print("Lower_Left: Target_point:", target_point_lower_left, "Nearest_Point", nearest_point_lower_left)
    print("Upper_Left: Target_point:", target_point_upper_left, "Nearest_Point", nearest_point_upper_left)
    print("Lower_right: Target_point:", target_point_lower_right, "Nearest_Point", nearest_point_lower_right)
    print("Upper_right: Target_point:", target_point_upper_right, "Nearest_Point", nearest_point_upper_right)
    
    return nearest_index_lower_left, nearest_index_upper_left, nearest_index_lower_right, nearest_index_upper_right

def visualize_pointcloud(nearest_index_lower_left, nearest_index_upper_left, nearest_index_lower_right, nearest_index_upper_right, pointcloud, texture_rgb):
    
    pointcloud_vis = pointcloud.copy()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pointcloud_vis)
    texture_visual = texture_rgb.copy()
    texture_visual[nearest_index_lower_left] = [65535, 0, 0]
    texture_visual[nearest_index_upper_left] = [65536, 0, 0]
    texture_visual[nearest_index_lower_right] = [65536, 0, 0]
    texture_visual[nearest_index_upper_right] = [65536, 0, 0]
    texture_vis = cv2.normalize(1/65536 * texture_visual, dst=None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    pcd.colors = o3d.utility.Vector3dVector(texture_vis)
    o3d.visualization.draw_geometries([pcd], width=800,height=600)

    return pcd
    

def freerun():
    # PhotoneoTL_DEV_<ID>
    device_id = "PhotoneoTL_DEV_IDV-016"
    print("--> device_id: ", device_id)

    if platform == "win32":
        cti_file_path_suffix = "/API/bin/photoneo.cti"
        save_last_scan_path_prefix = "C:/Users/Public"
    else:
        cti_file_path_suffix = "/API/lib/photoneo.cti"
        save_last_scan_path_prefix = "~"
    cti_file_path = os.getenv('PHOXI_CONTROL_PATH') + cti_file_path_suffix
    print("--> cti_file_path: ", cti_file_path)

    with Harvester() as h:
        h.add_file(cti_file_path, True, True)
        h.update()

        # Print out available devices
        print()
        print("Name : ID")
        print("---------")
        for item in h.device_info_list:
            print(item.property_dict['serial_number'], ' : ', item.property_dict['id_'])
        print()

        with h.create({'id_': device_id}) as ia:
            features = ia.remote_device.node_map
            
            print("TriggerMode BEFORE: ", features.PhotoneoTriggerMode.value)
            features.PhotoneoTriggerMode.value = "Freerun"
            print("TriggerMode AFTER: ", features.PhotoneoTriggerMode.value)
            
            # Order is fixed on the selected output structure. Disabled fields are shown as empty components.
            # Individual structures can enabled/disabled by the following features:
            # SendTexture, SendPointCloud, SendNormalMap, SendDepthMap, SendConfidenceMap, SendEventMap, SendColorCameraImage
            # payload.components[#]
            # [0] Texture
            # [1] TextureRGB
            # [2] PointCloud [X,Y,Z,...]
            # [3] NormalMap [X,Y,Z,...]
            # [4] DepthMap
            # [5] ConfidenceMap
            # [6] EventMap
            # [7] ColorCameraImage

            features.SendTexture.value = True
            features.SendPointCloud.value = True
            features.SendNormalMap.value = False
            features.SendDepthMap.value = True
            features.SendConfidenceMap.value = False

            ia.start() 
            vis = o3d.visualization.Visualizer()
            # vis.create_window(window_name='Open3D Visualization', width=800, height=600)          
            while True:
                with ia.fetch(timeout=10.0) as buffer:

                    vis.poll_events()
                    vis.update_renderer()
                    vis.poll_events()
                    
                    # grab newest frame
                    # do something with second frame
                    payload = buffer.payload
                    
                    point_cloud_component = payload.components[2]
                    texture_grey_component = payload.components[0]
                    texture_rgb_component = payload.components[1]
                    
                    pointcloud = point_cloud_check(point_cloud_component)
                    texture_rgb = texture_check(texture_grey_component , texture_rgb_component , point_cloud_component)
                        
                    #First filtration using Point Cloud Data
                    pointcloud_v1 =Layer_1st(pointcloud)
                    first_filtered_points = np.sum(np.any(pointcloud_v1 != 0, axis=1))
                    print("There are:", first_filtered_points, "points after 1st filtration")
                    
                    #2nd filtration using Greyscale Channel Information
                    texture_greyscale_v2 = Layer_2nd(texture_rgb , pointcloud_v1)
                    second_filtered_points = np.sum(np.any(texture_greyscale_v2 != 0, axis=1))
                    print("There are:", second_filtered_points , "points after 2nd filtration")
                    pointcloud_2nd_edition = pointcloud_v1.copy()
                    pointcloud_2nd_edition[np.all(texture_greyscale_v2  == 0, axis=1)] = 0
                    
                    #Select 4 vertexes
                    nearest_index_lower_left, nearest_index_upper_left, nearest_index_lower_right, nearest_index_upper_right = vertex_selection(pointcloud_2nd_edition)
                    
                    #Visualize the filtered points
                    # pcd = visualize_pointcloud(nearest_index_lower_left, nearest_index_upper_left, nearest_index_lower_right, nearest_index_upper_right, pointcloud, texture_rgb)
                    
                    # vis.clear_geometries()
                    # vis.poll_events()
                    
                    # vis.add_geometry(pcd)
                    # vis.poll_events()
                    # vis.update_renderer()
                    # vis.poll_events()
                    time.sleep(1/8)


if __name__ == "__main__":
    freerun()