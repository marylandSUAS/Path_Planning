
import sys
import clr
import time
import System

clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") #includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink
MissionPlanner.MainV2.speechEnable = True




wp_file_loc = 'C:/Users/derek/Documents/Documents/MUAS/Path_Planning/2019/Path_Planning/MissionPlanner/test.txt'

file_ob = open(wp_file_loc,"r")
wp_lst = file_ob.readlines()
file_ob.close()

lst = []

for wp in wp_lst:
	dat = wp.split('\n')[0]
	dat = dat.split(' ')
	print dat


	
	cam = Locationwp()
	Locationwp.id.SetValue(cam, int(dat[1]))
	Locationwp.p1.SetValue(cam, float(dat[2]))
	Locationwp.p2.SetValue(cam, float(dat[3]))
	Locationwp.p3.SetValue(cam, float(dat[4]))
	Locationwp.p4.SetValue(cam, float(dat[5]))
	Locationwp.lat.SetValue(cam, float(dat[6]))
	Locationwp.lng.SetValue(cam, float(dat[7]))
	Locationwp.alt.SetValue(cam, float(dat[8]))
	lst.append(cam)
	





# competition
home = Locationwp().Set(38.1451066, -76.4282477, 100, 16)

# freestate
# home = Locationwp().Set(39.0828599, -76.9044766,100, 16)

# greenwell
# home = Locationwp().Set(38.3652309, -76.5365955, 100, 16)
print 'setting wps'
MAV.setWPTotal(len(lst)+1)	
MAV.setWP(home,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);


if (len(lst) != 0):
	for i in range(len(lst)):
		MAV.setWP(lst[i],1+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
		if (i+1 == 1):
			MAV.setWPCurrent(1)


print 'done setting waypoints'
# MAV.setMode("Auto")
# MAV.doARM(True)
