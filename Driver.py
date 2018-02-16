import sys
import math
from math import pi,sin,cos,atan,atan2
import clr
import time
import System
from System import Byte
import threading

clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") #includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink
MissionPlanner.MainV2.speechEnable = True

import Mission_Testing
import Avoider
import Cord_System



# Driver

Tasks = ['Takeoff','Navigation','Payload','Off Axis','Search Grid','Emergent Target','Landing']



def run(avoider, Cord_System):



def monitor(avoider)::
	while(AvoiderMethod.isAlive()):
		print avoider.get_current_index
		print avoider.get_current_status
		time.sleep(.5)

def main():
	# set home position for takeoff to wherever script is started
	Home = [cs.lng,cs.lat,cs.alt]

	# initialize coordinate system
	cordSystem = Cord_System(Home)

	# create avoidance class to control vehicle during obstacle avoidance (Home,cs,MAV)
	avoider = avoidance(Home,cs,MAV,cord_System)

	# define test mission
	Missions = Mission('CASA1') 

	

	# thread this 
	AvoiderMethod = threading.Thread(target=run(avoider,cordSystem))
	AvoiderMethod.start()

	monitor(AvoiderMethod,avoider)

