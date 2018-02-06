import sys
import math
import time
import os

import interop
import threading

global pathName
global ImageInfoLoc
global ImageLoc

usern = 'testuser'
passw = 'testpass'
youareL = 'http://172.17.0.1:8000'
pathName = 'D:/MUAS/AutoPilot/MissionData/'

ImageInfoLoc = 'D:/MUAS/Imaging/Info.txt'
ImageLoc = 'D:/MUAS/Imaging/Yes/'
global NumberSubmitted
NumberSubmitted = 0
with open(ImageInfoLoc,"w") as file:
	file.write('0')


missionFileName = "Mission_data.txt"
missionFileLoc = os.path.join(pathName,missionFileName)

TelmFileName = 'current_state.txt'
TelmFileLoc = os.path.join(pathName,TelmFileName)

staticObjFileName = 'static_obstacle_data.txt'
staticObjFileLoc = os.path.join(pathName,staticObjFileName)

movingObjFileName = 'moving_obstacle_data.txt'
movingObjFileLoc = os.path.join(pathName,movingObjFileName)


client = interop.Client(url=youareL, username=usern, password=passw)

missions = client.get_missions()


with open(missionFileLoc,"w") as missionFile:
	missionFile.write("air_drop_pos")
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].air_drop_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].air_drop_pos.longitude))
	missionFile.write(str('\n'))
	
	missionFile.write("home_pos")
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].home_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].home_pos.longitude))
	missionFile.write(str('\n'))

	missionFile.write("off_axis_target_pos")
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].off_axis_target_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].off_axis_target_pos.longitude))
	missionFile.write(str('\n'))

	missionFile.write("emergent_last_known_pos")
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].emergent_last_known_pos.latitude))
	missionFile.write(str(' '))
	missionFile.write(str(missions[0].emergent_last_known_pos.longitude))
	missionFile.write(str('\n'))


		

stationary_obstacles, moving_obstacles = client.get_obstacles()

with open(staticObjFileLoc,"w") as staticObjFile:
	for j in range(len(stationary_obstacles)):
		staticObjFile.write(str(j+1))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].latitude))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].longitude))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].cylinder_height))
		staticObjFile.write(str(' '))
		staticObjFile.write(str(stationary_obstacles[j].cylinder_radius))
		staticObjFile.write('\n')


def postTel(interop,client,TelmFileLoc,count):
	with open(TelmFileLoc,"r") as Telfile:
		lat = Telfile.readline()
		lng = Telfile.readline()
		alt = Telfile.readline()
		bear = Telfile.readline()
	lat = 38.1427925
	lng = -76.4312732+count/1000
	alt = 100
	bear = 180
	telemetry = interop.Telemetry(latitude=lat,
                             longitude=lng,
                             altitude_msl=alt,
                             uas_heading=bear)
	client.post_telemetry(telemetry)

def newImage():
	with open(ImageInfoLoc,"r") as file:
		num = float(file.readline())
		if(num == NumberSubmitted)
			return False
		else:
			return num

def postimage(num):
	SubmissionText = os.path.join(ImageLoc,str(num),'.txt')
	SubmissionImage = os.path.join(ImageLoc,str(num),'.jpg')

	with open(ImageInfoLoc,"r") as file: 
		alpha = file.readline()
		alphaColor = file.readline()
		shape = file.readline()
		backColor = file.readline()
		targetType = file.readline()
		lat = float(file.readline())
		lng = float(file.readline())
		deg = float(file.readline())

	if (deg > 180):
		deg = deg-360
	elif(deg < -180):
		deg = deg+360

	if (deg > 157.5):
		orient = 's'
	elif(deg <= 157.5 and deg > 112.5):
		orient = 'sw'
	elif(deg <= 112.5 and deg > 67.5):
		orient = 'w'
	elif(deg <= 67.5 and deg > 22.5):
		orient = 'nw'
	elif(deg <= 22.5 and deg > -22.5):
		orient = 'n'
	elif(deg <= -22.5 and deg > -67.5):
		orient = 'ne'
	elif(deg <= -67.5 and deg > -112.5):
		orient = 'e'
	elif(deg <= -112.5 and deg > -157):
		orient = 'se'
	else:
		orient = 's'


	target = interop.Target(type=targetType,
		latitude=lat,
		longitude=lng,
		orientation=orient,
		shape=shape,
		background_color=backColor,
		alphanumeric=alpha,
		alphanumeric_color=alphaColor)

	target = client.post_target(target)

	with open(SubmissionImage, 'rb') as f:
   		image_data = f.read()
   		client.put_target_image(target.id, image_data)


class obMoving():
	def __init__(self):
		self.dlat = 0
		self.dlng = 0
		self.dalt = 0
		self.avglat = [0,0,0,0,0]
		self.avglng = [0,0,0,0,0]
		self.avgalt = [0,0,0,0,0]

	def update(self,latitude,longitude,altitude):
		self.avglat[0] = self.avglat[1]
		self.avglat[1] = self.avglat[2]
		self.avglat[2] = self.avglat[3]
		self.avglat[3] = self.avglat[4]
		self.avglat[4] = latitude
		self.dlat = ((self.avglat[1]-self.avglat[0])+(self.avglat[2]-self.avglat[1])+(self.avglat[3]-self.avglat[2])+(self.avglat[4]-self.avglat[3]))/.00000899

		self.avglng[0] = self.avglng[1]
		self.avglng[1] = self.avglng[2]
		self.avglng[2] = self.avglng[3]
		self.avglng[3] = self.avglng[4]
		self.avglng[4] = longitude
		self.dlng = ((self.avglng[0]-self.avglng[1])+(self.avglng[2]-self.avglng[1])+(self.avglng[3]-self.avglng[2])+(self.avglng[4]-self.avglng[3]))/.0000116

		self.avgalt[0] = self.avgalt[1]
		self.avgalt[1] = self.avgalt[2]
		self.avgalt[2] = self.avgalt[3]
		self.avgalt[3] = self.avgalt[4]
		self.avgalt[4] = altitude
		self.dalt = (self.avgalt[0]-self.avgalt[1])+(self.avgalt[2]-self.avgalt[1])+(self.avgalt[3]-self.avgalt[2])+(self.avgalt[4]-self.avgalt[3])

MovingObstacles = []
for i in range(len(moving_obstacles)):
	MovingObstacles.append(obMoving())


count = 1
while(True):
	
	#posting Telemetry
	#postTel(interop,client,count)

	#Posting Targets
	if (count % 4 == 0):
		num = newImage()

		if (num != False)
			postimage(num)
			NumberSubmitted = num

	#updating moving obstacles
	#if (count % 1 == 0):
	stationary_obstacles, moving_obstacles = client.get_obstacles()
	with open(movingObjFileLoc,"w") as movingObjFile:

		for i in range(len(MovingObstacles)):

			MovingObstacles[i].update(moving_obstacles[i].latitude,moving_obstacles[i].longitude,.3048*(moving_obstacles[i].altitude_msl))

			movingObjFile.write(str(i+1))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].latitude))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].longitude))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].altitude_msl))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(moving_obstacles[i].sphere_radius))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(MovingObstacles[i].dlat))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(MovingObstacles[i].dlng))
			movingObjFile.write(str(' '))
			movingObjFile.write(str(MovingObstacles[i].dalt))
			movingObjFile.write('\n')
			print (MovingObstacles[i].dlat/.00000899,'	',MovingObstacles[i].dlng/.0000116,'	',MovingObstacles[i].dalt)


	count += 1
	if(count == 5):
		count = 1
	time.sleep(.25)
