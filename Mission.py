import sys
import math
from math import pi,sin,cos,atan,atan2
import clr
import time
import System
from System import Byte


#from System import Threading
#rom System.Threading import Thread, ThreadStart
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
global Home
global givenTime
global Dstar

global delLat
global delLng

delLat = .00000899
delLng = .0000116
givenTime = 2
Dstar = Dstar()

def gps_distanceCS(lat, lng):
	dist = ((lat-cs.lat)**2+(lng-cs.lng)**2)
	return (dist**(1/2.0))

def gps_distance(lat1,lng1,lat2,lng2):
	dist = (((lat2-lat1)/delLat)**2+((lng2-lng1)/delLng)**2)**.5
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
	global Home
	Home = Locationwp().Set(cs.lat,cs.lng,0, 16)
	global groundBearing
	groundBearing = cs.nav_bearing*(3.1415/180)
	print "ground bearing is ",groundBearing, " at location ",Home.lat,", ", Home.lng

def setHome(num):
	MAV.setWPTotal(num)	
	MAV.setWP(Home,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);

def closestPoint(gl, st, ob):
	#gl = [goal.lat,goal.lng,goal.alt]
	#st = [start.lat,start.lng,goal.alt]
	lin = [gl[0]-st[0],gl[1]-st[1],gl[2]-st[2]]
	length = ((lin[0])**2+(lin[1])**2+(lin[2])**2)*.5
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

def speak(str):
	MissionPlanner.MainV2.speechEngine.SpeakAsync(str)
	pass

def readWpFile(wpfilename):
	globallist = open(wpfilename,"r")
	lngth = file_len(wpfilename)
	lst = []
	if (globallist.readline().split()[1] == "WPL"):
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

def readInteropWpFile(wpfileLoc):
	lngth = file_len(wpfileLoc)
	with open(wpfileLoc,"r") as globallist:
		lst = []
		if (lngth != 0):
			for wpnum in range(lngth):
				dat = globallist.readline().split("	")
				cam = Locationwp()
				Locationwp.id.SetValue(cam, 16)
				Locationwp.lat.SetValue(cam, float(dat[1]))
				Locationwp.lng.SetValue(cam, float(dat[2]))
				Locationwp.alt.SetValue(cam, float(dat[3]))
				lst.append(cam)  #append cam trig
		else:
			print "Nothing found"
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

def getCameraGridStart(wpfilename):
	globallist = open(wpfilename,"r")
	lngth = file_len(wpfilename)
	lst = []
	if (globallist.readline().split()[1] != "WPL"):
		print "Nothing found"
		return None
	else:
		globallist.readline()
		dat = globallist.readline().split("	")
	
	return Locationwp().Set(dat[8],dat[9],dat[10], 16)

def cameraGrid(wpfileLoc):
	lngth = file_len_Loc(wpfileLoc)
	with open(wpfileLoc,"r") as globallist:
		lst = []
		if (globallist.readline().split()[1] != "WPL"):
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

def takeoff():
	to = Locationwp()
	Locationwp.id.SetValue(to, int(MAVLink.MAV_CMD.TAKEOFF))
	Locationwp.p1.SetValue(to, 15)
	Locationwp.alt.SetValue(to, 40)

	dist = gpsDist(310)
	lat1 = cs.lat + dist*sin(groundBearing)
	lng1 = cs.lng + dist*cos(groundBearing)
 
	loc = Locationwp().Set(lat1,lng1,50, 16)

	#setHome(20)
	#MAV.setWP(to,1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
	#MAV.setWP(loc,2,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);

	return to

	#tempalt = cs.alt
	#speak("Taking off")
	#Script.Sleep(2000)
	#MAV.setMode("Auto")
	#while(True):
	#	Script.Sleep(100)
	#	if (cs.wpno == 2):#.5*(cs.alt+tempalt) > 40):
	#		break
	#		print "finished taking off "
		#tempalt = cs.alt

def getLandingStart():
	descent_ratio = 20.0/150.0 #20 meter descent for every 150 meters traveled
	alt1 = 50
	dist1 = gpsDist(alt1/descent_ratio)
	lat1 = loc.lat - dist1*sin(bear)
	lng1 = loc.lng - dist1*cos(bear)
	return Locationwp().Set(lat1,lng1,alt1, 16)

#rework
def landLoc(loc,bear):
	descent_ratio = 20.0/150.0 #20 meter descent for every 150 meters traveled
	alt1 = 50
	alt2 = 20
	dist1 = gpsDist(alt1/descent_ratio)
	dist2 = gpsDist(alt2/descent_ratio)
	lat1 = loc.lat - dist1*sin(bear)
	lng1 = loc.lng - dist1*cos(bear)
	lat2 = loc.lat - dist2*sin(bear)
	lng2 = loc.lng - dist2*cos(bear)

	setHome(20)
	MAV.setWP(Locationwp().Set(lat1,lng1,alt1, 16),1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
	MAV.setWP(Locationwp().Set(lat2,lng2,alt1, 16),2,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
	MAV.setWP(Locationwp().Set(loc.lat,loc.lng,0,21),3,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);

#rework
def land():
	descent_ratio = 20.0/150.0 #20 meter descent for every 150 meters traveled
	alt1 = 50
	alt2 = 20
	dist1 = gpsDist(alt1/descent_ratio)
	dist2 = gpsDist(alt2/descent_ratio)
	lat1 = Home.lat - dist1*sin(groundBearing)
	lng1 = Home.lng - dist1*cos(groundBearing)
	lat2 = Home.lat - dist2*sin(groundBearing)
	lng2 = Home.lng - dist2*cos(groundBearing)

	setHome(20)
	MAV.setWP(Locationwp().Set(lat1,lng1,alt1, 16),1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
	MAV.setWPCurrent(1)
	MAV.setWP(Locationwp().Set(lat2,lng2,alt1, 16),2,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
	MAV.setWP(Locationwp().Set(Home.lat,Home.lng,0,21),3,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);

#has to be able to stop if cant get to 
def uploadGlobal(globalWp,globalWpNum,intWp):
	setHome(50)
	numInt = 0
	MAV.setWP(globalWp[globalWpNum-1],1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
	if (intWp != None):
		numInt += len(intWp)
		for i in range(len(intWP)):
			MAV.setWP(intWP[i],2+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
	MAV.setWPCurrent(2)
	MAV.setWP(globalWp[globalWpNum],2+numInt,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
	if (globalWpNum+1 < len(globalWp)):
		MAV.setWP(globalWp[globalWpNum]+1,3+numInt,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)

def getpayloadstart(loc, bear):
	distprevious1 = gpsDist(180)
	prelat1 = loc.lat - distprevious1*sin(bear)
	prelng1 = loc.lng - distprevious1*cos(bear)

	MAV.setWP(Locationwp().Set(prelat1,prelng1,50, 16),1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);

	return None

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

	speak("setting up payload drop")
	setHome(50)
	MAV.setWP(Locationwp().Set(prelat1,prelng1,50, 16),1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
	MAV.setWPCurrent(1)
	MAV.setWP(Locationwp().Set(prelat2,prelng2,50, 16),2,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
	MAV.setWP(Locationwp().Set(droplat,droplng,50, 16),3,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);

	dropWP = Locationwp()
	Locationwp.id.SetValue(dropWP, 183)
	Locationwp.p1.SetValue(dropWP, 13)
	Locationwp.p2.SetValue(dropWP, 1900)

	MAV.setWP(dropWP,4,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
	MAV.setWP(Locationwp().Set(postlat,postlng,55, 16),5,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);

	while (cs.wpno < 3):
		print "dist to drop point is ",meters(gps_distanceCS(dropspot.lat,dropspot.lng))
		Script.Sleep(100)
	speak("Bombs Away")
	while (cs.wpno < 5):
		pass
		Script.Sleep(100)		

#figure this out in the future
def uploadWp(lst):
	setHome(50)
	if (len(lst) != 0):
		for i in range(len(lst)):
			MAV.setWP(lst[i],1+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
			if (i+1 == 1):
				MAV.setWPCurrent(1)
	#MAV.setMode("Auto")

def travel(loc,loc2):
	if (cs.wpno != None):
		start = MAV.getWP(cs.wpno)
		if(loc2 == None):
			uploadWp([start,loc])
		else:
			uploadWp([start,loc,loc2])
		MAV.setWPCurrent(1)
	else:
		start = Locationwp().Set(cs.lat,cs.lng,cs.alt, 16)
		if(loc2 == None):
			uploadWp([start,loc])
		else:
			uploadWp([start,loc,loc2])
		MAV.setWPCurrent(2)
		

	#dstar = Dstar(start,loc,[])
	#dstar.replan()
	if(loc2 == None):
		uploadWp([start,loc])
	else:
		uploadWp([start,loc,loc2])

	
	notArrived = True
	while(notArrived):		#waiting for dstar result
		Script.Sleep(100)
		print cs.wpno
		if (True):#dstar.isDone()):
			IntWp = []#dstar.getInt()
			if (len(IntWp) > 0):
				speak("Intermidiate waypoints needed")
				lst = [start]
				for wp in IntWp:
					lst.append(wp)
				lst.append(loc)
				if(loc2 != None):
					lst.append(loc2)
				uploadWp(lst)
			break

		if (gps_distanceCS(loc.lat, loc.lng) < gpsDist(16*givenTime)):
			notArrived = False 
			#dstar.kill()

	#Transversing towards  WP
	while (notArrived):
		Script.Sleep(100)
		print cs.alt
		if (needReplan()):
			pass
			#what to do here

		if (gps_distanceCS(loc.lat, loc.lng) < gpsDist(16*givenTime)):
			notArrived = False

		Script.Sleep(5000)
		notArrived = False

#total rework of this
def WpMission(InteropFileLoc):
	GlobalUpdate = False
	GlobalWpNum = 0
	#GlobalWp = readInteropWpFile(InteropFileLoc)
	GlobalWp = readWpFile("TestWPMission.txt")
	while (GlobalWpNum < len(GlobalWp)):
		
		if (GlobalWpNum+1 < len(GlobalWp)):
			travel(GlobalWp[GlobalWpNum],GlobalWp[GlobalWpNum+1])
		else:
			travel(GlobalWp[GlobalWpNum],None)
		speak("Starting Next Waypoint")
		print "Starting Next Waypoint"
		GlobalWpNum += 1
	print "done with waypoints"

def getMissionData(missionFileLoc):
	with open(missionFileLoc,"r") as missionFile:
		airdropData = missionFile.readline().split("	")
		homeData = missionFile.readline().split("	")
		offaxisData = missionFile.readline().split("	")
		emergentData = missionFile.readline().split("	")
		
		airdropLoc = Locationwp().Set(float(airdropData[1]),float(airdropData[2]),0, 16)
		homeLoc = Locationwp().Set(float(homeData[1]),float(homeData[2]),0, 16)
		offaxistagetLoc = Locationwp().Set(float(offaxisData[1]),float(offaxisData[2]),0, 16)
		emergentLoc = Locationwp().Set(float(emergentData[1]),float(emergentData[2]),0, 16)
	return airdropLoc, homeLoc, offaxistagetLoc, emergentLoc

def getWPData(WPFileLoc):
	length = file_len_Loc(WPFileLoc)
	WPs = []
	with open(WPFileLoc,"r") as WPFile:
		for i in range(length)
			WPdat = WPFile.readline().split("	")
			WPs.append(Locationwp().Set(float(WPdat[1]),float(WPdat[2]),float(WPdat[3]), 16))
	return WPs

def getBoundryData(BoundFileLoc):
	length = file_len_Loc(BoundFileLoc)
	bounds = []
	with open(WPFileLoc,"r") as BoundFile:
		BoundFile.readline()
		BoundFile.readline()
		for i in range(length-2)
			WPdat = BoundFile.readline().split("	")
			bounds.append(Locationwp().Set(float(WPdat[1]),float(WPdat[2]),float(WPdat[3]), 16))
	return bounds

def getBoundryData(ObSFileLoc):
	length = file_len_Loc(ObSFileLoc)
	Obstas = []
	with open(WPFileLoc,"r") as ObSFile:
		for i in range(length)
			Obdat = ObSFile.readline().split("	")
			Obstas.append(obStatic(float(Obdat[1]),float(Obdat[2]),float(Obdat[3]),float(Obdat[4])))
	return bounds

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

def offaxistarget(loc,bounds):
	boundry1,boundry2 = findclosestboundries(loc,bounds)
	print 'made it through findclosestboundies'
	safeloc = findSafeOffAxisLoc(boundry1,boundry2,loc)
	
	#negative 1 if want to go RtoL
	LtoR = 1

	dist = (((safeloc.lat-loc.lat)/delLat)**2 + ((safeloc.lng-loc.lng)/delLng)**2)**.5
	height = safeloc.alt
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
	#move gimbal to angle

	predist2 = -80
	latPre2 = safeloc.lat + (predist2*sin(direc))*delLat
	lngPre2 = safeloc.lng + (predist2*cos(direc))*delLng
	preOff2 = Locationwp().Set(latPre2,lngPre2,height, 16)
	print 'camera trigger'
	#camtrig once

	afterDist = 40
	lataft = safeloc.lat + (afterDist*sin(direc))*delLat
	lngaft = safeloc.lng + (afterDist*cos(direc))*delLng
	afterOff = Locationwp().Set(lataft,lngaft,height, 16)
	print 'reseting gimbal'
	#move gimbal back to reg

	return [preOff1,preOff2,safeloc,afterOff]

#
#	Should be good to go
#

#put inside of Dstar
def NodestoInt(nodes,ObSList,ObMList):
	#just needs to filter the list to take out unnecessary one
	waypoints = []
	cansee = True
	onNode = 1
	lastNode = 0
	previousNode = 0
	for on in range(1,len(nodes)):

		cansee = True

		for i in range(len(ObSList)):
			if (distFromPath(nodes[on], nodes[lastNode],ObSList[i]) < ObSList[i].rad*.00001):
				cansee = False
	        
	    #for i in range(len(ObMList)):
		#	if (distFromPath(nodes[on], nodes[lastNode],ObSList[i]) < ObSList[i].rad*.00001):
		#		cansee = False

		if (cansee == False):
			waypoints.append(nodes[previousNode])
			lastNode = previousNode

		previousNode += 1
	
	return waypoints


#
#	Working on these
#


#turns out this doesnt work
def writePhotoLocations(lst):
	print "writing locations to file"
	locList = []
	for i in range(len(lst)):
		print i
		if (lst[i].id == 203 or lst[i].id == 206):
			if (lst[i].p1 == 0):
				locList.append(lst[i-1])
			else:
				alt = lst[i-1].alt
				lat1 = lst[i-1].lat
				lat2 = lst[i+1].lat
				lng1 = lst[i-1].lng
				lng2 = lst[i+1].lng

				phi = atan2((lat2-lat1),-(lng2-lng1))

				lat = lat1 + gpsDist(lst[i].p1)*sin(phi)
				lng = lng1 - gpsDist(lst[i].p1)*cos(phi)

				locList.append(Locationwp().Set(lat,lng,alt, 16))

	print "actually writing now", len(locList)
	locFile = open("PhotoLocations.txt","w")
	for j in range(len(locList)):
		locFile.write(str(j+1))
		locFile.write(str('	'))
		locFile.write(str(locList[j].lat))
		locFile.write(str('	'))
		locFile.write(str(locList[j].lng))
		locFile.write(str('	'))
		locFile.write(str(locList[j].alt))
		locFile.write('\n')
		print j
	print 'done writing file'
	locFile.close()

#should probably be deleted
def needReplan():#ob,WPlen):
	objectsInPath = False
	'''
	for i in range(WPlen):
		for j in range(len(ob))
			if (distFromPath(MAV.getWP(cs.wpno-1+i,cs.wpno+i,ob[j])) < ob[j][3]+safety):
				objectsInPath = True
	'''
	if (objectsInPath):
		return True
	else:
		return False

#probably throw this into wpMission/Travel
#loiterunlimited change altitude
#have to change for new gps_distance function
def checkaltitudechange(lst):
	wps = []
	for i in range(len(lst)-1):
		dist = meters(gps_distance(lst[i].lat,lst[i].lng,lst[i+1].lat,lst[i+1].lng))
		height = lst[i+1].alt-lst[i].alt
		slope = height/dist
		wps.append(lst[i])
		if(slope >= .48 or slope <= -.48):
			halflat = (lst[i].lat + lst[i+1].lat)/2
			halflng = (lst[i].lng + lst[i+1].lng)/2
			wps.append(Locationwp().Set(halflat,halflat,lst[i+1].alt, 31))
			#print "need waypoint in between"
	wps.append(lst[len(lst)])


#
#	Mission Objects
#
class obStatic():
	def __init__(self,longitude,latitude,altitude,radius):
		self.lng = longitude
		self.lat = latitude
		self.alt = altitude
		self.rad = radius

class obMoving():
	def __init__(self,longitude,latitude,altitude,radius):
		self.lng = longitude
		self.lat = latitude
		self.alt = altitude
		self.rad = radius
		self.vel = [0,0,0]

	def getloc(time):
		x = self.lng + (time*self.vel[0])
		y = self.lat + (time*self.vel[1])
		x = self.alt + (time*self.vel[2])
		return [x,y,z]

	def update(self,FileLoc):
		self.lng = 0
		self.lat = 0
		self.alt = 0


#find away to enter a route
class Dstar:
	def __init__(self):
		self.obM = []
		self.obS = []
		self.dataPath = 'D:/muas/Autopilot/Dstar/senario.txt'
		self.intPath = 'D:/muas/Autopilot/Dstar/IntWp.txt'
		self.scale = 0
		self.start = None
		self.obstacleList = []

	def addObS(self,lst):
		for ob in lst:
			self.obS.append(ob)

	def addObM(self,lst):
		for ob in lst:
			self.obM.append(ob)

	def updateMoving():
		#do something here
		return None
	
	def startSenario(self,st,gl):
		if (self.scale != 0):
			self.kill()
		self.start = st
		dlat = gl.lat - st.lat
		dlng = gl.lng - st.lng

		latMeter = dlat / (delLat)
		lngMeter = dlng / (delLng)

		self.scale = 100/(((latMeter**2)+(lngMeter**2))**.5)
		self.obstacleList = []
		for ob in self.obS:
			Y = dlat*self.scale/delLat
			X = dlng*self.scale/delLng
			Z = dalt*self.scale
			R = 1.25*ob.radius*self.scale
			obstacleList.append([X,Y,Z,R])

		#find which file and how to write to it
		with open(self.dataPath,"w") as senarioFile:
			senarioFile.write("Changed 1")

			senarioFile.write(str('\n'))
			senarioFile.write("start")
			senarioFile.write(str('	'))
			senarioFile.write(str(0))
			senarioFile.write(str('	'))
			senarioFile.write(str(0))
			senarioFile.write(str('	'))
			senarioFile.write(str(0))

			senarioFile.write(str('\n'))
			senarioFile.write("goal")
			senarioFile.write(str('	'))
			senarioFile.write(str(lngMeter*scale))
			senarioFile.write(str('	'))
			senarioFile.write(str(latMeter*scale))
			senarioFile.write(str('	'))
			senarioFile.write(str(dalt*altScale))

			for ob in obstacleList:
				senarioFile.write(str('\n'))
				senarioFile.write("Obstacle")
				senarioFile.write(str('	'))
				senarioFile.write(str(ob[0]))
				senarioFile.write(str('	'))
				senarioFile.write(str(ob[1]))
				senarioFile.write(str('	'))
				senarioFile.write(str(ob[2]))
				senarioFile.write(str('	'))
				senarioFile.write(str(ob[3]))
		#write in files to start the dstar process
	
	def getInt():
		lngth = file_len_Loc(self.intPath)
		nodes = []
		with open(self.intPath,"r") as intFile:
			intFile.readline()
			for i in range():
				dat = intFile.readline().split("	")
				nodes.append([dat[0],dat[1],dat[2]])
		WP = NodestoInt(nodes,self.obstacleList,[])
		IntWP = []
		for wp in WP:
			lat = (wp[1]/scale)*delLat
			lng = (wp[0]/scale)*delLng
			alt = (wp[2])/scale
			IntWP.append(Locationwp().Set(lat,lng,alt, 16))
		return IntWP

	def isDone():
		done = False
		with open(self.intPath,"r") as intFile:
			if (intFile.readline() == "1"):
				 done = True
		return done

	def kill():
		with open(self.dataPath,"w") as senarioFile:
			senarioFile.write("Changed 0")
		with open(self.intPath,"w") as senarioFile:
			senarioFile.write(str(0))
		self.start = None
		self.scale = 0
		self.obstacleList = []



#
#	Mission Parameters
#

#pathName = 'D:/muas/Autopilot/Mission_Data/'


#missionFileLoc = os.path.join(pathName,'Mission_data.txt')
#dropspot,homeLoc,offaxistarget,emergentLoc = getMissionData(missionFileLoc)


#WPFileLoc = os.path.join(pathName,'Mission_WP.txt')
#MissionWp = getMissionData(missionFileLoc)


#BoundFileLoc = os.path.join(pathName,'fly_zones.txt')
#Bounds = getBoundryData(BoundFileLoc)


#ObSFileLoc = os.path.join(pathName,'Mission_WP.txt')
#staticObstacles = getObSData(ObSFileLoc)
#Dstar.addObS(staticObstacles)

#upload geofence

#upload search grid points and save file
#search

#maybe moving obstacles

#
#	needed for testing
#
#dropspot = Locationwp().Set(39.0829473,-76.9045366,50, 16)
#testOb = obStatic(-76.9053805,39.0837427,200,40)


#
#	change during mission
#
#homebear = 194*(pi/180)
#dropbear = 15*(pi/180)


#
#	Mission Execution
#
'''
print "starting"
defineHome()
print "Home Defined"
if (groundBearing == 0.0):
	groundBearing = homebear
	print "New ground bearing is ",groundBearing

takeoff()

WPFileLoc = os.path.join(pathName,'Mission_WP.txt')
WpMission(WPFileLoc)

travel(getpayloadstart(dropspot,dropbear))
payloaddrop(dropspot,dropbear)

#fix this to read the correct place
travel(getCameraGridStart())
cameraGrid('D:/muas/Autopilot/MissionData/PhotoGrid.txt')
#cameraGrid("TestPhotoGridTrigg.txt")

#travel()
#offaxistarget()

travel(getLandingStart(Home,homebear))
landLoc(Home,homebear)
'''
