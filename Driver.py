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




def run(avoider object):
	Start avoider object
	Localization object
	Cord_System object
	Mission_Testing object



def monitor(avoider object)::
	Access avoider.get_current_index

def main():
	Cs = current state object
	Moving_obstacles = new Moving Obstacles Object
	run(Moving_obstacles)
	Static_info = retrieve static info
	
	Arm -> record home coords -> take off ->
	Avoider1 = new Avoider(lst3,Cs,Mav,Moving_obstacles,Static_info,home_coords)
	
		run(Avoider1)
		monitor(Avoider1)


