'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3A of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_3a.py
# Functions:		detect_all_nodes,detect_paths_to_graph, detect_arena_parameters, path_planning, paths_to_move
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import numpy as np
import cv2
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

dictx = {
	0: "o",
	100: "A",
	200: "B",
	300: "C",
	400: "D",
	500: "E",
	600: "F",
	700: "x"
}

dicty = {
	0: "o",
    100: "1",
    200: "2",
    300: "3",
    400: "4",
    500: "5",
    600: "6",
	700: "x"
}



##############################################################

def detect_all_nodes(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals, start_node and end_node are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals, start_node, end_node` : [ list ], str, str
			list containing nodes in which traffic signals are present, start and end node too
	
	Example call:
	---
	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	"""    
	traffic_signals = []
	start_node = ""
	end_node = ""

	##############	ADD YOUR CODE HERE	##############
	
	img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	for i in range (100,700,100):
		for j in range (100,700,100):
			if img[i,j,0] == 255 and img[i,j,1] == 0 and img[i,j,2] == 0 :
				traffic_signals.append(dictx[j]+dicty[i])
			elif img[i,j,0] == 0 and img[i,j,1] == 255 and img[i,j,2] == 0 :
				start_node += (dictx[j]+dicty[i])
			elif img[i,j,0] == 105 and img[i,j,1] == 43 and img[i,j,2] == 189 :
				end_node += (dictx[j]+dicty[i])
	traffic_signals.sort()
	# print(traffic_signals)

	##################################################

	return traffic_signals, start_node, end_node


def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	HINT: Check for the road besides the nodes for connectivity 

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`paths` : { dictionary }
			Every node's connection to other node
			Eg. : { "D3":{"C3", "E3", "D2", "D4" }, 
					"D5":{"C5", "D2", "D6" }  }
	Example call:
	---
	paths = detect_paths_to_graph(maze_image)
	"""    
	# print(image)
	paths = {}

	##############	ADD YOUR CODE HERE	##############
	
	black = np.array([0, 0, 0])

	for i in range (100,700,100):
		for j in range (100,700,100):
			nodes = {}
			if (image[int(i),int(j+50)] == black).all():
				nodes[f"{dictx[j+100]}{dicty[i]}"] = 1
			if (image[int(i),int(j-75)] == black).all():
				nodes[f"{dictx[j-100]}{dicty[i]}"] = 1
			if (image[int(i+50),int(j)] == black).all():
				nodes[f"{dictx[j]}{dicty[i+100]}"] = 1
			if (image[int(i-75),int(j)] == black).all():
				nodes[f"{dictx[j]}{dicty[i-100]}"] = 1
	
			paths[f"{dictx[j]}{dicty[i]}"] = nodes
	# print("paths:")
	# print(paths)
	##################################################

	return paths



def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

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

	Eg. arena_parameters={"traffic_signals":[], 
	                      "start_node": "E4", 
	                      "end_node":"A3", 
	                      "paths": {}}
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############

	# arena_parameters["traffic_signals"] = detect_all_nodes(image)
	l1 = list(detect_all_nodes(maze_image))
	arena_parameters["traffic_signals"] = l1[0]
	arena_parameters["start_node"] = l1[1]
	arena_parameters["end_node"] = l1[2]
	arena_parameters["paths"] = detect_paths_to_graph(maze_image)
	# print(arena_parameters)

	##################################################
	
	return arena_parameters

def path_planning(graph, start, end):

	"""
	Purpose:
	---
	This function takes the graph(dict), start and end node for planning the shortest path

	** Note: You can use any path planning algorithm for this but need to produce the path in the form of 
	list given below **

	Input Arguments:
	---
	`graph` :	[ numpy array ]
			numpy array of image returned by cv2 library
	`start` :	str
			name of start node
	`end` :		str
			name of end node


	Returns:
	---
	`backtrace_path` : [ list of nodes ]
			list of nodes, produced using path planning algorithm

		eg.: ['C6', 'C5', 'B5', 'B4', 'B3']
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    

	backtrace_path=[]

	##############	ADD YOUR CODE HERE	##############
	paths = graph
	pathlist = list(paths)
	#     print(pathlist)
	visited = list(np.zeros(36,dtype=np.int32))
	dis = [1000 for _ in range(36)]
	prev = [-1 for _ in range (36)]
	dis[pathlist.index(start)] = 0
	dist = 0
	node = start
	#     print(paths)
	# d_algo(paths,pathlist,start_node,end_node,dis,visited,dist,node)
	# print(len(paths[start_node]))
	# print(list(paths[start_node]))
	for i in range (0,36,1):
		adj_nodes = list(paths[node])
		for j in adj_nodes:
			if (dis[pathlist.index(node)]+1 < dis[pathlist.index(j)]) and visited[pathlist.index(j)]==0:
				dis[pathlist.index(j)] = dis[pathlist.index(node)]+1
				prev[pathlist.index(j)] = pathlist[pathlist.index(node)]
		visited[pathlist.index(node)] = 1
		minn = 1001
		min_in = 100
	#     adj_nodes.reverse()
		for k in range (36):
			if dis[k] < minn and visited[k] == 0:
				minn = dis[k]
				minn_in = k
		node = pathlist[minn_in]
	#     print(dis[pathlist.index(end_node)])
	prev_node = end
	backtrace_path.append(prev_node)
	while prev_node != -1:
		prev_node = prev[pathlist.index(prev_node)]
		if prev_node==-1:
			break
		backtrace_path.append(prev_node)
	backtrace_path.reverse()
		
	return backtrace_path

# parameters(img)
# param=parameters(img)
# path_plan(img,param[""],"A3")
# paths(img)
# pathlist = list(paths(img))
# print(pathlist)
# path_plan(img,param["start_node"],param["end_node"])
	##################################################


	return backtrace_path

def paths_to_moves(paths, traffic_signal):

	"""
	Purpose:
	---
	This function takes the list of all nodes produces from the path planning algorithm
	and connecting both start and end nodes

	Input Arguments:
	---
	`paths` :	[ list of all nodes ]
			list of all nodes connecting both start and end nodes (SHORTEST PATH)
	`traffic_signal` : [ list of all traffic signals ]
			list of all traffic signals
	---
	`moves` : [ list of moves from start to end nodes ]
			list containing moves for the bot to move from start to end

			Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']
	
	Example call:
	---
	moves = paths_to_moves(paths, traffic_signal)
	"""    
	
	list_moves=[]

	##############	ADD YOUR CODE HERE	##############
	face="N"
	for x in range(0, (len(paths)-1)):
		node=paths[x]
		nextnode=paths[x+1]           
		column1=node[0]
		row1=node[1]
		column2=nextnode[0]
		row2=nextnode[1]
		# print(node)
		# print(nextnode)
		
		sety1={i for i in dicty if dicty[i]==row1}
		for i in sety1:
			y1=int(i)
	#     y1 = int({i for i in dicty if dicty[i]==row1})
	#     print(y1)
		setx1 = {i for i in dictx if dictx[i]==column1}
		for i in setx1:
			x1=int(i)
	#     print(x1)
		sety2 = {i for i in dicty if dicty[i]==row2}
		for i in sety2:
			y2=int(i)
	#     print(y2)
		setx2 = {i for i in dictx if dictx[i]==column2}
		for i in setx2:
			x2=int(i)
	#     print(x2)
		if (node in traffic_signal):
				list_moves.append("WAIT_5")

		if(face=="N"):
			if (x1==x2 and y1<y2):
				list_moves.append("REVERSE")
				face="S"
			elif(x1==x2 and y1>y2):
				list_moves.append("STRAIGHT")
				face="N"
			elif(x1>x2 and y1==y2):
				list_moves.append("LEFT")
				face="W"
			elif(x1<x2 and y1==y2):
				list_moves.append("RIGHT")
				face="E"
			else:
				print("error")

		elif(face=="S"):
			if (x1==x2 and y1<y2):
				list_moves.append("STRAIGHT")
				face="S"
			elif(x1==x2 and y1>y2):
				list_moves.append("REVERSE")
				face="N"
			elif(x1>x2 and y1==y2):
				list_moves.append("RIGHT")
				face="W"
			elif(x1<x2 and y1==y2):
				list_moves.append("LEFT")
				face="E"
			else:
				print("error")

		elif(face=="E"):
			if (x1==x2 and y1<y2):
				list_moves.append("RIGHT")
				face="S"
			elif(x1==x2 and y1>y2):
				list_moves.append("LEFT")
				face="N"
			elif(x1>x2 and y1==y2):
				list_moves.append("REVERSE")
				face="W"
			elif(x1<x2 and y1==y2):
				list_moves.append("STRAIGHT")
				face="E"
			else:
				print("error")

		elif(face=="W"):
			if (x1==x2 and y1<y2):
				list_moves.append("LEFT")
				face="S"
			elif(x1==x2 and y1>y2):
				list_moves.append("RIGHT")
				face="N"
			elif(x1>x2 and y1==y2):
				list_moves.append("STRAIGHT")
				face="W"
			elif(x1<x2 and y1==y2):
				list_moves.append("REVERSE")
				face="E"
			else:
				print("error")

	##################################################

	return list_moves

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

	# # path directory of images
	img_dir_path = "test_images/"

	for file_num in range(0,10):
			
			img_key = 'maze_00' + str(file_num)
			img_file_path = img_dir_path + img_key  + '.png'
			# read image using opencv
			image = cv2.imread(img_file_path)
			
			# detect the arena parameters from the image
			arena_parameters = detect_arena_parameters(image)
			print('\n============================================')
			print("IMAGE: ", file_num)
			print(arena_parameters["start_node"], "->>> ", arena_parameters["end_node"] )

			# path planning and getting the moves
			back_path=path_planning(arena_parameters["paths"], arena_parameters["start_node"], arena_parameters["end_node"])
			moves=paths_to_moves(back_path, arena_parameters["traffic_signals"])

			print("PATH PLANNED: ", back_path)
			print("MOVES TO TAKE: ", moves)

			# display the test image
			cv2.imshow("image", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()