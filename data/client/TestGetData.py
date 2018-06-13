import sys
import math
import time
#import System
#from System import Byte

#from System import Threading
#from System.Threading import Thread, ThreadStart
#import threading 

'''
clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") #includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink
MissionPlanner.MainV2.speechEnable = True
'''

import interop


client = interop.Client(url='http://127.0.0.1:8000',
                        username='testuser',
                        password='testpass')

missions = client.get_missions()

missionFile = open("Mission_data.txt","w")

missionFile.write("air_drop_pos")
missionFile.write(str('	'))
missionFile.write(str(missions.air_drop_pos.latitude))
missionFile.write(str('	'))
missionFile.write(str(missions.air_drop_pos.longitude))
missionFile.write(str('\n'))

missionFile.write("home_pos")
missionFile.write(str('	'))
missionFile.write(str(missions.home_pos.latitude))
missionFile.write(str('	'))
missionFile.write(str(missions.home_pos.longitude))
missionFile.write(str('\n'))

missionFile.write("off_axis_target_pos")
missionFile.write(str('	'))
missionFile.write(str(missions.off_axis_target_pos.latitude))
missionFile.write(str('	'))
missionFile.write(str(missions.off_axis_target_pos.longitude))
missionFile.write(str('\n'))

missionFile.write("emergent_last_known_pos")
missionFile.write(str('	'))
missionFile.write(str(missions.emergent_last_known_pos.latitude))
missionFile.write(str('	'))
missionFile.write(str(missions.emergent_last_known_pos.longitude))
missionFile.write(str('\n'))
missionFile.close()

MissionWPFile = open("Mission_WP.txt","w")
for j in range(len(missions.mission_waypoints)):
	MissionWPFile.write(str(missions.mission_waypoints[j].order))
	MissionWPFile.write(str('	'))
	MissionWPFile.write(str(missions.mission_waypoints[j].latitude))
	MissionWPFile.write(str('	'))
	MissionWPFile.write(str(missions.mission_waypoints[j].longitude))
	MissionWPFile.write(str('	'))
	MissionWPFile.write(str(missions.mission_waypoints[j].altitude_msl))
	MissionWPFile.write('\n')
MissionWPFile.close()

searchGridFile = open("search_grid.txt","w")
for j in range(len(missions.search_grid_points)):
	searchGridFile.write(str(missions.search_grid_points[j].order))
	searchGridFile.write(str('	'))
	searchGridFile.write(str(missions.search_grid_points[j].latitude))
	searchGridFile.write(str('	'))
	searchGridFile.write(str(missions.search_grid_points[j].longitude))
	searchGridFile.write(str('	'))
	searchGridFile.write(str(missions.search_grid_points[j].altitude_msl))
	searchGridFile.write('\n')
searchGridFile.close()

flyzoneFile = open("fly_zones.txt","w")
flyzoneFile.write("Max Altitude")
flyzoneFile.write(str('	'))
flyzoneFile.write(str(missions.fly_zones.altitude_msl_max))
flyzoneFile.write('\n')
flyzoneFile.write("Min Altitude")
flyzoneFile.write(str('	'))
flyzoneFile.write(str(missions.fly_zones.altitude_msl_min))
flyzoneFile.write('\n')

for j in range(len(missions.fly_zones.boundary_pts)):
	flyzoneFile.write(str(missions.fly_zones.boundary_pts[j].order))
	flyzoneFile.write(str('	'))
	flyzoneFile.write(str(missions.fly_zones.boundary_pts[j].latitude))
	flyzoneFile.write(str('	'))
	flyzoneFile.write(str(missions.fly_zones.boundary_pts[j].longitude))
	flyzoneFile.write('\n')
flyzoneFile.close()


stationary_obstacles, moving_obstacles = client.get_obstacles()
staticObjFile = open("static_obstacle_data.txt","w")
for j in range(len(stationary_obstacles)):
	staticObjFile.write(str(j+1))
	staticObjFile.write(str('	'))
	staticObjFile.write(str(stationary_obstacles[j].latitude))
	staticObjFile.write(str('	'))
	staticObjFile.write(str(stationary_obstacles[j].longitude))
	staticObjFile.write(str('	'))
	staticObjFile.write(str(stationary_obstacles[j].cylinder_height))
	staticObjFile.write(str('	'))
	staticObjFile.write(str(stationary_obstacles[j].cylinder_radius))
	staticObjFile.write('\n')
staticObjFile.close()

def updateMovingObstacles():
	pass
	return None

def postTel(interop,client):
	Telfile = open("current_state.txt","r")
	lat = Telfile.readline()
	lng = Telfile.readline()
	alt = Telfile.readline()
	bear = Telfile.readline()
	telemetry = interop.Telemetry(latitude=lat,
                             longitude=lng,
                             altitude_msl=alt,
                             uas_heading=bear)
	client.post_telemetry(telemetry)

def postimage():
	target = interop.Target(type='test',
                      latitude=38.145215,
                      longitude=-76.427942,
                      orientation='n',
                      shape='square',
                      background_color='green',
                      alphanumeric='A',
                      alphanumeric_color='white')
	target = client.post_target(target)

	#with open('path/to/image/A.jpg', 'rb') as f:
   	#	image_data = f.read()
   	#	client.put_target_image(target.id, image_data)

class obMoving():
	def __init__(self):
		self.dlat = 0
		self.dlng = 0
		self.dalt = 0
		avglat = [0,0,0]
		avglng = [0,0,0]
		avgalt = [0,0,0]

	def update(self,latitude,longitude,altitude):
		self.avglat[0] = self.avglat[1]
		self.avglat[1] = self.avglat[2]
		self.avglat[0] = latitude
		self.dlat = (self.avglat[1]-self.avglat[0])+(self.avglat[2]-self.avglat[1])

		self.avglng[0] = self.avglng[1]
		self.avglng[1] = self.avglng[2]
		self.avglng[0] = longitude
		self.dlng = (self.avglng[0]-self.avglng[1])+(self.avglng[2]-self.avglng[1])

		self.avgalt[0] = self.avgalt[1]
		self.avgalt[1] = self.avgalt[2]
		self.avgalt[0] = altitude
		self.dalt = (self.avgalt[0]-self.avgalt[1])+(self.avgalt[2]-self.avgalt[1])

MovingObstacles = []
for i in range(len(moving_obstacles)):
	MovingObstacles.append(obMoving())

count = 1
while(True):
	
	postTel(interop,client)

	if (count % 2 == 0):
		stationary_obstacles, moving_obstacles = client.get_obstacles()
		movingObjFile = open("moving_obstacle_data.txt","w")

		for i in range(len(MovingOstacles)):
			MovingOstacles[i].update(moving_obstacles[i].latitude,moving_obstacles[i].longitude,moving_obstacles[i].altitude_msl)
			movingObjFile.write(str(i+1))
			movingObjFile.write(str('	'))
			movingObjFile.write(str(moving_obstacles[i].latitude))
			movingObjFile.write(str('	'))
			movingObjFile.write(str(moving_obstacles[i].longitude))
			movingObjFile.write(str('	'))
			movingObjFile.write(str(moving_obstacles[i].altitude_msl))
			movingObjFile.write(str('	'))
			movingObjFile.write(str(moving_obstacles[i].sphere_raduis))
			movingObjFile.write(str('	'))
			movingObjFile.write(str(MovingOstacles[i].dlat))
			movingObjFile.write(str('	'))
			movingObjFile.write(str(MovingOstacles[i].dlng))
			movingObjFile.write(str('	'))
			movingObjFile.write(str(MovingOstacles[i].dalt))
			movingObjFile.write('\n')

		movingObjFile.close()

	count += 1
	if(count == 5):
		count = 1
	time.sleep(.25)