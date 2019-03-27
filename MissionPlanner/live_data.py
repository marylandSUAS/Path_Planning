
#import math
#from math import pi,sin,cos,atan,atan2
import clr
import time
import System
from System import Byte




clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") #includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink
MissionPlanner.MainV2.speechEnable = True

print 'imported all'

def speak(strin):
	print strin
	MissionPlanner.MainV2.speechEngine.SpeakAsync(strin)


data_file = 'C:/Users/derek/Documents/Documents/MUAS/Path_Planning/2019/Path_Planning/MissionPlanner/LiveData.txt'


temp = 0
while True:
	with open(data_file,'w') as write_file:
		write_file.write(str(cs.lat))
		write_file.write(' ')
		write_file.write(str(cs.lng))
		write_file.write(' ')
		write_file.write(str(cs.alt))
		write_file.write(' ')
		write_file.write(str(cs.yaw))
		write_file.write(' ')
		write_file.write(str(cs.wpno))
		write_file.write(' ')
		write_file.write(str(cs.timeInAir))
	Script.Sleep(500)
	print 'Printed: ',temp
	temp += 1
	if temp > 9:
		temp = 0

'''
cs.lat
cs.lng
cs.alt
cs.nav_bearing
cs.nav_roll
cs.nav_pitch
cs.wpno #current waypoint number
cs.satcount
cs.gpshdop
cs.mode
cs.wp_dist
cs.DistToHome
cs.timeInAir
cs.distTraveled
cs.climbrate
cs.landed
cs.connected
cs.messages
cs.messages.Clear
'''