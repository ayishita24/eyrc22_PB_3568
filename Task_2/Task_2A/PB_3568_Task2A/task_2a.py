'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
*  Created:				
*  Last Modified:		8/10/2022
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
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2, detect_distance_sensor_3
# 					left_shift, right_shift, left_turn, right_turn
# Global variables:
# 					none

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################


def left_shift(sim):
    e = objectHandle = sim.getObject("/left_joint")
    r = objectHandle = sim.getObject("/right_joint")
    
    # left_joint = sim.getJointTargetVelocity(e)
    # right_joint = sim.getJointTargetVelocity(r)
    # sim.setJointTargetVelocity(e, -left_joint)
    # sim.setJointTargetVelocity(r, right_joint)
    distance_1 = detect_distance_sensor_1(sim)
    distance_2 = detect_distance_sensor_2(sim)
    distance_3 = detect_distance_sensor_3(sim)
    # print(distance_1,distance_2,distance_3)
    # count = 2
    sim.setJointTargetVelocity(e, -0.5)
    sim.setJointTargetVelocity(r, 0.5)

    while distance_2 > 0:
        distance_1 = detect_distance_sensor_1(sim)
        distance_2 = detect_distance_sensor_2(sim)
        distance_3 = detect_distance_sensor_3(sim)
        # print(distance_1, distance_2)
        sim.setJointTargetVelocity(e, -0.5)
        sim.setJointTargetVelocity(r, 0.5)
    # time.sleep(0.7)
    # time.sleep(0.77)
    # while distance_1>0 and distance_3>0 and distance_2 > 0 and distance_2 < 0.17:
    #     distance_1 = detect_distance_sensor_1(sim)
    #     distance_2 = detect_distance_sensor_2(sim)
    #     distance_3 = detect_distance_sensor_3(sim)
    #     sim.setJointTargetVelocity(e, -2)
    #     sim.setJointTargetVelocity(r, 2)
    #     print(distance_1,distance_2,distance_3)
    #     time.sleep(1)
    sim.setJointTargetVelocity(e, 4.7)
    sim.setJointTargetVelocity(r, 4.7)

def right_shift(sim):
    e = objectHandle = sim.getObject("/left_joint")
    r = objectHandle = sim.getObject("/right_joint")
    sim.setJointTargetVelocity(e, 0.5)
    sim.setJointTargetVelocity(r, -0.5)
    # count = 1
    # left_joint = sim.getJointTargetVelocity(e)
    # right_joint = sim.getJointTargetVelocity(r)
    # sim.setJointTargetVelocity(e, left_joint)
    # sim.setJointTargetVelocity(r, -right_joint)
    distance_1 = detect_distance_sensor_1(sim)
    distance_2 = detect_distance_sensor_2(sim)
    distance_3 = detect_distance_sensor_3(sim)
    # print(distance_1,distance_2,distance_3)
    # time.sleep(3.67)
    while distance_1 > 0:
        distance_1 = detect_distance_sensor_1(sim)
        distance_2 = detect_distance_sensor_2(sim)
        distance_3 = detect_distance_sensor_3(sim)
        # print(distance_1,distance_2,distance_3)
        sim.setJointTargetVelocity(e, 0.5)
        sim.setJointTargetVelocity(r, -0.5)
    # while distance_3 == 0.0:
    #     distance_1 = detect_distance_sensor_1(sim)
    #     distance_2 = detect_distance_sensor_2(sim)
    #     distance_3 = detect_distance_sensor_3(sim)
    #     print(distance_1,distance_2,distance_3)
    #     sim.setJointTargetVelocity(e, 0.5)
    #     sim.setJointTargetVelocity(r, -0.5)
    sim.setJointTargetVelocity(e, 4.7)
    sim.setJointTargetVelocity(r, 4.7)

def right_turn(sim):
    e = objectHandle = sim.getObject("/left_joint")
    r = objectHandle = sim.getObject("/right_joint")
    sim.setJointTargetVelocity(e, 2)
    sim.setJointTargetVelocity(r, -2)
    time.sleep(1.3)
    sim.setJointTargetVelocity(e, 4.7)
    sim.setJointTargetVelocity(r, 4.7)

def left_turn(sim):
    e = objectHandle = sim.getObject("/left_joint")
    r = objectHandle = sim.getObject("/right_joint")
    sim.setJointTargetVelocity(e, -2)
    sim.setJointTargetVelocity(r, 2)
    time.sleep(1.3)
    sim.setJointTargetVelocity(e, 4.7)
    sim.setJointTargetVelocity(r, 4.7)
    # n = n + 1
    # return n

def control_logic(sim):
    """
    Purpose:
    ---
    This function should implement the control logic for the given problem statement
    You are required to actuate the rotary joints of the robot in this function, such that
    it traverses the points in given order

    Input Arguments:
    ---
    `sim`    :   [ object ]
            ZeroMQ RemoteAPI object

    Returns:
    ---
    None

    Example call:
    ---
    control_logic(sim)
    """
    ##############  ADD YOUR CODE HERE  ##############

    e = objectHandle = sim.getObject("/left_joint")
    r = objectHandle = sim.getObject("/right_joint")
    sim.setJointTargetVelocity(e, 6)
    sim.setJointTargetVelocity(r, 6)
    # n=0
    # n=left_turn(sim,n)
    # print("num of left turns: ",n)
    # if n > 4:
    #     sim.stopSimulation
    # n = time.sleep(2.55)
    # print(type(n))
    # list matrix=sim.buildMatrix(list position,list eulerAngles)
    # print(matrix)
    # left_joint = sim.getJointTargetVelocity(e)
    # right_joint = sim.getJointTargetVelocity(r)
    # print(left_joint)
    # print(right_joint)
    # time.sleep(200)
    while True:
        # left_turn(sim)
        # if distance_2 < 0.1741:
        #     sim.setJointTargetVelocity(e, oo)
        #     sim.setJointTargetVelocity(r, 0.51)
        #     print("left turn")
        #     time.sleep(1)
        #     sim.setJointTargetVelocity(r, uu)
        # elif distance_2 > 0.1748:
        #     sim.setJointTargetVelocity(e, 0.51)
        #     sim.setJointTargetVelocity(r, uu)
        #     print("right turn")
        #     time.sleep(1)
        #     sim.setJointTargetVelocity(e, oo)
        # else:
        #     sim.setJointTargetVelocity(e, oo)
        #     sim.setJointTargetVelocity(r, uu)
        # # if (distance_1 > 0 and distance_1 < 0.21) and (distance_2 > 0.1 and distance_2 < 0.4):
        # #     sim.stopSimulation()
        # #     break
        # while True:
        distance_1 = detect_distance_sensor_1(sim)
        distance_2 = detect_distance_sensor_2(sim)
        distance_3 = detect_distance_sensor_3(sim)
        # print("dist_1: ",distance_1)
        # print("dist_2: ",distance_2)
        # print("dist_3: ",distance_3)
        # count = 0
            # if distance_2 > 0.1 and distance_2 < 0.4:
        if distance_1 == 0 and distance_2 == 0 and distance_3 > 0:
            continue
        elif (distance_3 > 0) and (distance_1 > 0 and distance_1 < 0.32) and (distance_2 > 0 and distance_2 < 0.32):
            # print("right")
            right_turn(sim)
            distance_1 = detect_distance_sensor_1(sim)
            distance_2 = detect_distance_sensor_2(sim)
            distance_3 = detect_distance_sensor_3(sim)
            # print("dist_1: ",distance_1)
            # print("dist_2: ",distance_2)
            # print("dist_3: ",distance_3)
            if (distance_3 > 0) and (distance_1 > 0) and (distance_2 > 0):
                # time.sleep(2)
                # print("huh")
                sim.setJointTargetVelocity(e, -0.5)
                sim.setJointTargetVelocity(r, 0.5)
                time.sleep(0.1)
                break
            else:
                sim.setJointTargetVelocity(e, 3)
                sim.setJointTargetVelocity(r, 3)
            
        elif (distance_3 == 0) and (distance_1 > 0 and distance_1 < 0.32) and (distance_2 > 0 and distance_2 < 0.32):
            # print("left")
            left_turn(sim)
            distance_1 = detect_distance_sensor_1(sim)
            distance_2 = detect_distance_sensor_2(sim)
            distance_3 = detect_distance_sensor_3(sim)
            if (distance_3 == 0) and (distance_1 > 0) and (distance_2 > 0):
                # time.sleep(2)
                # print("huh")
                sim.setJointTargetVelocity(e, -0.5)
                sim.setJointTargetVelocity(r, 0.5)
                time.sleep(0.1)
                break
            else:
                sim.setJointTargetVelocity(e, 4)
                sim.setJointTargetVelocity(r, 4)
        elif (distance_3 > 0) and (distance_1 > 0 and distance_1 < 0.32) and (distance_2 == 0):
            # print("right")
            # if count == 1:
            #     sim.simulation_stopped
            #     break
            right_shift(sim)
        elif (distance_3 > 0) and (distance_2 > 0 and distance_2 < 0.32) and (distance_1 == 0):
            # print("left")
            # if count == 2:
            #     sim.simulation_stopped
            #     break
            left_shift(sim)
        
    sim.simulation_stopped
        # elif (distance_3 > 0 and distance_3 < 0.24) and (distance_2 > 0 and distance_2 < 0.3) and (distance_1 > 0 and distance_1 < 0.3):
        #     sim.simulation_stopped
        #     break

        #             sim.setJointTargetVelocity(e, -uu)
        #             sim.setJointTargetVelocity(r, uu)
        #             time.sleep(3.35)
        #             if distance_2 == 0:
        #                 sim.setJointTargetVelocity(e, oo)
        #                 sim.setJointTargetVelocity(r, uu)
        #             else:
        #                 sim.simulation_stopped

        #         else:
        #             sim.setJointTargetVelocity(e, oo)
        #             sim.setJointTargetVelocity(r, uu)
        #         continue

        #     elif distance_2 == 0:
        #         if distance_1 > 0 and distance_1 < 0.22:
        #             sim.setJointTargetVelocity(e, oo)
        #             sim.setJointTargetVelocity(r, -oo)
        #             time.sleep(3.5)
        #             sim.setJointTargetVelocity(e, oo)
        #             sim.setJointTargetVelocity(r, uu)
        #         else:
        #             sim.setJointTargetVelocity(e, oo)
        #             sim.setJointTargetVelocity(r, uu)
        #     else:
        #         sim.setJointTargetVelocity(e, oo)
        #         sim.setJointTargetVelocity(r, uu)

    ##################################################


def detect_distance_sensor_1(sim):
    """
    Purpose:
    ---
    Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

    Input Arguments:
    ---
    `sim`    :   [ object ]
            ZeroMQ RemoteAPI object

    Returns:
    ---
    distance  :  [ float ]
        distance of obstacle from sensor

    Example call:
    ---
    distance_1 = detect_distance_sensor_1(sim)
    """
    distance = None
    ##############  ADD YOUR CODE HERE  ##############

    q = objectHandle = sim.getObject("/distance_sensor_1")
    result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
        q)

    ##################################################
    return distance


def detect_distance_sensor_2(sim):
    """
    Purpose:
    ---
    Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

    Input Arguments:
    ---
    `sim`    :   [ object ]
            ZeroMQ RemoteAPI object

    Returns:
    ---
    distance  :  [ float ]
        distance of obstacle from sensor

    Example call:
    ---
    distance_2 = detect_distance_sensor_2(sim)
    """
    distance = None
    ##############  ADD YOUR CODE HERE  ##############

    w = objectHandle = sim.getObject("/distance_sensor_2")
    result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
        w)

    ##################################################
    return distance


def detect_distance_sensor_3(sim):
    l = objectHandle = sim.getObject("/distance_sensor_3")
    result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
        l)

    return distance

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########


if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')

    try:

        # Start the simulation using ZeroMQ RemoteAPI
        try:
            return_code = sim.startSimulation()
            if sim.getSimulationState() != sim.simulation_stopped:
                print('\nSimulation started correctly in CoppeliaSim.')
            else:
                print('\nSimulation could not be started correctly in CoppeliaSim.')
                sys.exit()

        except Exception:
            print('\n[ERROR] Simulation could not be started !!')
            traceback.print_exc(file=sys.stdout)
            sys.exit()

        # Runs the robot navigation logic written by participants
        try:
            control_logic(sim)
            time.sleep(5)

        except Exception:
            print(
                '\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
            print('Stop the CoppeliaSim simulation manually if required.\n')
            traceback.print_exc(file=sys.stdout)
            print()
            sys.exit()

        # Stop the simulation using ZeroMQ RemoteAPI
        try:
            return_code = sim.stopSimulation()
            time.sleep(0.5)
            if sim.getSimulationState() == sim.simulation_stopped:
                print('\nSimulation stopped correctly in CoppeliaSim.')
            else:
                print('\nSimulation could not be stopped correctly in CoppeliaSim.')
                sys.exit()

        except Exception:
            print('\n[ERROR] Simulation could not be stopped !!')
            traceback.print_exc(file=sys.stdout)
            sys.exit()

    except KeyboardInterrupt:
        # Stop the simulation using ZeroMQ RemoteAPI
        return_code = sim.stopSimulation()
        time.sleep(0.5)
        if sim.getSimulationState() == sim.simulation_stopped:
            print('\nSimulation interrupted by user in CoppeliaSim.')
        else:
            print('\nSimulation could not be interrupted. Stop the simulation manually .')
            sys.exit()
