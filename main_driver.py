#!/usr/bin/env python

import rospy
import math
import common_resources as cr
import Avoider as av
import missionFunctions as mf





# cr.getMission()
launch = [0.0,0.0]

mission = cr.Mission()
launch = mission.toMeters(launch)

mission_prof = cr.Mission_Profile(mission)

display = cr.visual()




### compute order
display.draw_mission(mission)

mission_prof.path = [cr.Waypoint(22,[0,0,100],20)]
for wp in mission.WPs
	mission_prof.path.append(cr.Waypoint(16,wp))

drop_points = mf.calc_drop_pos(mission,20,[0,0]) # approach angle, wind params

mission_prof.path.extend(drop_points)

while True
	display.draw_mission_profile(mission_prof)	
	tweek_drop
	display
	approve

check_offAxis = mf.photo_possible(OffAxis_point,path)

check_emergent = mf.photo_possible(Emergent_point,path)

grid_points = mf.calc_grid_points(been_already, path(-1))
path.extend(grid_points)

while True	
	display 
	w/ suggested order
	set order
	check  

calculate avoidance
while not approved:
	
	tweek order
	tweek points
	calculate avoidance
	approve?



# create plane plan of action

# send to plane
# send to plane systems

# confirm ready systems

# start mission

# launch