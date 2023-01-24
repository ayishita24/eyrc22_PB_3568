'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			3568
# Author List:		Kashmira, Ishita, Yash
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters, no_of_coloured_pixels, Sort
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

dictx = {
        100: "A",
        200: "B",
        300: "C",
        400: "D",
        500: "E",
        600: "F",
        700: "G"
    }

dicty = {
    100: "1",
    200: "2",
    300: "3",
    400: "4",
    500: "5",
    600: "6",
    700: "7"
}

def no_of_coloured_pixels(image):
    count=0
    black=np.array([0,0,0])
    green=np.array([75,255,0])
    pink=np.array([255,0,255])
    orange=np.array([255,128,0])
    blue=np.array([0,0,255])
    shape=''
    colour=''
    for i in range(0,40,1):
        for j in range(0,40,1):
            if (image[i][j]!=black).any():
                count=count+1
                if (count==1):
                    if(image[i][j+1]!=black).any():
                        shape="Square"
                    if(image[i][j]==pink).all():
                        colour="Green"
                    elif(image[i][j]==green).all():
                        colour="Pink"
                    elif(image[i][j]==orange).all():
                        colour="Orange"
                    else:
                        colour="Skyblue"
    if (shape==''):
        if (count<300 and count>0):
            shape="Triangle"
        elif(count>0):
            shape="Circle"
        else:
            shape=''
    firstpixel=[shape,count,colour]
    return firstpixel

def Sort(sub_li):
    sub_li.sort(key = lambda x: x[0]+x[1])
    return sub_li
  

##############################################################

def detect_start_node(maze_image):
    start_node = ""
    img = cv2.cvtColor(maze_image, cv2.COLOR_BGR2RGB)
    for i in range (100,700,100):
        for j in range (100,700,100):
            if img[i,j,0] == 0 and img[i,j,1] == 255 and img[i,j,2] == 0 :
                start_node += (dictx[j]+dicty[i])

    return start_node

def detect_end_node(maze_image):
    end_node = ""
    img = cv2.cvtColor(maze_image, cv2.COLOR_BGR2RGB)
    for i in range (100,700,100):
        for j in range (100,700,100):
            if img[i,j,0] == 105 and img[i,j,1] == 43 and img[i,j,2] == 189 :
                end_node += (dictx[j]+dicty[i])

    return end_node

def detect_traffic_signals(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list of
    nodes in which traffic signals are present in the image

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `traffic_signals` : [ list ]
            list containing nodes in which traffic signals are present

    Example call:
    ---
    traffic_signals = detect_traffic_signals(maze_image)
    """    
    traffic_signals = []

    ##############	ADD YOUR CODE HERE	##############
    maze = cv2.cvtColor(maze_image, cv2.COLOR_BGR2RGB)
    for i in range (100,700,100):
        for j in range (100,700,100):
            if maze[i,j,0] == 255 and maze[i,j,1] == 0 and maze[i,j,2] == 0 :
                traffic_signals.append(dictx[j]+dicty[i])
    ##################################################

    return traffic_signals


def detect_horizontal_roads_under_construction(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing horizontal links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `horizontal_roads_under_construction` : [ list ]
            list containing missing horizontal links

    Example call:
    ---
    horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
    """    
    horizontal_roads_under_construction = []

    ##############	ADD YOUR CODE HERE	##############
    r=100
    l=0
    black = np.array([0, 0, 0])
    for c in range(100,700,100):
        for r in range(100,600,100):
            l = r + 50
            if (maze_image[int(c),int(l)] != black).all(): 
                horizontal_roads_under_construction.append(f"{dictx[int(l-50)]+dicty[c]}-{dictx[int(l+50)]+dicty[c]}")
        r=100
    ##################################################

    return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing vertical links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `vertical_roads_under_construction` : [ list ]
            list containing missing vertical links

    Example call:
    ---
    vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
    """    
    vertical_roads_under_construction = []

    ##############	ADD YOUR CODE HERE	##############
    c=100
    l=0
    black = np.array([0, 0, 0])
    for r in range(100,700,100):
        for c in range(100,600,100):
            l = c+50
            if (maze_image[int(l),r] != black).all(): 
                vertical_roads_under_construction.append(f"{dictx[r]+dicty[int(l-50)]}-{dictx[r]+dicty[int(l+50)]}")
        c=100
    ##################################################

    return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a nested list of
    details of the medicine packages placed in different shops

    ** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
       as well as in the alphabetical order of colors.
       For example, the list should first have the packages of shop_1 listed. 
       For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `medicine_packages` : [ list ]
            nested list containing details of the medicine packages present.
            Each element of this list will contain 
            - Shop number as Shop_n
            - Color of the package as a string
            - Shape of the package as a string
            - Centroid co-ordinates of the package
    Example call:
    ---
    medicine_packages = detect_medicine_packages(maze_image)
    """    
    medicine_packages = []

    ##############	ADD YOUR CODE HERE	##############
    cx=0
    cy=0
    shop=0
    shopspecs=[]
    for k in range(100,600,100):
        cropped_image = maze_image[110:190, k+10:k+90]
        for i in range(0,80,40):
            for j in range(0,80,40):
                cropped_images= cropped_image[i:(i+40), j:(j+40)]
                cx=20+j 
                cy=20+i
                cropped_images = cv2.bitwise_not(cropped_images)
                np_img = np.array(cropped_images)
                p=no_of_coloured_pixels(np_img)
                cx=cx+k+10
                cy=cy+110
                shopno="Shop_"+str(int(k/100))
                if(p[1]!=0):
                    if(p[0]=="Triangle"):
                        centroid=[cx,cy-1]
                    else:
                        centroid=[cx,cy]
                    shopspecs=[shopno,p[2],p[0],centroid]
                    medicine_packages.append(shopspecs)

                    # plotPoint(maze_image, cy, cx)
    
                    # plt.imshow(maze_image)
                    # plt.show()
    medicine_packages=Sort(medicine_packages)
    ##################################################
    return medicine_packages

def detect_arena_parameters(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary
    containing the details of the different arena parameters in that image

    The arena parameters are of four categories:
    i) traffic_signals : list of nodes having a traffic signal
    ii) horizontal_roads_under_construction : list of missing horizontal links
    iii) vertical_roads_under_construction : list of missing vertical links
    iv) medicine_packages : list containing details of medicine packages

    These four categories constitute the four keys of the dictionary

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `arena_parameters` : { dictionary }
            dictionary containing details of the arena parameters

    Example call:
    ---
    arena_parameters = detect_arena_parameters(maze_image)
    """    
    arena_parameters = {}

    ##############	ADD YOUR CODE HERE	##############
    
    arena_parameters["traffic_signals"] = detect_traffic_signals(maze_image)
    arena_parameters["horizontal_roads_under_construction"] = detect_horizontal_roads_under_construction(maze_image)
    arena_parameters["vertical_roads_under_construction"] = detect_vertical_roads_under_construction(maze_image)
    arena_parameters["medicine_packages"] = detect_medicine_packages(maze_image)
    arena_parameters["start_node"] = detect_start_node(maze_image)
    arena_parameters["end_node"] = detect_end_node(maze_image)
    
    ##################################################

    return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
    img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
    file_num = 0
    img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'

    # read image using opencv
    maze_image = cv2.imread(img_file_path)

    print('\n============================================')
    print('\nFor maze_' + str(file_num) + '.png')

    # detect and print the arena parameters from the image
    arena_parameters = detect_arena_parameters(maze_image)

    print("Arena Prameters: " , arena_parameters)

    # display the maze image
    cv2.imshow("image", maze_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')

    if choice == 'y':

        for file_num in range(1, 15):

            # path to maze image file
            img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'

            # read image using opencv
            maze_image = cv2.imread(img_file_path)

            print('\n============================================')
            print('\nFor maze_' + str(file_num) + '.png')

            # detect and print the arena parameters from the image
            arena_parameters = detect_arena_parameters(maze_image)

            print("Arena Parameter: ", arena_parameters)

            # display the test image
            cv2.imshow("image", maze_image)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()