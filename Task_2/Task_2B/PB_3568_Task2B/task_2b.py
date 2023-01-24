'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
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
# Author List:		Kashmira, Yash, Ishita
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					forward,right,left
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
from re import A
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
##############################################################
dick = {
        1: ["LEFT","A"],
        2: ["RIGHT","B"],
        3: ["LEFT","C"],
        4: ["RIGHT","D"],
        5: ["FORWARD","E"],
        6: ["RIGHT","F"],
        7: ["LEFT","G"],
        8: ["RIGHT","H"],
        9: ["FORWARD","I"],
        10: ["RIGHT","J"],
        11: ["LEFT","K"],
        12: ["RIGHT","L"],
        13: ["FORWARD","M"],
        14: ["RIGHT","N"],
        15: ["LEFT","O"],
        16: ["RIGHT","P"],
        17: ["STOP","A"]
    }
################# ADD UTILITY FUNCTIONS HERE #################

# def plotPoint(img, x,y, color = (0, 255, 255)):
#     return cv2.circle(img, (x,y), radius=5, color=color, thickness=-1)
def forward(sim, e, r):
    sim.setJointTargetVelocity(e,3.5)
    sim.setJointTargetVelocity(r,3.5)
def right(sim, e, r):
    sim.setJointTargetVelocity(e,-0.35)
    sim.setJointTargetVelocity(r,2.5)
def left(sim, e, r):
    sim.setJointTargetVelocity(e,2.5)
    sim.setJointTargetVelocity(r,-0.35)




##############################################################

def control_logic(sim):
    """
    Purpose:
    ---
    This function should implement the control logic for the given problem statement
    You are required to make the robot follow the line to cover all the checkpoints
    and deliver packages at the correct locations.

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
    visionSensorHandle = sim.getObject('/vision_sensor')
    # print("gtdfgthv")
    black = np.array([0, 0, 0])
    white = np.array([255,255,255])
    # red   = np.array([0,0,255])
    yellow1=np.array([246,198,4])
    yellow2=np.array([242,196,8])
    y3=np.array([238,194,15])
    y4=np.array([245,197,4])
    y5=np.array([234,192,20])
    y6=np.array([245,200,14])
    grey1=np.array([150, 150, 150])
    e=sim.getObject("/left_joint")
    r=sim.getObject("/right_joint")
    oo=sim.getJointTargetVelocity(e)
    rr=sim.getJointTargetVelocity(r)
    sim.setJointTargetVelocity(e,0)
    sim.setJointTargetVelocity(r,0)
    # time.sleep(0.3)
    sim.setJointTargetVelocity(e,10)
    sim.setJointTargetVelocity(r,10)

    node=0
    # x=64

    while (True):
        image, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
        imag = np.frombuffer(image, dtype=np.uint8)
        imag=imag.reshape(resY, resX, 3)
        imag=cv2.cvtColor(imag,cv2.COLOR_BGR2RGB)
        imag=cv2.flip(imag,0)
        x,baw_image=cv2.threshold(imag,160,255,cv2.THRESH_BINARY_INV)
      
    
        cropped_image=imag[85:512-85,85:512-85]
        copy_image=imag.copy()
        # plotPoint(copy_image,140,286)
        # plotPoint(copy_image,180,306)
        # plotPoint(copy_image,362,306)
        # plotPoint(copy_image,322,286)
        # cropped_image=cv2.bitwise_not(cropped_image,0)
        #lx=140 rx322 ly286 ry286
        # cropped_image = cv2.GaussianBlur(cropped_image,(5,5),2)
        stop_image_l=copy_image[316:366,140:180]
        stop_image_r=copy_image[316:366,322:362]
        # cv2.imshow("lavde",stop_image_l)
        # cv2.waitKey(1)
        # cv2.imshow("lag gaye",stop_image_r)
        # cv2.waitKey(1)
    

        if(((stop_image_l==yellow1).any() or (stop_image_l==yellow2).any() or (stop_image_l==y3).any() or(stop_image_l==y4).any() or(stop_image_l==y4).any()) or(stop_image_l==y6).any())and ((stop_image_r==yellow1).any() or (stop_image_r==yellow2).any()  or (stop_image_r==y3).any()  or (stop_image_r==y4).any()  or (stop_image_r==y5).any() or (stop_image_r==y6).any()):
            sim.setJointTargetVelocity(e,-0.000000001)
            sim.setJointTargetVelocity(r,-0.000000001)
            print("Current checkpoint : ",dick[node+1][1])
            time.sleep(0.3)
           
            

           
            
            # ch=str(int(x))
            # print("tfgbf")
            if(dick[node+1][1]=="E"):
                sim.setJointTargetVelocity(e,0.2)
                sim.setJointTargetVelocity(r,0.2)
                ## Retrieve the handle of the Arena_dummy scene object.
                arena_dummy_handle = sim.getObject("/Arena_dummy") 
                ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
                ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
                sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint E")
                str=read_qr_code(sim)
                if(str=='Orange Cone'):
                    x="package_1"
                elif(str=='Blue Cylinder'):
                    x="package_2"
                elif(str=='Pink Cuboid'):
                    x="package_3"
                
                ## Deliver package_1 at checkpoint E
                sim.callScriptFunction("deliver_package", childscript_handle, x, "checkpoint E")

                ## Call the deactivate_qr_code() function defined in the child script to make the QR code invisible at checkpoint E
                sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint E")
            elif(dick[node+1][1]=="I"):
                sim.setJointTargetVelocity(e,0.3)
                sim.setJointTargetVelocity(r,0.3)
                ## Retrieve the handle of the Arena_dummy scene object.
                arena_dummy_handle = sim.getObject("/Arena_dummy") 
                ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
                ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint J
                sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint I")

                str=read_qr_code(sim)
                if(str=='Orange Cone'):
                    x="package_1"
                elif(str=='Blue Cylinder'):
                    x="package_2"
                elif(str=='Pink Cuboid'):
                    x="package_3"
                ## Deliver package_1 at checkpoint j
                sim.callScriptFunction("deliver_package", childscript_handle,x, "checkpoint I")
                 ## Call the deactivate_qr_code() function defined in the child script to make the QR code invisible at checkpoint J
                sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint I")

            elif(dick[node+1][1]=="M"):
                sim.setJointTargetVelocity(e,0.34)
                sim.setJointTargetVelocity(r,0.34)
                ## Retrieve the handle of the Arena_dummy scene object.
                arena_dummy_handle = sim.getObject("/Arena_dummy") 
                ## Retrieve the handle of the child script attached to the Arena_dummy scene object.
                childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
                ## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint I
                sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint M")
                str=read_qr_code(sim)
                if(str=='Orange Cone'):
                    x="package_1"
                elif(str=='Blue Cylinder'):
                    x="package_2"
                elif(str=='Pink Cuboid'):
                    x="package_3"
               
               
                ## Deliver package_3 at checkpoint I
                sim.callScriptFunction("deliver_package", childscript_handle, x, "checkpoint M")

                 ## Call the deactivate_qr_code() function defined in the child script to make the QR code invisible at checkpoint E
                sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint M")

            
            # print(dick[node+1][0])
            
            if(dick[node+1][0]=="FORWARD"):
                forward(sim,e,r)
                time.sleep(0.2)
            elif(dick[node+1][0]=="LEFT"):
                right(sim,e,r)
                time.sleep(0.31)
            elif(dick[node+1][0]=="RIGHT"):
                left(sim,e,r)  
                time.sleep(0.31)
            else:
                sim.setJointTargetVelocity(e,0.0)
                sim.setJointTargetVelocity(r,0.0)
            node+=1



        cropped_image_l= baw_image[492:512,15:35]
        cropped_image_r= baw_image[492:512,477:492]
        inside_image_l= baw_image[492:512,55:75]
        inside_image_r= baw_image[492:512,467:482]

        if((cropped_image_l==black).all() and (cropped_image_r==black).all()):
            forward(sim,e,r)
            # print("forward")
        elif((cropped_image_l==white).any() and (cropped_image_r==black).any()):
            # while(imag[35,10]==black):
            right(sim,e,r)
            # print("right")
        elif((cropped_image_l==black).any() and (cropped_image_r==white).any()):
            # while(imag[477,10]==black):
            left(sim,e,r)
            # print("left")                                                 
        else:
            sim.setJointTargetVelocity(e,0.8)
            sim.setJointTargetVelocity(r,0.8)
        # if((baw_left==black).all and (baw_right==black).all):
    
        #     sim.setJointTargetVelocity(e,0.4006)
        #     sim.setJointTargetVelocity(r,0.4)
        #     print("forward")
        # elif((baw_left==white).any and (baw_right==black).all):
    
        #     sim.setJointTargetVelocity(e,0.0)
        #     sim.setJointTargetVelocity(r,0.5)
        #     print("right")
        #     time.sleep(1)
        # # delay(100);
        

        # elif((baw_left==black).all and (baw_right==white).any):
    
        #     sim.setJointTargetVelocity(e,0.5)
        #     sim.setJointTargetVelocity(r,0)
        #     print("left")
        #     time.sleep(1)

        # else:
        #     sim.setJointTargetVelocity(e,0)
        #     sim.setJointTargetVelocity(r,0) 
        #     time.sleep(5) 

        # print("outside if loop")
        # if(baw_left!=black).any:
        #     print("Inside if")
        #     sim.setJointTargetVelocity(r,0.2)
        #     sim.setJointTargetVelocity(e,0)
        # In CoppeliaSim images are left to right (x-axis), and bottom to top (y-axis)
        # (consistent with the axes of vision sensors, pointing Z outwards, Y up)
        # and color format is RGB triplets, whereas OpenCV uses BGR:
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # print(type(image))
        # img = np.array(image, dtype=np.uint8)
        # img.resize([resolution[0], resolution[1], 3])
        # img = imutils.rotate_bound(img, 180)
                
        # cv2.startWindowThread()
        # cv2.namedWindow("image")
        # print(resX)
        # print(resY)
        # print(image)
        # cv2.imshow('left',baw_left)
        # cv2.waitKey(1)
        # cv2.imshow('right',baw_right)
        
        # print("blah")
        # cv2.imshow('output', img)
        # cv2.waitKey(1)
        # 
        # sim.stopSimulation()
        if(node==17):
            break
    sim.setJointTargetVelocity(e,0)
    sim.setJointTargetVelocity(r,0)
    # sim.stopSimulation()        
    # sim.simulation_stopped
    # triggers next simulation step




    ##################################################

def read_qr_code(sim):
    """
    Purpose:
    ---
    This function detects the QR code present in the camera's field of view and
    returns the message encoded into it.

    Input Arguments:
    ---
    `sim`    :   [ object ]
        ZeroMQ RemoteAPI object

    Returns:
    ---
    `qr_message`   :    [ string ]
        QR message retrieved from reading QR code

    Example call:
    ---
    control_logic(sim)
    """
    qr_message = None
    ##############  ADD YOUR CODE HERE  ##############
    # print('above code')
    visionSensorHandle = sim.getObject('/vision_sensor')
    image, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
    imag = np.frombuffer(image, dtype=np.uint8)
    imag=imag.reshape(resY, resX, 3)
    imag=cv2.cvtColor(imag,cv2.COLOR_BGR2RGB)
    imag=cv2.flip(imag,0)
    for qrcode in decode(imag):
        qr_message =qrcode.data.decode( 'utf-8' )
    # print("after code")    
    print('Decoded QR message :', qr_message)
    ##################################################
    return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
    
    client = RemoteAPIClient()
    sim = client.getObject('sim')	

    try:
        print('running')
        ## Start the simulation using ZeroMQ RemoteAPI
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

        ## Runs the robot navigation logic written by participants
        try:
            time.sleep(5)
            control_logic(sim)

        except Exception:
            print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
            print('Stop the CoppeliaSim simulation manually if required.\n')
            traceback.print_exc(file=sys.stdout)
            print()
            sys.exit()


        ## Stop the simulation using ZeroMQ RemoteAPI
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
        ## Stop the simulation using ZeroMQ RemoteAPI
        return_code = sim.stopSimulation()
        time.sleep(0.5)
        if sim.getSimulationState() == sim.simulation_stopped:
            print('\nSimulation interrupted by user in CoppeliaSim.')
        else:
            print('\nSimulation could not be interrupted. Stop the simulation manually .')
            sys.exit()