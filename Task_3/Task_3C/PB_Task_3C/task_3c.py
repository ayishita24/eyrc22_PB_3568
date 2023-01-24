'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			3568
# Author List:		Ishita Yadav, Kashmira Sukhtankar, Yash Waghmare
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
#


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2
import numpy
from numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################


#####################################################################################

def perspective_transform(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array

    Example call:
    ---
    warped_image = perspective_transform(image)
    """
    warped_image = []
#################################  ADD YOUR CODE HERE  ###############################
    # cv2.circle(image, (570, 60), 5, (0, 0, 255), -1)
    # cv2.circle(image, (1440, 80), 5, (0, 255, 255), -1)
    # cv2.circle(image, (570, 900), 5, (255, 0, 255), -1)
    # cv2.circle(image, (1390, 930), 5, (255, 255, 255), -1)
    pts1 = numpy.float32([[683,163], [1407,155], [700,875], [1400,880]])
    pts2 = numpy.float32([[0, 0], [637, 0], [0, 637], [637, 637]])
    pers_M = cv2.getPerspectiveTransform(pts1, pts2)
    rows, cols, ch = image.shape
    transform_pers = cv2.warpPerspective(image, pers_M, (cols, rows))
    warped_image = transform_pers[0:637, 0:637]
    # cv2.imshow("warp", warped_image)
    # cv2.waitKey(0)
    # print(warped_image)
######################################################################################

    return warped_image


def transform_values(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns the
    position and orientation of the ArUco marker (with id 5), in the
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]

    HINT:
        Initially the image should be cropped using perspective transform
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.

    Example call:
    ---
    scene_parameters = transform_values(image)
    """
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################
    details, corners = task_1b.detect_ArUco_details(thresh)
    if 5 in details:
        aruco_5 = details[5]
        x = aruco_5[0][0]
        y = aruco_5[0][1]
        A = aruco_5[1]
        # c_x = (-(3*(x))+955)/1000 + 0.00603
        c_x = (-(3*(x))+955)/1000 - 0.012805556
        # c_y = ((3*(y))-955)/1000 + 0.01497
        c_y = ((3*(y))-955)/1000 + -0.015472222
        # c_angle = A
        # if A<=0:
        #     c_angle=A+180
        # elif A>0:
        #     c_angle=A-180
        
        if A>=-90 and A<=90:
            c_angle = A + 90 +90
        elif A<-90 and A>=-180:
            c_angle = A + 90 +90
        elif A>90 and A<=180:
            c_angle = A-270 +90
        else:
            c_angle = -90
        c_angle = (c_angle*3.142)/180
        scene_parameters = [c_x, c_y, c_angle]
    else:
        scene_parameters = [-1, -1, -1]


######################################################################################

    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.

    Example call:
    ---
    set_values(scene_parameters)
    """
    aruco_handle = sim.getObject('/aruco_5')
#################################  ADD YOUR CODE HERE  ###############################
    param = scene_parameters
    sim.setObjectPosition(aruco_handle, sim.handle_world, (param[0],param[1],0.0030))
    sim.setObjectOrientation(aruco_handle, sim.handle_parent, [0 ,0 ,param[2]])
######################################################################################

    return None


if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    # sim.setObjectPosition()
    task_1b = __import__('task_1b')
#################################  ADD YOUR CODE HERE  ################################
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
    # print
    while True:
        ret, image = cap.read()
        # cv2.imshow("img", image)
        warped = perspective_transform(image)
        ret, thresh = cv2.threshold(warped, 120, 255, cv2.THRESH_BINARY)
        details, corners = task_1b.detect_ArUco_details(thresh)
        # task_1b.mark_ArUco_image(warped, details, corners)
        # crop = warped[30:617, 30:617]
        crop = warped[54:585, 44:582]
        crop = cv2.resize(crop,(637,637))
        # cv2.imshow("warped", warped)
        
        parameters = transform_values(crop)
        if parameters == [-1, -1, -1]:
            continue
        # print(parameters)
        set_values(parameters)
        # cv2.circle(crop, (23, 23), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (140, 19), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (260, 15), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (383, 15), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (504, 20), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (620, 25), 5, (0, 0, 255), -1)
        # #2
        # cv2.circle(crop, (13, 137), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (135, 135), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (260, 133), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (385, 135), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (510, 135), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (626, 138), 5, (0, 0, 255), -1)
        # #3
        # cv2.circle(crop, (12, 263), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (135, 260), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (260, 260), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (385, 260), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (510, 260), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (626, 260), 5, (0, 0, 255), -1)
        # #4
        # cv2.circle(crop, (11, 388), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (135, 389), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (260, 388), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (387, 388), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (510, 385), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (629, 382), 5, (0, 0, 255), -1)
        # #5
        # cv2.circle(crop, (14, 510), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (135, 513), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (260, 515), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (387, 512), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (510, 510), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (624, 502), 5, (0, 0, 255), -1)
        # #6
        # cv2.circle(crop, (20, 622), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (138, 630), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (260, 630), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (385, 630), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (505, 623), 5, (0, 0, 255), -1)
        # cv2.circle(crop, (618, 617), 5, (0, 0, 255), -1)
        
        # cv2.imshow("crop", crop)
        cv2.imshow("frame", warped)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # perspective_transform(image)
    # print(details)
    cv2.destroyAllWindows()
    # print(details)
    # param = transform_values(pic)
    # print(param)

    # while True:
    #     task_1b.mark_ArUco_image(
    #         image, task_1b.ArUco_details_dict, task_1b.ArUco_corners)
    # print(ArUco_details_dict)


#######################################################################################
