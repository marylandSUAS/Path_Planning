import sys
import math
import time
import os

import interop


usern = 'maryland'
passw = '6148858800'
youareL = 'http://10.10.130.10:80'



missionFileLoc = '../current_mission.txt'


client = interop.Client(url=youareL, username=usern, password=passw)

missions = client.get_missions()

stationary_obstacles = client.get_obstacles()

mission_num = 0

with open(missionFileLoc,"w") as missionFile:
	# missionFile.write("air_drop_pos")
	# missionFile.write(str(' '))
	missionFile.write(str(missions[mission_num].air_drop_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[mission_num].air_drop_pos.longitude))
	missionFile.write(str('\n'))
	
	# missionFile.write("home_pos")
	# missionFile.write(str(' '))
	# missionFile.write(str(missions[misssion_num].home_pos.latitude))
	# missionFile.write(str(' '))
	# missionFile.write(str(missions[misssion_num].home_pos.longitude))
	# missionFile.write(str(' \n'))

	# missionFile.write("off_axis_target_pos")
	# missionFile.write(str(' '))
	missionFile.write(str(missions[mission_num].off_axis_odlc_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[mission_num].off_axis_odlc_pos.longitude))
	missionFile.write(str('\n'))

	# missionFile.write("emergent_last_known_pos")
	# missionFile.write(str(' '))
	missionFile.write(str(missions[misssion_num].emergent_last_known_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[misssion_num].emergent_last_known_pos.longitude))
	missionFile.write(str(' \n'))

	for j in range(len(missions[misssion_num].mission_waypoints)):
		# MissionWPFile.write(str(missions[misssion_num].mission_waypoints[j].order))
		# MissionWPFile.write(str(' '))
		missionFile.write(str(missions[misssion_num].mission_waypoints[j].latitude))
		missionFile.write(str(' '))
		missionFile.write(str(missions[misssion_num].mission_waypoints[j].longitude))
		missionFile.write(str(' '))
		missionFile.write(str(.3048*(missions[misssion_num].mission_waypoints[j].altitude_msl)))
		missionFile.write(',')
	missionFile.write('\n')


	# with open(flyzoneFileLoc,"w") as flyzoneFile:
	# 	flyzoneFile.write("Max Altitude")
	# 	flyzoneFile.write(str('	'))
	# 	flyzoneFile.write(str(.3048*(missions[misssion_num].fly_zones[0].altitude_msl_max)))
	# 	flyzoneFile.write('\n')
	# 	flyzoneFile.write("Min Altitude")
	# 	flyzoneFile.write(str('	'))
	# 	flyzoneFile.write(str(.3048*(missions[misssion_num].fly_zones[0].altitude_msl_min)))
	# 	flyzoneFile.write('\n')

	for j in range(len(missions[misssion_num].fly_zones[0].boundary_pts)):
		missionFile.write(str(missions[misssion_num].fly_zones[0].boundary_pts[j].order))
		missionFile.write(str('	'))
		missionFile.write(str(missions[misssion_num].fly_zones[0].boundary_pts[j].latitude))
		missionFile.write(str('	'))
		missionFile.write(str(missions[misssion_num].fly_zones[0].boundary_pts[j].longitude))
		missionFile.write(',')	
	missionFile.write('\n')



	for j in range(len(missions[misssion_num].search_grid_points)):
		# missionFile.write(str(missions[misssion_num].search_grid_points[j].order))
		# missionFile.write(str(' '))
		missionFile.write(str(missions[misssion_num].search_grid_points[j].latitude))
		missionFile.write(str('	'))
		missionFile.write(str(missions[misssion_num].search_grid_points[j].longitude))
		missionFile.write(str('	'))
		missionFile.write(str(.3048*(missions[misssion_num].search_grid_points[j].altitude_msl)))
		missionFile.write(',')	
	missionFile.write('\n')


	for j in range(len(stationary_obstacles)):
			# staticObjFile.write('\n')
		missionFile.write(str(stationary_obstacles[j].latitude))
		missionFile.write(str(' '))
		missionFile.write(str(stationary_obstacles[j].longitude))
		missionFile.write(str(' '))
		missionFile.write(str(stationary_obstacles[j].cylinder_height))
		missionFile.write(str(' '))
		missionFile.write(str(stationary_obstacles[j].cylinder_radius))
		missionFile.write(',')
		


