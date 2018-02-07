import sys
import math
from math import pi,sin,cos,atan,atan2
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

import Localization
import Mission_Testing
import Avoider
import Cord_System



# Driver

Tasks = ['Takeoff','Navigation','Payload','Off Axis','Search Grid','Emergent Target','Landing']



def run(avoider, Cord_System):
	Start avoider object


def monitor(avoider)::
	avoider.get_current_index
	avoider.get_current_status


def main():
	Home = [cs.lng,cs.lat,cs.alt]
	# create avoidance class to control vehicle during obstacle avoidance (Home,cs,MAV)
	cordSystem = Cord_System(Home)
	avoider = avoidance(Home,cs,MAV,cord_System)
	Missions = Mission('CASA1') 

	

	# Arm -> record home coords -> take off ->


	avoider.Moving_obstacles.run()
	monitor(Avoider1)

