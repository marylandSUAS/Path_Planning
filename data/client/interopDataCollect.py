import sys
import math
import time
import os

import interop


usern = 'testuser'
passw = 'testpass'
<<<<<<< HEAD
youareL = 'http://10.0.0.5:8000'
=======
youareL = 'http://172.17.0.1:8000'
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5

# pathName = 'D:/MUAS/AutoPilot/MissionData/'


<<<<<<< HEAD
missionFileLoc = "../Mission_data.txt"

staticObjFileloc = '../static_obstacles.txt'

movingObjFileLoc = '../moving_obstacles.txt'
=======
missionFileName = "Mission_data.txt"

staticObjFileName = 'static_obstacles.txt'
staticObjFileLoc = pathName+staticObjFileName

movingObjFileName = 'moving_obstacles.txt'
movingObjFileLoc = pathName+movingObjFileName

>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5

client = interop.Client(url=youareL, username=usern, password=passw)

missions = client.get_missions()


with open(missionFileLoc,"w") as missionFile:
	missionFile.write("off_axis_target_pos")
	missionFile.write(str(' '))
<<<<<<< HEAD
	missionFile.write(str(missions[0].off_axis_odlc_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].off_axis_odlc_pos.longitude))
=======
	missionFile.write(str(missions[0].off_axis_target_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].off_axis_target_pos.longitude))
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5
	missionFile.write(str('\n'))




		

stationary_obstacles, moving_obstacles = client.get_obstacles()

<<<<<<< HEAD
with open(staticObjFileloc,"w") as staticObjFile:
=======
with open(staticObjFileLoc,"w") as staticObjFile:
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5
	for j in range(len(stationary_obstacles)):
		if(j != 0):
			staticObjFile.write('\n')
		staticObjFile.write(str(stationary_obstacles[j].latitude))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].longitude))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].cylinder_height))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].cylinder_radius))
		



timelast = time.time()
while(True):

	stationary_obstacles, moving_obstacles = client.get_obstacles()
<<<<<<< HEAD
	print(moving_obstacles)
	with open(movingObjFileLoc,"w") as movingObjFile:
		for i in range(len(moving_obstacles)):
=======

	with open(movingObjFileLoc,"w") as movingObjFile:
		for i in range(len(MovingObstacles)):
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5
			if(i != 0):
				movingObjFile.write('\n')	
			movingObjFile.write(str(moving_obstacles[i].latitude))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].longitude))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].altitude_msl))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].sphere_radius))
<<<<<<< HEAD

	
	while(time.time()-timelast < .1):
=======
	
	while(time.time()-timelast < .1)
>>>>>>> 6ecfea6f2aa884c93ff663d9577e4690691e94c5
		time.sleep(.005)
	timelast = time.time()

	