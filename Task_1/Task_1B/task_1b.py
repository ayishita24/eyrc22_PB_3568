'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1B of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:	PB_3568		[ Team-ID ]
# Author List:	Ishita, Yash, Kashmira	[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1b.py
# Functions:		detect_Qr_details, detect_ArUco_details
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import numpy as np
import cv2
from cv2 import aruco
import math
# from pyzbar import pyzbar
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################


##############################################################

def detect_Qr_details(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary such
    that the message encrypted in the Qr code is the key and the center
    co-ordinates of the Qr code is the value, for each item in the dictionary

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `Qr_codes_details` : { dictionary }
            dictionary containing the details regarding the Qr code

    Example call:
    ---
    Qr_codes_details = detect_Qr_details(image)
    """
    Qr_codes_details = {}

    ##############	ADD YOUR CODE HERE	##############
    x = 0
    y = 0
    for qrcode in pyzbar.decode(image):
        codedata = qrcode.data.decode('utf-8')
        points = (np.array([qrcode.polygon], np.int32))
        for i in points[0]:
            x = x+(i[0])
            y = y+(i[1])
        z = [x//4, y//4]
        x = 0
        y = 0
        Qr_codes_details[codedata] = [int(z[0]), int(z[1])]
    ##################################################

    return Qr_codes_details


def detect_ArUco_details(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary such
    that the id of the ArUco marker is the key and a list of details of the marker
    is the value for each item in the dictionary. The list of details include the following
    parameters as the items in the given order
        [center co-ordinates, angle from the vertical, list of corner co-ordinates] 
    This order should be strictly maintained in the output

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `ArUco_details_dict` : { dictionary }
            dictionary containing the details regarding the ArUco marker

    Example call:
    ---
    ArUco_details_dict = detect_ArUco_details(image)
    """
    ArUco_details_dict = {}  # should be sorted in ascending order of ids
    ArUco_corners = {}

    ##############	ADD YOUR CODE HERE	##############

    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(
        imgGray, aruco_dict, parameters=arucoParam)
    ArUco_details = {}
    ids_list = []
    angle_list = []
    a = 0
    b = 0
    for i in range(len(ids)):
        item_list = []
        dist_list = []
        ids_list.append(ids[i][0])
        ArUco_corners[int(ids[i][0])] = bboxs[i][0].tolist()
        for j in range(4):
            a = a + bboxs[i][0][j][0].tolist()
            b = b + bboxs[i][0][j][1].tolist()

        centroid_details = [int(a/4), int(b/4)]
        a = 0
        b = 0

        a1 = int(bboxs[i][0][0][0].tolist())
        a2 = int(bboxs[i][0][0][1].tolist())
        b1 = int(bboxs[i][0][1][0].tolist())
        b2 = int(bboxs[i][0][1][1].tolist())

        x2 = (a1+b1)//2
        y2 = -(a2+b2)//2
        x1 = centroid_details[0]
        y1 = -centroid_details[1]
        if x1 == x2:
            m = 0
        else:
            m = (y2-y1)/(x2-x1)

        angle = round(math.degrees(math.atan(m)))

        if (x1 < x2):
            angle = angle - 90

        elif (x2 < x1):
            angle = angle + 90

        angle_list.append(angle)
        ArUco_details[int(ids[i][0])] = [centroid_details, angle]

    ArUco_details_dict = dict(sorted(ArUco_details.items()))

    ##################################################

    return ArUco_details_dict, ArUco_corners

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE CODE BELOW #########

# marking the Qr code with center and message


def mark_Qr_image(image, Qr_codes_details):
    for message, center in Qr_codes_details.items():
        encrypted_message = message
        x_center = int(center[0])
        y_center = int(center[1])

        cv2.circle(img, (x_center, y_center), 5, (0, 0, 255), -1)
        cv2.putText(image, str(encrypted_message), (x_center + 20,
                    y_center + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)

    return image

# marking the ArUco marker with the center, angle and corners


def mark_ArUco_image(image, ArUco_details_dict, ArUco_corners):

    for ids, details in ArUco_details_dict.items():
        center = details[0]
        cv2.circle(image, center, 5, (0, 0, 255), -1)

        corner = ArUco_corners[int(ids)]
        cv2.circle(image, (int(corner[0][0]), int(
            corner[0][1])), 5, (50, 50, 50), -1)
        cv2.circle(image, (int(corner[1][0]), int(
            corner[1][1])), 5, (0, 255, 0), -1)
        cv2.circle(image, (int(corner[2][0]), int(
            corner[2][1])), 5, (128, 0, 255), -1)
        cv2.circle(image, (int(corner[3][0]), int(
            corner[3][1])), 5, (255, 255, 255), -1)

        tl_tr_center_x = int((corner[0][0] + corner[1][0]) / 2)
        tl_tr_center_y = int((corner[0][1] + corner[1][1]) / 2)

        cv2.line(image, center, (tl_tr_center_x,
                 tl_tr_center_y), (255, 0, 0), 5)
        display_offset = 2 * \
            int(math.sqrt(
                (tl_tr_center_x - center[0])**2+(tl_tr_center_y - center[1])**2))
        cv2.putText(image, str(ids), (center[0]+int(display_offset/2),
                    center[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        angle = details[1]
        cv2.putText(image, str(
            angle), (center[0]-display_offset, center[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    return image


if __name__ == "__main__":

    # path directory of images in test_images folder
    img_dir_path = "public_test_cases/"

    # choose whether to test Qr or ArUco images
    choice = input('\nWhich images do you want to test ? => "q" or "a": ')

    if choice == 'q':

        marker = 'qr'

    else:

        marker = 'aruco'

    for file_num in range(0, 2):
        img_file_path = img_dir_path + marker + '_' + str(file_num) + '.png'

        # read image using opencv
        img = cv2.imread(img_file_path)

        print('\n============================================')
        print('\nFor ' + marker + str(file_num) + '.png')

        # testing for Qr images
        if choice == 'q':
            Qr_codes_details = detect_Qr_details(img)
            print("Detected details of Qr: ", Qr_codes_details)

            # displaying the marked image
            img = mark_Qr_image(img, Qr_codes_details)
            cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # testing for ArUco images
        else:
            ArUco_details_dict, ArUco_corners = detect_ArUco_details(img)
            print("Detected details of ArUco: ", ArUco_details_dict)

            # displaying the marked image
            img = mark_ArUco_image(img, ArUco_details_dict, ArUco_corners)
            cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
