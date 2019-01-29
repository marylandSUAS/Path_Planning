import math
from math import pi,sin,cos,atan,atan2
import time

import MissionPlanner
from MissionPlanner.Utilities import Locationwp
import MAVLink




# southern maryland
# droploc = [38.3652078,-76.5366331,115]
# competition
droploc = [38.145842,-76.426375,115]
dropMeters = cr.toMeters(droploc)
dropwps = payloaddropSet()
dropPlan = [True]
dropPlan.extend([False]*(len(dropwps)-1))

# southern maryland
# offAxisloc = [38.3648986,-76.5373251,0.0]
# competition
# offAxisloc = [38.1476020,-76.4272070,100]
offAxisheight = 200
offAxisDist = 250
offAxisbearing = -90 * pi/180
LookRight = -1
offAxisMeters = cord_System.toMeters(offAxisloc)
offAxiswps = offAxisSet()
offAxisPlan = [True]
offAxisPlan.extend([False]*(len(offAxiswps)-1))


# southern maryland
# emergentloc = [38.3652078,-76.5366331,50]
# competition
# emergentloc = [38.1441594,-76.4251471,50]
emergentMeters = cord_System.toMeters(emergentloc)
emergentwps = emergentwpsSet()
emergentPlan = [True]		
# emergentPlan.extend([False]*(len(emergentPlan)-1))


LandLoc = Home
landbearing = -160 * pi/180
landingwps = landSet()
landingPlan = [False]*len(landingwps)


TakeoffWps = takeoffSet()
TakeoffPlan = [False]
# takeoffPoint = []

searchGridWps = searchGridSet()
# searchGridPlan = [False]*len(searchGridWps)

printMissionMeters()
print "initalized mission functions"


	
	# done
def offAxisSet():

	dist = offAxisDist
	height = offAxisheight
	angle = atan(dist/height)

	bear = offAxisbearing
	LookRight = LookRight

	safeloc = [offAxisMeters[0]+LookRight*dist*cos(bear*pi/180),
				offAxisMeters[1]+LookRight*dist*sin(bear*pi/180),
				height]

	predist = -150
	prex = safeloc[0] + predist*cos((bear+90)*pi/180)
	prey = safeloc[1] + predist*sin((bear+90)*pi/180)

	pre = cord_System.toGPS([prex,prey,height])
	preloc = Locationwp().Set(pre[0],pre[1],height, 16)

	setangle = Locationwp()
	Locationwp.id.SetValue(setangle, 205)
	Locationwp.p2.SetValue(setangle, angle)

	offloc = cord_System.toGPS(safeloc)
	offloc = Locationwp().Set(offloc[0],offloc[1],height, 16)

	takephoto = Locationwp()
	Locationwp.id.SetValue(takephoto, 203)

	after1dist = 20
	prex = safeloc[0] + after1dist*cos((bear+90)*pi/180)
	prey = safeloc[1] + after1dist*sin((bear+90)*pi/180)
	post1 = cord_System.toGPS([prex,prey,height])
	post1 = Locationwp().Set(post1[0],post1[1],height, 16)
			
	resetangle = Locationwp()
	Locationwp.id.SetValue(resetangle, 205)
	Locationwp.p2.SetValue(resetangle, 0)

	postdist2 = 40
	prex = safeloc[0] + postdist2*cos((bear+90)*pi/180)
	prey = safeloc[1] + postdist2*sin((bear+90)*pi/180)
	post2 = cord_System.toGPS([prex,prey,height])
	postloc = Locationwp().Set(post2[0],post2[1],height, 16)

	# print 'Coordinates set with angle ',angle*180/3.1415, ' and distance ', (dist**2+height**2)**.5

	return [preloc,setangle,offloc,post1,resetangle,postloc]#,cord_System.MetertoWp(offAxisMeters)]


def payloaddropSet():
	bear = dropbearing + pi
	height = 115.0
	windbearing = 0
	windoffset  = 0

	dist = 110.0 #function of alt and vel
	
	distprevious = 250.0
	distafter = -120.0

			
	prey = dropMeters[1] + (distprevious+dist)*sin(bear)
	prex = dropMeters[0] + (distprevious+dist)*cos(bear)
	pre = [prex,prey,height]
	cr.Waypoint(16,[])
	preGPS = cord_System.toGPS(pre)
	pre = Locationwp().Set(preGPS[0],preGPS[1],preGPS[2], 16)

	posty = dropMeters[1] + (distafter+dist)*sin(bear)
	postx = dropMeters[0] + (distafter+dist)*cos(bear)
	post = [postx,posty,height]
	postGPS = cord_System.toGPS(post)
	post = Locationwp().Set(postGPS[0],postGPS[1],postGPS[2], 16)

	dropy = dropMeters[1] + dist*sin(bear)
	dropx = dropMeters[0] + dist*cos(bear)
	drop = [dropx,dropy,height]
	dropGPS = cord_System.toGPS(drop)
	drop = Locationwp().Set(dropGPS[0],dropGPS[1],dropGPS[2], 16)
	
	
	dropWP1 = Locationwp()
	Locationwp.id.SetValue(dropWP1, 183)
	Locationwp.p1.SetValue(dropWP1, 10) # servo number
	Locationwp.p2.SetValue(dropWP1, 1900) # ms

	dropWP2 = Locationwp()
	Locationwp.id.SetValue(dropWP2, 183)
	Locationwp.p1.SetValue(dropWP2, 11) # servo number
	Locationwp.p2.SetValue(dropWP2, 1100) # ms

	OpenWP1 = Locationwp()
	Locationwp.id.SetValue(OpenWP1, 183)
	Locationwp.p1.SetValue(OpenWP1, 8)
	Locationwp.p2.SetValue(OpenWP1, 950)

	OpenWP2 = Locationwp()
	Locationwp.id.SetValue(OpenWP2, 183)
	Locationwp.p1.SetValue(OpenWP2, 9)
	Locationwp.p2.SetValue(OpenWP2, 2100)

	CloseWP1 = Locationwp()
	Locationwp.id.SetValue(CloseWP1, 183)
	Locationwp.p1.SetValue(CloseWP1, 8)
	Locationwp.p2.SetValue(CloseWP1, 2100)

	CloseWP2 = Locationwp()
	Locationwp.id.SetValue(CloseWP2, 183)
	Locationwp.p1.SetValue(CloseWP2, 9)
	Locationwp.p2.SetValue(CloseWP2, 900)

	return [pre, OpenWP1, OpenWP2, drop, dropWP1, dropWP2, post, CloseWP2, CloseWP2]


def landSet():

	descent_ratio = 17.0/150.0 #20 meter descent for every 150 meters traveled

	alt1 = 150
	alt2 = 65
	alt3 = 36

	bear = landbearing

	dist1 = 800
	dist2 = 550
	dist3 = 350

	pre1 = [dist1*cos(bear),dist1*sin(bear),alt1]
	pre2 = [dist2*cos(bear),dist2*sin(bear),alt2]
	pre3 = [dist3*cos(bear),dist3*sin(bear),alt3]

	pre1 = cord_System.toGPS(pre1)
	pre2 = cord_System.toGPS(pre2)
	pre3 = cord_System.toGPS(pre3)

	pre1 = Locationwp().Set(pre1[0],pre1[1],alt1, 16)
	pre2 = Locationwp().Set(pre2[0],pre2[1],alt2, 16)
	pre3 = Locationwp().Set(pre3[0],pre3[1],alt3, 16)
	landing = Locationwp().Set(Home[0],Home[1],0,21)
	
	return [pre1,pre2,pre3,landing]
		

def searchGridSet():
	# lst = [Locationwp().Set(,,), 16)]
	lst = []


	cam = Locationwp()
	Locationwp.id.SetValue(cam, 206)
	Locationwp.p1.SetValue(cam, 40.0)
	# lst.append(cam)

	wpfileLoc = 'Path_Planning/data/SearchGridWps.waypoints'
	with open(wpfileLoc,"r") as globallist:
		
		if (globallist.readline().split()[1] != "WPL"):
			print "Nothing found"
		
		else:
			dat = globallist.readline().split()
			dat = globallist.readline().split()
			i = 1
			while(len(dat) > 5):
				if (dat[3] == '16'):
					lst.append(Locationwp().Set(float(dat[8]),float(dat[9]),200, 16))
					# print dat[10]
				dat = globallist.readline().split("	")
	
	cam = Locationwp()
	Locationwp.id.SetValue(cam, 206)
	Locationwp.p1.SetValue(cam, 0)
	# lst.append(cam)

	searchGridPlan = [True,False,True,False,True,
						False,True,False,True,False,
						True,False,True,False,False]

	# print lst
	return lst


def emergentwpsSet():
	lst = []
	lst.append(Locationwp().Set(emergentloc[0],emergentloc[1],emergentloc[2], 16))

	cam = Locationwp()
	Locationwp.id.SetValue(cam, 203)

	# lst.append(cam)
	return lst


