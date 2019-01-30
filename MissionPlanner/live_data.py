
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



def speak(strin):
	print strin
	MissionPlanner.MainV2.speechEngine.SpeakAsync(strin)


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