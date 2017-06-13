import sys
import math
from math import pi,sin,cos,atan,atan2
import clr
import time
import System
from System import Byte

sys.path.append('C:\Program Files\IronPython 2.7\lib')
#import os
#import threading

#from System import Threading
#from System.Threading import Thread, ThreadStart
#import threading
#import os

clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") #includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink
MissionPlanner.MainV2.speechEnable = True


global groundBearing
global givenTime
global loiterRadius
global Dstar
global bounds
global staticObstacles
global OffAxisLtoR

global delLat
global delLng

OffAxisLtoR = 1
delLat = .00000898
delLng = .0000115
givenTime = 2
loiterRadius = 40
#setparam loiter radius to loiterRadius

def gps_distanceCS(lat, lng):
	dist = (((lat-cs.lat)*delLat)**2+((lng-cs.lng)*delLng)**2)
	return (dist**(1/2.0))

def dist_CS(loc):
	dlat = (loc.lat-cs.lat)/delLat
	dlng = (loc.lng-cs.lng)/delLng
	dalt = loc.alt-cs.alt
	dist = ((dlat)**2+(dlng)**2+(dalt)**2)**.5
	return dist

def gps_distance(lat1,lng1,lat2,lng2):
	dist = (((lat2-lat1)/delLat)**2+((lng2-lng1)/delLng)**2)**.5
	return dist

def dist_loc(loc1,loc2):
	dlat = (loc2.lat-loc1.lat)/delLat
	dlng = (loc2.lng-loc1.lng)/delLng
	dalt = loc2.alt-loc1.alt
	dist = ((dlat)**2+(dlng)**2+(dalt)**2)**.5
	return dist

def gpsDist(m):
	dist = (m/10)*.0001
	return dist
    
def meters(gps):
	dist = gps/.00001
	return dist

def file_len(fname):
    i = 0
    file = open(fname,"r")
    for line in file:
    	i += 1
    file.close()
    print "file length is ", i
    return i

def file_len_Loc(fileLoc):
    i = 0
    with open(fileLoc,"r") as file:
	    for line in file:
	    	i += 1
    #print "file length is ", i
    return i

def defineHome():
	global Dstar
	Dstar = Dstar()
	global groundBearing
	groundBearing = cs.nav_bearing*(3.1415/180)
	print "ground bearing is ",groundBearing, " at location ",Dstar.Home.lat,", ", Dstar.Home.lng

def setHome(num):
	MAV.setWPTotal(num)	
	MAV.setWP(Dstar.Home,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);

def closestPoint(gl, st, ob):
	#gl = [goal.lat,goal.lng,goal.alt]
	#st = [start.lat,start.lng,goal.alt]
	lin = [gl[0]-st[0],gl[1]-st[1],gl[2]-st[2]]
	length = ((lin[0])**2+(lin[1])**2+(lin[2])**2)**.5
	ln = [lin[0]/length,lin[1]/length,lin[2]/length]
	t = (((ob[0]-st[0])*ln[0])+((ob[1]-st[1])*ln[1])+(ln[2]*(ob[2]-st[2])))/(ln[0]**2+ln[1]**2+ln[2]**2)
	if (t < 0):
		t = 0
	elif(t > length):
		t = length;
	cp = [st[0]+ln[0]*t,st[1]+ln[1]*t,st[2]+ln[2]*t]
	close = [cp[0],cp[1],cp[2]]#Locationwp().Set(cp[0],cp[1],cp[2], 16)
	return close

def distFromPath(gl, st, ob):
	cp = closestPoint(gl, st, ob)
	d = ((ob[0]-cp[0])**2+(ob[1]-cp[1])**2+(ob[2]-cp[2])**2)**.5
	return d

def speak(strin):
	print strin
	MissionPlanner.MainV2.speechEngine.SpeakAsync(strin)

def readWpFile(wpfilename):
	globallist = open(wpfilename,"r")
	lngth = file_len(wpfilename)
	lst = []
	if (globallist.readline().split(" ")[1] == "WPL"):
		globallist.readline()
		for wpnum in range(lngth-2):
			dat = globallist.readline().split("	")
			cam = Locationwp()
			Locationwp.id.SetValue(cam, int(dat[3]))
			Locationwp.p1.SetValue(cam, float(dat[4]))
			Locationwp.p2.SetValue(cam, float(dat[5]))
			Locationwp.p3.SetValue(cam, float(dat[6]))
			Locationwp.p4.SetValue(cam, float(dat[7]))
			Locationwp.lat.SetValue(cam, float(dat[8]))
			Locationwp.lng.SetValue(cam, float(dat[9]))
			Locationwp.alt.SetValue(cam, float(dat[10]))
			lst.append(cam)  #append cam trig
	else:
		print "Nothing found"
	globallist.close()
	return lst

def readNodeFile(nodefilename):
	Nodelist = open(nodefilename,"r")
	lngth = file_len(nodefilename)
	lst = []
	globallist.readline()
	for wpnum in range(lngth-1):

		dat = globallist.readline().split("	")
		lst.append(dat)  #append cam trig

	globallist.close()
	return lst

def cameraGrid(wpfileLoc):
	lngth = file_len_Loc(wpfileLoc)
	with open(wpfileLoc,"r") as globallist:
		lst = []
		if (globallist.readline().split(" ")[1] != "WPL"):
			print "Nothing found"
		else:
			globallist.readline()
			i = 0
			for wpnum in range(lngth-2):
				dat = globallist.readline().split("	")
				print dat[3]
				if (int(dat[3]) == 16):
					print "16"
					print dat[8],dat[9],dat[10]
					lst.append(Locationwp().Set(float(dat[8]),float(dat[9]),float(dat[10]), 16))
				elif(int(dat[3]) == 203):
					print "203"
					cam = Locationwp()
					Locationwp.id.SetValue(cam, 203)
					Locationwp.p1.SetValue(cam, float(dat[4]))
					Locationwp.p2.SetValue(cam, float(dat[5]))
					Locationwp.p3.SetValue(cam, float(dat[6]))
					Locationwp.p4.SetValue(cam, float(dat[7]))
					Locationwp.lat.SetValue(cam, float(dat[8]))
					Locationwp.lng.SetValue(cam, float(dat[9]))
					Locationwp.alt.SetValue(cam, float(dat[10]))
					lst.append(cam)  #append cam trig

				elif(int(dat[3]) == 206):
					print "206"
					cam = Locationwp()
					Locationwp.id.SetValue(cam, 206)
					Locationwp.p1.SetValue(cam, float(dat[4]))
					Locationwp.p2.SetValue(cam, float(dat[5]))
					Locationwp.p3.SetValue(cam, float(dat[6]))
					Locationwp.p4.SetValue(cam, float(dat[7]))
					Locationwp.lat.SetValue(cam, float(dat[8]))
					Locationwp.lng.SetValue(cam, float(dat[9]))
					Locationwp.alt.SetValue(cam, float(dat[10]))
					lst.append(cam)  #append cam trig

					print dat[4], dat[8]
				else:
					print "was not 16, 206, or 203"
				i = wpnum
		print "number of waypoints are", len(lst)

		#end it here and return the list
		writePhotoLocations(lst)
		return lst
		
		#uploadWp(lst)
		#print "about to write"
		

	#while (cs.wpno < len(lst)-1):
	#	print ((len(lst)-1)-cs.wpno)
	#	Script.Sleep(100)
		
	#return None

def getBear(loc,lastloc):
	dlat = (loc.lat-lastloc.lat)/delLat
	dlng = (loc.lng-lastloc.lng)/delLng
	return atan2(dlng,dlat)

def writePhotoLocations(lst):
	# file_loc = 'C:\Users\derek_000\Documents\Documents\MUAS\Imaging\Picture_Info.txt';
	file_loc = 'D:\MUAS\Imaging\Picture_Info.txt';

	locList = []
	lastLoc = lst[0]
	lastlastLoc = None
	for i in range(len(lst)):
		print i
		if (lst[i].id == 203 or lst[i].id == 206):
			loca = [lst[i-1].lat,lst[i-1].lng]
			loca.append(getBear(lastLoc,lastlastLoc))
			locList.append(loca)
		elif(lst[i].id == 16):
			lastlastLoc = lastLoc
			lastLoc = lst[i]

	with open(file_loc,"w") as locFile:
		for j in range(len(locList)):
			locFile.write(str(j+1))
			locFile.write(str('	'))
			locFile.write(str(loca[0]))
			locFile.write(str('	'))
			locFile.write(str(loca[1]))
			locFile.write(str('	'))
			locFile.write(str(loca[2]))
			locFile.write('\n')
	print 'done writing photo locations file'

def takeoff():
	to = Locationwp()
	Locationwp.id.SetValue(to, int(MAVLink.MAV_CMD.TAKEOFF))
	Locationwp.p1.SetValue(to, 15)
	Locationwp.alt.SetValue(to, 40)
	return [to]

def getTakeoffLoc(loc,bear):
	dist = 310
	lat1 = loc.lat + delLat*dist*sin(bear)
	lng1 = loc.lng + delLng*dist*cos(bear)
 
	loc = Locationwp().Set(lat1,lng1,50, 16)

def landLoc(loc,bear):
	descent_ratio = 20.0/150.0 #20 meter descent for every 150 meters traveled
	alt1 = 60
	alt2 = 50
	dist1 = gpsDist(alt1/descent_ratio)
	dist2 = gpsDist(alt2/descent_ratio)
	lat1 = loc.lat - dist1*sin(bear)
	lng1 = loc.lng - dist1*cos(bear)
	lat2 = loc.lat - dist2*sin(bear)
	lng2 = loc.lng - dist2*cos(bear)

	loc1 = Locationwp().Set(lat1,lng1,alt1, 16)
	loc2 = Locationwp().Set(lat2,lng2,alt1, 16)
	loc3 = Locationwp().Set(loc.lat,loc.lng,0,21)
	return [loc1, loc2, loc3]

def land():
	descent_ratio = 20.0/150.0 #20 meter descent for every 150 meters traveled
	alt1 = 60
	alt2 = 50
	dist1 = gpsDist(alt1/descent_ratio)
	dist2 = gpsDist(alt2/descent_ratio)
	lat1 = Dstar.Home.lat - dist1*sin(groundBearing)
	lng1 = Dstar.Home.lng - dist1*cos(groundBearing)
	lat2 = Dstar.Home.lat - dist2*sin(groundBearing)
	lng2 = Dstar.Home.lng - dist2*cos(groundBearing)

	return [Locationwp().Set(lat1,lng1,alt1, 16), Locationwp().Set(lat2,lng2,alt1, 16), Locationwp().Set(Dstar.Home.lat,Dstar.Home.lng,0,21)]

def payloaddrop(loc, bear):
	
	dist = 20 #function of alt and vel
	windoffset  = 0
	wind = gpsDist(windoffset)
	windbearing = 0

	dropAlt = 50
	vel = 16


	dist1 = gpsDist(dist)

	droplat = loc.lat - dist1*sin(bear) - wind*sin(windbearing)
	droplng = loc.lng - dist1*cos(bear) - wind*cos(windbearing)

	distprevious1 = gpsDist(220)
	prelat1 = loc.lat - distprevious1*sin(bear) - wind*sin(windbearing)
	prelng1 = loc.lng - distprevious1*cos(bear) - wind*cos(windbearing)

	distprevious2 = gpsDist(80)
	prelat2 = loc.lat - distprevious2*sin(bear) - wind*sin(windbearing)
	prelng2 = loc.lng - distprevious2*cos(bear) - wind*cos(windbearing)

	distafter = gpsDist(50)
	postlat = loc.lat + distafter*sin(bear) - wind*sin(windbearing)
	postlng = loc.lng + distafter*cos(bear) -  wind*cos(windbearing)

	#speak("setting up payload drop")
	#setHome(50)
	
	loc1 = Locationwp().Set(prelat1,prelng1,50, 16)
	#MAV.setWPCurrent(1)
	loc2 = Locationwp().Set(prelat2,prelng2,50, 16)
	loc3 = Locationwp().Set(droplat,droplng,50, 16)

	dropWP = Locationwp()
	Locationwp.id.SetValue(dropWP, 183)
	Locationwp.p1.SetValue(dropWP, 5)
	Locationwp.p2.SetValue(dropWP, 1100)

	loc5 = Locationwp().Set(postlat,postlng,50, 16)

	return [loc1, loc2, loc3, dropWP, loc5]
	'''
	while (cs.wpno < 3):
		print "dist to drop point is ",meters(gps_distanceCS(dropspot.lat,dropspot.lng))
		Script.Sleep(100)
	speak("Bombs Away")
	while (cs.wpno < 5):
		pass
		Script.Sleep(100)		
	'''

def uploadWp(lst,start):
	if (len(lst) != 0):
		if (start == 1):
			setHome(len(lst)+1)
			for i in range(len(lst)):
				MAV.setWP(lst[i],1+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
				if (i+1 == 1):
					MAV.setWPCurrent(1)
		else:
			for i in range(len(lst)):
				MAV.setWP(lst[i],start+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)

	MAV.setMode("Auto")


##### Getting Mission Stuff

def getMissionData(missionFileLoc):
	with open(missionFileLoc,"r") as missionFile:
		airdropData = missionFile.readline().split(" ")
		homeData = missionFile.readline().split(" ")
		offaxisData = missionFile.readline().split(" ")
		emergentData = missionFile.readline().split(" ")
		
		airdropLoc = Locationwp().Set(float(airdropData[1]),float(airdropData[2]),0, 16)
		homeLoc = Locationwp().Set(float(homeData[1]),float(homeData[2]),0, 16)
		offaxistagetLoc = Locationwp().Set(float(offaxisData[1]),float(offaxisData[2]),0, 16)
		emergentLoc = Locationwp().Set(float(emergentData[1]),float(emergentData[2]),0, 16)
	return airdropLoc, homeLoc, offaxistagetLoc, emergentLoc

def getWPData(WPFileLoc):
	length = file_len_Loc(WPFileLoc)
	WPs = []
	with open(WPFileLoc,"r") as WPFile:
		for i in range(length):
			WPdat = WPFile.readline().split(" ")
			WPs.append(Locationwp().Set(float(WPdat[1]),float(WPdat[2]),float(WPdat[3]), 16))
	return WPs

def getBoundryData(BoundFileLoc):
	length = file_len_Loc(BoundFileLoc)
	bounds = []
	with open(WPFileLoc,"r") as BoundFile:
		BoundFile.readline()
		BoundFile.readline()
		for i in range(length-2):
			WPdat = BoundFile.readline().split(" ")
			bounds.append(Locationwp().Set(float(WPdat[1]),float(WPdat[2]),float(WPdat[3]), 16))
	return bounds

##### off axis stuff

def findclosestboundries(loc, bnd):
	ob = [loc.lng, loc.lat, 0]
	st = [bnd[0].lng, bnd[0].lat, 0]
	gl = [bnd[len(bnd)-1].lng, bnd[len(bnd)-1].lat, 0]
	print '1'
	dist = distFromPath(gl, st, ob)
	Bound1 = bnd[0]
	Bound2 = bnd[len(bnd)-1]
	print '2'
	for i in range(len(bnd)-1):
		st = [bnd[i].lng, bnd[i].lat, 0]
		gl = [bnd[i+1].lng, bnd[i+1].lat, 0]
		distTemp = distFromPath(gl, st, ob)
		print '3'
		if (distTemp < dist):
			dist = distTemp
			Bound1 = bnd[i]
			Bound2 = bnd[i+1]
			print '4'
	return Bound1, Bound2

def findSafeOffAxisLoc(boundry1,boundry2,loc):
	DistFromLine = 75
	gl = [boundry2.lng,boundry2.lat,0]
	st = [boundry1.lng,boundry1.lat,0]
	ob = [loc.lng,loc.lat,0]
	clpoint = closestPoint(gl,st,ob)
	dist = gps_distance(clpoint[1],clpoint[0],ob[1],ob[0])
	
	lat = clpoint[1] + (clpoint[1]-loc.lat)*(DistFromLine/dist)
	lng = clpoint[0] + (clpoint[0]-loc.lng)*(DistFromLine/dist)
	height = 50+125*(dist/75)
	safeloc = Locationwp().Set(lat,lng,height, 16)
	return safeloc

def offaxistarget(loc):
	boundry1,boundry2 = findclosestboundries(loc,bounds)

	safeloc = findSafeOffAxisLoc(boundry1,boundry2,loc)
	
	#negative 1 if want to go RtoL
	LtoR = OffAxisLtoR

	dist = (((safeloc.lat-loc.lat)/delLat)**2 + ((safeloc.lng-loc.lng)/delLng)**2)**.5
	#height = safeloc.alt
	height = 50
	print height
	print 'dist = ',dist,' height = ',height
	angle = atan(dist/height)
	print 'angle at ',angle,' degrees'
	
	dlat = (loc.lat - safeloc.lat)/delLat
	dlng = (loc.lng - safeloc.lng)/delLng
	phi = atan2(dlat,dlng)

	direc = phi+.5*pi*LtoR

	predist1 = -220
	latPre1 = safeloc.lat + (predist1*sin(direc))*delLat
	lngPre1 = safeloc.lng + (predist1*cos(direc))*delLng
	preOff1 = Locationwp().Set(latPre1,lngPre1,height, 16)
	
	print 'setting gimbal to ',angle*180/pi
	setangle = Locationwp()
	Locationwp.id.SetValue(setangle, 205)
	Locationwp.p2.SetValue(setangle, angle)


	predist2 = -80
	latPre2 = safeloc.lat + (predist2*sin(direc))*delLat
	lngPre2 = safeloc.lng + (predist2*cos(direc))*delLng
	preOff2 = Locationwp().Set(latPre2,lngPre2,height, 16)
	
	print 'camera trigger'
	takephoto = Locationwp()
	Locationwp.id.SetValue(takephoto, 206)

	afterDist = 40
	lataft = safeloc.lat + (afterDist*sin(direc))*delLat
	lngaft = safeloc.lng + (afterDist*cos(direc))*delLng
	afterOff = Locationwp().Set(lataft,lngaft,height, 16)
	
	print 'reseting gimbal'
	resetangle = Locationwp()
	Locationwp.id.SetValue(resetangle, 205)
	Locationwp.p2.SetValue(resetangle, 0)
	

	return [preOff1,preOff2,setangle,safeloc,takephoto,afterOff,resetangle]

##### path definition

# need to know if intwps returns the goalwp too
def getPath(loc,loc2,Moving,timeout):
	if (Moving == False):


		Dstar.startSenario(loc,loc2,Moving)
		timestart = time.clock()
		done = False
		while((time.clock()-timeStart) < timeout):
			Script.Sleep(50)
			if(Dstar.isDone):
				done = True
				break

		if (done):
			return Dstar.getInt()

		else:
			return [loc,loc2]

	else:
		movingresult = Dstar.startSenario(loc,loc2,Moving)
		if (movingresult):
			done = False
			while((time.clock()-timeStart) < timeout):
				Script.Sleep(50)
				if(Dstar.isDone):
					done = True
					break

			if (done):
				return Dstar.getInt()
			else:
				return False
		else:
			return False

def intercept(st,gl,b1,b2):
	dbx = b2[0]-b1[0]
	dby = b2[1]-b1[1]
	dpx = gl[0]-st[0]
	dpy = gl[1]-st[1]

	t1 = (st[1]-b1[1]-(dby/dbx)*(st[0]-b1[0]))/(dby*dpx/dbx-dpy)
	t2 = (st[0] - b1[0] + dpx*t1)/dbx
	intercept = [st[0]+dpx*t1, st[1]+dpy*t1]
	if (t1 < 0 or t1 > 1 or t2 < 0 or t2 > 1):
		return False
	else:
		return [st[0]+dpx*t1, st[1]+dpy*t1]


#
#	Should be good to go
#

#probably throw this into wpMission/Travel
#loiterunlimited change altitude
#have to change for new gps_distance function

def checkaltitudechange(loc1,loc2):#,loiterLoc):
	wps = []
	for i in range(len(lst)-1):
		dist = gps_distance(loc1.lat,loc1.lng,loc2.lat,loc2.lng)
		height = loc2.alt-loc1.alt
		slope = height/dist

		if(slope <= .48 or slope >= -.48):
			return False
		else:
			return Locationwp().Set((loc2.lat+loc1.lat)/2,(loc2.lng+loc1.lng)/2,loc2.alt, 31)
			# return Locationwp().Set(loiterloc.lat,loiterLoc.lng,loc2.alt, 31)

def WpMission(GlobalWp):

	GlobalPath = []

	templist = []

	for i in range(len(GlobalWp)-1):

		templist = getPath(GlobalWp[i], GlobalWp[i+1],False,10)

		# templist.append(GlobalWp[i+1])

		GlobalPath.append(templist)

	return GlobalPath

def addStaticObstacles(StaticObstacleLoc):
	Length = file_len_Loc(StaticObstacleLoc)
	with open(StaticObstacleLoc,"r") as ObSFile:
		for i in range(length):
			Obdat = ObSFile.readline().split(" ")
			staticObstacles.append([Obdat[1],Obdat[2],Obdat[3],Obdat[4]])


#
#	Working on these
#

def writeTel():
	with open('C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/telemetry.txt',"w") as Telfile:
		Telfile.write(str(cs.lat))
		Telfile.write(str(cs.lng))
		Telfile.write(str(cs.alt))
		Telfile.write(str(cs.nav_bearing))

def timeAtClosestApproach(Pos1,Vel1,Pos2,Vel2):
	p1 = Pos2[0]-Pos1[0]
	p2 = Pos2[1]-Pos1[1]
	p3 = Pos2[2]-Pos1[2]

	v1 = Vel2[0]-Vel1[0]
	v2 = Vel2[1]-Vel1[1]
	v3 = Vel2[2]-Vel1[2]

	t = -(p1*v1+p2*v2+p3*v3)/(v1**2+v2**2+v3**2)
	return t

def dca(Pos1,Vel1,Pos2,Vel2):
	t = timeAtClosestApproach(Pos1,Vel1,Pos2,Vel2)

	x1 = Pos1[0]+t*Vel1[0]
	y1 = Pos1[1]+t*Vel1[1]
	z1 = Pos1[2]+t*Vel1[2]

	x2 = Pos2[0]+t*Vel2[0]
	y2 = Pos2[1]+t*Vel2[1]
	z2 = Pos2[2]+t*Vel2[2]
	
	loc = [x2,y2,z2]

	dist = ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**.5
	return dist,loc

def dcaAddtime(Pos1,Vel1,Pos2,Vel2,time):
	
	x1 = Pos1[0]-time*Vel1[0]
	y1 = Pos1[1]-time*Vel1[1]
	z1 = Pos1[2]-time*Vel1[2]

	x2 = Pos2[0]-time*Vel2[0]
	y2 = Pos2[1]-time*Vel2[1]
	z2 = Pos2[2]-time*Vel2[2]

	dc,loc = dca([x1,y1,z1],Vel1,[x2,y2,z2],Vel2)
	return dc,loc



def missiontype(lst,strng):
	upload(lst,1)
	wp = 1
	while(cs.wpno < len(lst)-1)
		Script.Sleep(50)
		if (cs.wpno != wp)
			wp = cs.wpno
			print strng, " Wp number ",wp

def travel(previousWps,start,goal):
	wp = cs.wpno
	temp = [start]
	temp.extend(previousWps)
	temp.append(goal)
	upload(temp,1)

	while (cs.wpno == wp):
		Script.Sleep(10)

	path = getPath(start,goal,True,4)

	actualpath = temp
	if (path != False):
		if (cs.wpno == wp):
			temp2 = [start]
		else:
			temp2 = []
		temp2.extend(path)
		temp2.append(goal)
		actualpath = temp2
		upload(temp2,1)

	wp = 1
	while(cs.wpno < len(actualpath)-1):
		Script.Sleep(50)
		if (cs.wpno != wp)
			wp = cs.wpno
			print strng, " Wp number ",wp
#
#	DSTAR
#

class Dstar:
	
	def __init__(self,start):
		#self.dataPath = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/flight_information.txt'
		#self.intPath = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/shortest_path.txt'
		#self.MovingObstacleLoc = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/moving_obstacle_data.txt'

		self.dataPath = 'C:/Users/derek_000/Documents/Documents/MUAS/Python/Test/flight_information.txt'
		self.intPath = 'C:/Users/derek_000/Documents/Documents/MUAS/Python/Test/shortest_path.txt'
		self.MovingObstacleLoc = 'C:/Users/derek_000/Documents/Documents/MUAS/Python/Test/moving_obstacle_data.txt'
		self.Safety = 6
		self.cruise = 16

		if(start == None):
			self.Home = Locationwp().Set(cs.lat,cs.lng,0, 16)
		else:
			self.Home = start

		# self.Bounds = []
		#self.addBounds()
		#self.printBounds()

		self.StaticObstacles = [[0,0,100,20],[0,20,200,20]]
		#self.addStaticObstacles()
		print "finished Dstar"

	def addBounds(self):
		for i in range(len(bounds)):
			locat = self.toPoint(bounds[i])
			bond = [locat[0],locat[1]]
			self.Bounds.append(bond)

	def printBounds(self):
		with open(BoundsLoc,"w") as boundryFile:
			#boundryFile.write(str(len(self.Bounds)))
			for i in range(len(self.Bounds)):
				if (i != 0):
					boundryFile.write('\n')
				boundryFile.write(str(Bounds[i][0]))
				boundryFile.write(str('	'))
				boundryFile.write(str(Bounds[i][1]))

	def addStaticObstacles(self):
		for i in range(len(staticObstacles)):
			locat = self.toPoint2(staticObstacles[i][0],staticObstacles[i][1],staticObstacles[i][2])
			locat.append(staticObstacles[i][3])
			self.StaticObstacles.append(locat)
	
	def readMovingObstacles(self):
		movingobstas = []
		length = file_len_Loc(self.MovingObstacleLoc)
		with open(self.MovingObstacleLoc,"r") as movingFile:
			for i in range(length):
				movingdat = movingFile.readline().split(" ")
				pos = toPoint2(movingdat[1],movingdat[2],movingdat[3])
				xpos = pos[0]
				ypos = pos[1]
				zpos = pos[2]

				#testing
				# xpos = float(movingdat[1])
				# ypos = float(movingdat[2])
				# zpos = float(movingdat[3])
				
				rad = float(movingdat[4])
				xvel = float(movingdat[5])#/delLat 		#not sure if ill need these
				yvel = float(movingdat[6])#/delLng
				zvel = float(movingdat[7])
				movingobstas.append([xpos,ypos,zpos,rad,xvel,yvel,zvel])
		return movingobstas

	#fix right after if statement to save the obstacle 
	def getMovingObstacles(self,WPlst,TimeToStart):		
		Time = 0#TimeToStart#dist_CS(lst[0])
		
		movObs = self.readMovingObstacles()

		ImportantmovObs = []
		for i in range(len(WPlst)-1):
			Pos1 = WPlst[i]
			dx = WPlst[i+1][0]-WPlst[i][0]
			dy = WPlst[i+1][1]-WPlst[i][1]
			dz = WPlst[i+1][2]-WPlst[i][2]
			dis = (dx**2+dy**2+dz**2)**.5

			Vel1 = [dx*self.cruise/dis,dy*self.cruise/dis,dz*self.cruise/dis]

			for j in range(len(movObs)):
				Pos2 = [movObs[j][0],movObs[j][1],movObs[j][2]]
				Vel2 = [movObs[j][4],movObs[j][5],movObs[j][6]]

				closest,loc = dcaAddtime(Pos1,Vel1,Pos2,Vel2,Time)
				print closest,'	',loc,'	',movObs[j][3]+5
				if (closest < movObs[j][3]+self.Safety):
					loc.append(movObs[j][3]+self.Safety)

					ImportantmovObs.append(loc)

		Time = Time + dist_loc(lst[i],lst[i+1])/self.cruise



		return ImportantmovObs
		


		#probably return a list of location, radius, and velocity

	def toPoint2(self,lat,lng,alt):
		dlat = (lat - self.Home.lat)/delLat
		dlng = (lng - self.Home.lng)/delLng
		alt = alt
		return [dlat,dlng,alt]

	def toPoint(self,loc):
		dlat = (loc.lat - self.Home.lat)/delLat
		dlng = (loc.lng - self.Home.lng)/delLng
		alt = loc.alt
		return [dlat,dlng,alt]

	def toGPS(self,loc):
		dlat = (loc[0])*delLat + self.Home.lat
		dlng = (loc[1])*delLng + self.Home.lng
		alt = loc[2]
		return Locationwp().Set(dlat,dlng,alt, 16)

	def startSenario(self,wps,moving):
		self.kill()
		if (moving == False):
			Script.Sleep(.05)

		#testing
		# lst = wps

		lst = []
		for pnt in wps:
			lst.append(toPoint(pnt))
		start = lst[0]
		goal = lst[len(lst)-1]

		TimeToStart = 0

		movingobstas = self.getMovingObstacles([WPlst],TimeToStart)

		if (moving == True and len(movingobstas) == 0):
			return False
			print 'No moving obstacles needed'
		else:

			#find which file and how to write to it
			with open(self.dataPath,"w") as senarioFile:
				senarioFile.write("Changed 1")

				senarioFile.write(str('\n'))
				senarioFile.write("start")
				senarioFile.write(str('	'))
				senarioFile.write(str(start[0]))
				senarioFile.write(str('	'))
				senarioFile.write(str(start[1]))
				senarioFile.write(str('	'))
				senarioFile.write(str(start[2]))

				senarioFile.write(str('\n'))
				senarioFile.write("goal")
				senarioFile.write(str('	'))
				senarioFile.write(str(goal[0]))
				senarioFile.write(str('	'))
				senarioFile.write(str(goal[1]))
				senarioFile.write(str('	'))
				senarioFile.write(str(goal[2]))

				for ob in self.StaticObstacles:
					senarioFile.write(str('\n'))
					senarioFile.write("static")
					senarioFile.write(str('	'))
					senarioFile.write(str(ob[0]))
					senarioFile.write(str('	'))
					senarioFile.write(str(ob[1]))
					senarioFile.write(str('	'))
					senarioFile.write(str(ob[2]))
					senarioFile.write(str('	'))
					senarioFile.write(str(ob[3]))

				if (moving):
					print 'Moving obstacles found'
					for ob in self.getMovingObstacles([WPlst],TimeToStart):
						senarioFile.write(str('\n'))
						senarioFile.write("dynamic")
						senarioFile.write(str(' '))
						senarioFile.write(str(ob[0]))
						senarioFile.write(str(' '))
						senarioFile.write(str(ob[1]))
						senarioFile.write(str(' '))
						senarioFile.write(str(ob[2]))
						senarioFile.write(str(' '))
						senarioFile.write(str(ob[3]))
			return True

	def getInt():
		lngth = file_len_Loc(self.intPath)
		nodes = []

		with open(self.intPath,"r") as intFile:
			intFile.readline()

			for i in range(lngth-1):
				dat = intFile.readline().split(" ")
				nodes.append([dat[0],dat[1],dat[2]])

		#not sure how to node to WP with moving obstacles
		#WP = NodestoInt(nodes,self.staticObstacles,self.)
		IntWP = []

		for wp in WP:
			IntWP.append(self.toGPS(wp))
		return IntWP

	def isDone():
		done = False
		with open(self.intPath,"r") as intFile:
			if (dataFile.readline() == "Changed 1"):
				 done = True
		return done

	def kill(self):
		with open(self.dataPath,"w") as senarioFile:
			senarioFile.write("Changed 2")
		with open(self.intPath,"w") as senarioFile:
			senarioFile.write("Changed 0")

	#probably kill all of these
	def SafetoLoiter(self, loc):
		Safe = True
		loca = toPoint(loc)
		if (distFromPath([self.Bounds[1][1],self.Bounds[1][2],0],[self.Bounds[len(self.Bounds)][1], self.Bounds[len(self.Bounds)][2], 0],[loca[1],loca[2],0]) <= loiterRadius*1.15):
			Safe = False
		for i in range(len(bounds)-1):
			if (distFromPath([self.Bounds[i][1],self.Bounds[i][2],0],[self.Bounds[i+1][1], self.Bounds[i+1][2], 0],[loca[1],loca[2],0]) <= loiterRadius*1.3):
				Safe = False


		for i in range(len(StaticObstacles)):		
			if (((StaticObstacles[i][1]-loca[1])**2+(StaticObstacles[i][2]-loca[2])**2)*.5 <= (1.3*loiterRadius+StaticObstacles[i][4])):
				Safe = False
		return Safe

	#probably dont need
	def PathClear(lst):
		path = []
		for loc in lst:
			path.append(toPoint(loc))

		Safe = True
		for j in range(len(path)-1):
			if (intercept([self.Bounds[1][1],self.Bounds[1][2]],[self.Bounds[len(self.Bounds)][1], self.Bounds[len(self.Bounds)][2]],[path[j][1],path[j][2]],[path[j+1][1],path[j+1][2]]) != False):
				Safe = False
			for i in range(len(bounds)-1):
				if (intercept([self.Bounds[i][1],self.Bounds[i][2]],[self.Bounds[i+1][1], self.Bounds[i+1][2]],[path[j][1],path[j][2]],[path[j+1][1],path[j+1][2]]) != False):
					Safe = False
			#see if were going to go above it
			for i in range(len(StaticObstacles)):		
				if (distFromPath([path[j][1],path[j][2]],[path[j+1][1],path[j+1][2]],[self.StaticObstacles[i][1],self.StaticObstacles[i][2],0]) <= (10+StaticObstacles[i][4])):
					Safe = False
		return Safe

	#finish this
	def findSafeLoiter(lst):
		dist = dist_loc(lst[0],lst[1])
		dlat = (lst[1].lat-lst[0].lat)/int(dist/10)
		dlng = (lst[1].lng-lst[0].lng)/int(dist/10)
		for j in range(int(dist/10)):
			loc = Locationwp().Set(lst[0].lat+j*dlat,lst[0].lng+j*dlat,alt, 16)
			if (SafetoLoiter(loc)):
				return loc

		#not sure how to find better point
		print "no point found that is safe to loiter"
		return lst[0]

#
#	Testing parameters
#


dropspot = Locationwp().Set(38.3652711,-76.5366065,50, 16)
'''
bounds = [Locationwp().Set(38.3650585,-76.5367001,0, 16)]
bounds.append(Locationwp().Set(38.3652015,-76.5390927,0, 16))
bounds.append(Locationwp().Set(38.3659207,-76.5388942,0, 16))
bounds.append(Locationwp().Set(38.3658198,-76.5372419,0, 16))
bounds.append(Locationwp().Set(38.3669806,-76.5368342,0, 16))
bounds.append(Locationwp().Set(38.3666441,-76.5348816,0, 16))
bounds.append(Locationwp().Set(38.3659375,-76.5350318,0, 16))
bounds.append(Locationwp().Set(38.3652309,-76.5335298,0, 16))
bounds.append(Locationwp().Set(38.3647766,-76.5338302,0, 16))

offaxisloc = Locationwp().Set(38.3646505,-76.5376335,0, 16)
'''
wp1 = Locationwp().Set(38.3656641,-76.5385830,0, 16)
wp2 = Locationwp().Set(38.3652225,-76.5342271,0, 16)
GlobalWp = [wp1,wp2]

OB1 = [38.3654833,-76.5365821,100,40]
staticObstacles = [OB1]


#StartPoint = Locationwp().Set(38.3652730,-76.5367323,0, 16)
# Dstar = Dstar(None)
# Dstar.startSenario(wp1,wp2,True)

FarLeft = Locationwp().Set(38.3661731,-76.5402782,50, 16)
FarRight = Locationwp().Set(38.3650543,-76.5328163,50, 16)


#
#	Mission Parameters
#


#dropspot,homeLoc,offaxisloc,emergentLoc = getMissionData(missionFileLoc)

#MissionWp = getMissionData(missionFileLoc)

#bounds = getBoundryData(BoundLoc)

#staticObstacles = getStaticObData(StaticObstacleLoc)

#upload geofence
#upload search grid points and save search grid to readable file


#
#	Programable changes
#

homebear = -6.5*(pi/180)
dropbear = -6.5*(pi/180)


#
#	Mission Setup
#


#global pathName
#global StaticObstacleLoc
#global MovingObstacleLoc
#global BoundsLoc
#global WPFileLoc
#global missionFileLoc
#global SearchfileLoc

'''
pathName = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/'
StaticObstacleLoc = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/static_obstacle_data.txt'
MovingObstacleLoc = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/moving_obstacle_data.txt'
BoundsLoc = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/boundry.txt'
WPFileLoc = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/Mission_WP.txt'
missionFileLoc = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/Mission_data.txt'

SearchfileLoc = 'C:/Users/imaging2.0/Documents/MUAS-17/Flight_Path/searchGrid.waypoints'
'''
SearchfileLoc = 'D:/MUAS/Imaging/CameraGrid.waypoints';


#cameragridWP = cameraGrid(SearchfileLoc)
#totalwps = takeoffWps
#totalWps.extend([FarRight])1
#totalWps.extend(cameragridWP)
#totalWps.extend([FarLeft]) 
#totalWps.extend(landingWP)

#print "starting"

Dstar = Dstar(None)

groundBearing = homebear
print "Ground bearing is ",groundBearing

takeoffWps = takeoff()

GlobalWp = readInteropWpFile(InteropFileLoc)
MissionWP = WpMission(GlobalWp)

payloadWp = payloaddrop(dropspot,dropbear)

searchGridWp = cameraGrid(SearchfileLoc)

offAxisWP = offaxistarget(offaxisloc)

median = checkaltitudechange(FarRight,searchGridWp[0])
median2 = checkaltitudechange(searchGridWp[len(searchGridWp)-1],FarLeft)

landingWP = landLoc(Dstar.Home,groundBearing)


takeoffToWPMissionWP = getPath(getTakeoffLoc(Dstar.Home,homebear),MissionWP[0],False,10)

missionWPtoPayload = getPath(MissionWP[len(MissionWP)-1],payloadWp[0],False,10)

payloadToCamera = getPath(payloadWp[len(payloadWp)-1],searchGridWp[0],False,10)

CameraToOffAxis = getPath(searchGridWp[len(searchGridWp)-1],offAxisWP[0],False,10)

OffAxisToLanding = getPath(offAxisWP[len(offAxisWP)-1],landingWP[0],False,10)

#
#	Mission Execution
#

def missiontype(lst,strng):
	upload(lst,1)
	wp = 1
	while(cs.wpno < len(lst)-1)
		Script.Sleep(50)
		if (cs.wpno != wp)
			wp = cs.wpno
			print strng, " Wp number ",wp

def travel(previousWps,start,goal):
	wp = cs.wpno
	temp = []
	if (start != None):
		temp.append(start)

	temp.extend(previousWps)
	temp.append(goal)
	upload(temp,1)

	if (start != None):
		st = start
		while (cs.wpno == wp):
			Script.Sleep(10)
	else
		st = Locationwp().Set(cs.lat,cs.lng,cs.alt, 16)


	path = getPath(st,goal,True,4)

	actualpath = temp
	if (path != False):
		path.append(goal)
		actualpath = path
		upload(path,1)

	wp = 1
	while(cs.wpno < len(actualpath)-1):
		Script.Sleep(50)
		if (cs.wpno != wp)
			wp = cs.wpno
			print strng, " Wp number ",wp






takeoffWps.extend(takeoffToWPMissionWP)
upload(takeoffWps)


uploadWp(totalWps,1)
print "uploaded"

speak("Starting Mission")
Script.Sleep(3000)

MAV.doARM(True)
speak("Armed")
Script.Sleep(2000)
speak("Taking Off")
MAV.setMode("Auto")



while(cs.wpno == 1):
	Script.Sleep(5):


travel(takeoffToWPMissionWP,None,GlobalWp[0])




for i in range(len(GlobalWp-1))
	travel(MissionWP[i],GlobalWp[i],GlobalWp[i])


travel(missionWPtoPayload,MissionWP[len(MissionWP)-1],payloadWp[0])

missiontype(payloadWp,'Payload Drop')

travel(payloadToCamera,payloadWp[len(payloadWp)-1],searchGridWp[0])

missiontype(searchGridWp,'Grid Search')

travel(CameraToOffAxis,searchGridWp[len(searchGridWp)-1],offAxisWP[0])

missiontype(offAxisWP,'Off Axis')

travel(OffAxisToLanding,offAxisWP[len(offAxisWP)-1],landingWP[0])

upload(landingWP,1)

