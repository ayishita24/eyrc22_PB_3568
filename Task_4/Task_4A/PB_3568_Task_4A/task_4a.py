'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*
*  This script is intended for implementation of Task 4A
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_4a.py
*  Created:
*  Last Modified:		02/01/2023
*  Author:				e-Yantra Team
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
# Filename:			task_4a.py
# Functions:		transform_coordinates, place_packages, place_traffic_signals, place_start_end_nodes,
#                   place_horizontal_barricade, place_vertical_barricade
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
from zmqRemoteApi import RemoteAPIClient
import zmq
import os
import time

##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
dictx = {
    "A": 100,
    "B": 200,
    "C": 300,
    "D": 400,
    "E": 500,
    "F": 600
}

dicty = {
    "1": 100,
    "2": 200,
    "3": 300,
    "4": 400,
    "5": 500,
    "6": 600
}

shapes = {
    "Circle": "cylinder",
    "Triangle": "cone",
    "Square": "cube"
}

def transform_coordinates(x,y):
    c_x = (350-x)/280.9
    c_y = (y-350)/280.9

    return c_x,c_y

##############################################################

def place_packages(medicine_package_details, sim, all_models):
    """
	Purpose:
	---
	This function takes details (colour, shape and shop) of the packages present in
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The packages should be inserted only into the
    designated areas in each shop as mentioned in the Task document.

    Functions from Regular API References should be used to set the position of the
    packages.

	Input Arguments:
	---
	`medicine_package_details` :	[ list ]
                                nested list containing details of the medicine packages present.
                                Each element of this list will contain
                                - Shop number as Shop_n
                                - Color of the package as a string
                                - Shape of the package as a string
                                - Centroid co-ordinates of the package

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene

	Example call:
	---
	all_models = place_packages(medicine_package_details, sim, all_models)
	"""
    models_directory = os.getcwd()
    packages_models_directory = os.path.join(models_directory, "package_models")
    arena = sim.getObject('/Arena')
####################### ADD YOUR CODE HERE #########################

    # print(medicine_package_details)
    m_details = {}
    for packages in medicine_package_details:
        packages_models = os.path.join(packages_models_directory,f"{packages[1]}_{shapes[packages[2]]}.ttm")
        pack = sim.loadModel(packages_models)
        all_models.append(pack)
        sim.setObjectAlias(pack,f"{packages[1]}_{shapes[packages[2]]}")
        

        m = int(packages[0][-1])
        y = 156.71875

        if m in m_details:
            x = m_details[m] + 21.5
        else:
            x = m*100 + 17.75

        m_details[m] = x

        c_x, c_y = transform_coordinates(x, y)

        sim.setObjectPosition(pack, sim.handle_parent, (c_x,c_y,0.0030))
        sim.setObjectParent(pack, arena, 1)

        # print(parent)

    # print(m_details)


####################################################################
    return all_models

def place_traffic_signals(traffic_signals, sim, all_models):
    """
	Purpose:
	---
	This function takes position of the traffic signals present in
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The signal should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the
    signals.

	Input Arguments:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	None

	Example call:
	---
	all_models = place_traffic_signals(traffic_signals, sim, all_models)
	"""
    models_directory = os.getcwd()
    traffic_sig_model = os.path.join(models_directory, "signals", "traffic_signal.ttm" )
    arena = sim.getObject('/Arena')
    
####################### ADD YOUR CODE HERE #########################

    for nodes in traffic_signals:
        traffic = sim.loadModel(traffic_sig_model)
        all_models.append(traffic)
        sim.setObjectAlias(traffic,"Signal_"+nodes)

        numx = dictx[nodes[0]]
        numy = dicty[nodes[1]]
        # print(numx,numy)
        c_x, c_y = transform_coordinates(numx, numy)
        sim.setObjectPosition(traffic, sim.handle_parent, (c_x,c_y,0.15588))
        sim.setObjectParent(traffic, arena, 1)
        # print(c_x,c_y)

####################################################################
    return all_models

def place_start_end_nodes(start_node, end_node, sim, all_models):
    """
	Purpose:
	---
	This function takes position of start and end nodes present in
    the arena and places them on the virtual arena.
    The models should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the
    start and end nodes.

	Input Arguments:
	---
	`start_node` : [ string ]
    `end_node` : [ string ]


    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None

	Example call:
	---
	all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
	"""
    models_directory = os.getcwd()
    start_node_model = os.path.join(models_directory, "signals", "start_node.ttm" )
    end_node_model = os.path.join(models_directory, "signals", "end_node.ttm" )
    arena = sim.getObject('/Arena')
####################### ADD YOUR CODE HERE #########################

    # print(start_node_model)

    start = sim.loadModel(start_node_model)
    end = sim.loadModel(end_node_model)
    # print("Object handle: ",end)
    sim.setObjectAlias(start, "Start_Node")
    sim.setObjectAlias(end, "End_Node")
    all_models.append(start)
    all_models.append(end)

    s_x = dictx[start_node[0]]
    s_y = dicty[start_node[1]]
    e_x = dictx[end_node[0]]
    e_y = dicty[end_node[1]]

    c_sx, c_sy = transform_coordinates(s_x, s_y)
    c_ex, c_ey = transform_coordinates(e_x, e_y)

    sim.setObjectPosition(start, sim.handle_parent, (c_sx,c_sy,0.15588))
    sim.setObjectPosition(end, sim.handle_parent, (c_ex,c_ey,0.15588))
    sim.setObjectParent(start, arena, 1)
    sim.setObjectParent(end, arena, 1)

####################################################################
    return all_models

def place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing horizontal roads present in
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    horizontal barricades on virtual arena. The barricade should be inserted
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the
    horizontal barricades.

	Input Arguments:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None

	Example call:
	---
	all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    horiz_barricade_model = os.path.join(models_directory, "barricades", "horizontal_barricade.ttm" )
    arena = sim.getObject('/Arena')
####################### ADD YOUR CODE HERE #########################

    for nodes in horizontal_roads_under_construction:
        h_barr = sim.loadModel(horiz_barricade_model)
        all_models.append(h_barr)
        sim.setObjectAlias(h_barr,"Horizontal_missing_road_"+nodes)

        h_x = dictx[nodes[0]] + 50
        h_y = dicty[nodes[-1]]

        c_x, c_y = transform_coordinates(h_x, h_y)

        sim.setObjectPosition(h_barr, sim.handle_parent, (c_x,c_y,0.0030))
        sim.setObjectParent(h_barr, arena, 1)

####################################################################
    return all_models


def place_vertical_barricade(vertical_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing vertical roads present in
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    vertical barricades on virtual arena. The barricade should be inserted
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the
    vertical barricades.

	Input Arguments:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None

	Example call:
	---
	all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    vert_barricade_model = os.path.join(models_directory, "barricades", "vertical_barricade.ttm" )
    arena = sim.getObject('/Arena')
####################### ADD YOUR CODE HERE #########################
    for nodes in vertical_roads_under_construction:
        v_barr = sim.loadModel(vert_barricade_model)
        all_models.append(v_barr)
        sim.setObjectAlias(v_barr, "Vertical_missing_road_"+nodes)

        v_x = dictx[nodes[0]]
        v_y = dicty[nodes[-1]] - 50

        c_x, c_y = transform_coordinates(v_x, v_y)

        sim.setObjectPosition(v_barr, sim.handle_parent, (c_x,c_y,0.0030))
        sim.setObjectParent(v_barr, arena, 1)

####################################################################
    return all_models

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')

    # path directory of images in test_images folder
    img_dir = os.getcwd() + "\\test_imgs\\"

    i = 0
    config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')
    
    print('\n============================================')
    print('\nFor maze_0.png')

    # object handles of each model that gets imported to the scene can be stored in this list
    # at the end of each test image, all the models will be removed
    all_models = []

    # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
    task_1 = __import__('task_1a')
    detected_arena_parameters = task_1.detect_arena_parameters(config_img)

    # obtain required arena parameters
    medicine_package_details = detected_arena_parameters["medicine_packages"]
    traffic_signals = detected_arena_parameters['traffic_signals']
    start_node = detected_arena_parameters['start_node']
    end_node = detected_arena_parameters['end_node']
    horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
    vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction']

    # print(detected_arena_parameters)

    print("[1] Setting up the scene in CoppeliaSim")
    all_models = place_packages(medicine_package_details, sim, all_models)
    all_models = place_traffic_signals(traffic_signals, sim, all_models)
    all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
    all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
    all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
    print("[2] Completed setting up the scene in CoppeliaSim")

    # wait for 10 seconds and then remove models
    time.sleep(10)
    print("[3] Removing models for maze_0.png")

    for i in all_models:
        sim.removeModel(i)


    choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')

    if choice == 'y':
        for i in range(1,5):

            print('\n============================================')
            print('\nFor maze_' + str(i) +'.png')
            config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

            # object handles of each model that gets imported to the scene can be stored in this list
            # at the end of each test image, all the models will be removed
            all_models = []

            # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
            task_1 = __import__('task_1a')
            detected_arena_parameters = task_1.detect_arena_parameters(config_img)

            # obtain required arena parameters
            medicine_package_details = detected_arena_parameters["medicine_packages"]
            traffic_signals = detected_arena_parameters['traffic_signals']
            start_node = detected_arena_parameters['start_node']
            end_node = detected_arena_parameters['end_node']
            horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
            vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction']

            print("[1] Setting up the scene in CoppeliaSim")
            place_packages(medicine_package_details, sim, all_models)
            place_traffic_signals(traffic_signals, sim, all_models)
            place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
            place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
            place_start_end_nodes(start_node, end_node, sim, all_models)
            print("[2] Completed setting up the scene in CoppeliaSim")

            # wait for 10 seconds and then remove models
            time.sleep(10)
            print("[3] Removing models for maze_" + str(i) + '.png')
            for i in all_models:
                sim.removeModel(i)
            