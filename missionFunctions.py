import math
from math import pi,sin,cos,atan,atan2
import time

import MissionPlanner
from MissionPlanner.Utilities import Locationwp
import MAVLink

MissionPlanner.MainV2.speechEnable = True



class missionTasks:


	def __init__(self,CS,mav,cord_Sys):

		self.cord_System = cord_Sys
		self.MAV = mav
		self.cs = CS
		self.Home = cord_Sys.Home

		# southern maryland
		# self.droploc = [38.3652078,-76.5366331,35]
		# competition
		self.droploc = [38.1459313,-76.4263701,35]
		self.dropMeters = self.cord_System.toMeters(self.droploc)
		self.dropwps = self.payloaddropSet()

		# southern maryland
		# self.offAxisloc = [38.3648986,-76.5373251,100]
		# competition
		self.offAxisloc = [38.1476020,-76.4272070,100]
		self.offAxisheight = 100
		self.offAxisDist = 110
		self.offAxisMeters = self.cord_System.toMeters(self.offAxisloc)
		self.offAxiswps = self.offAxisSet()

		# southern maryland
		# self.emergentloc = [38.3652078,-76.5366331,50]
		# competition
		self.emergentloc = [38.1441594,-76.4251471,50]
		self.emergentMeters = self.cord_System.toMeters(self.emergentloc)
		self.emergentwps = self.emergentwpsSet()
		
		self.LandLoc = self.Home
		self.landingwps = self.landSet()

		self.TakeoffWps = self.takeoffSet()
		# self.takeoffPoint = []

		self.searchGridWps = self.searchGridSet()

		print "initalized mission functions"


	def speak(self,strin):
		MissionPlanner.MainV2.speechEngine.SpeakAsync(strin)		

	# done
	def set_MP_wps(self,wps):
		self.MAV.setWPTotal(len(wps)+1)	
		self.MAV.setWP(Locationwp().Set(self.Home[0],self.Home[1],self.Home[2], 16),0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)

		for i in range(len(wps)):
			self.MAV.setWP(wps[i],1+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
			if (i+1 == 1):
				self.MAV.setWPCurrent(1)

		self.MAV.setMode("Auto")
		OFile = open('GUI/waypoints.txt',"w")
		for i in range(len(wps)):
			if(wps[i].id == 16):
				if(i != 0):
					OFile.write(str('\n'))
				temp = self.cord_System.toMeters([wps[i].lat,wps[i].lng,wps[i].alt])
				OFile.write(str(temp[0]))
				OFile.write(str(' '))
				OFile.write(str(temp[1]))
				OFile.write(str(' '))
				OFile.write(str(temp[2]))
		OFile.close()

	# done
	def set_vehicle_waypoints(self,wps):
		self.MAV.setWPTotal(len(wps)+1)	
		self.MAV.setWP(Locationwp().Set(self.Home[0],self.Home[1],self.Home[2], 16),0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
		for i in range(len(wps)):
			tempcord = self.cord_System.toGPS([wps[i][0],wps[i][1],wps[i][2]])
			self.MAV.setWP(Locationwp().Set(tempcord[0],tempcord[1],tempcord[2],16),1+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
			if (i+1 == 1):
				self.MAV.setWPCurrent(1)
		self.MAV.setMode("Auto")

		OFile = open('GUI/waypoints.txt',"w")
		for i in range(len(wps)):
			if(i != 0):
				OFile.write(str('\n'))
			OFile.write(str(wps[i][0]))
			OFile.write(str(' '))
			OFile.write(str(wps[i][1]))
			OFile.write(str(' '))
			OFile.write(str(wps[i][2]))
		OFile.close()

	# done
	def takeoffSet(self):
		to = Locationwp()
		Locationwp.id.SetValue(to, 21)
		Locationwp.p1.SetValue(to, 15)
		Locationwp.alt.SetValue(to, 40)
		return [to]

	# done
	def takeoff(self,wp1GPS):
		time.sleep(1)
		self.speak('Taking off')
		time.sleep(2)
		temp = self.TakeoffWps
		temp.append(Locationwp().Set(wp1GPS[0],wp1GPS[1],wp1GPS[2], 16))
		self.set_MP_wps(temp)
		while(self.cs.wpno == 1):
			time.sleep(.1)

	# done
	def offAxisSet(self):

		dist = self.offAxisDist
		height = self.offAxisheight
		angle = atan(dist/height)
		
		bear = 20
		LookRight = 1

		safeloc = [self.offAxisMeters[0]-LookRight*dist*sin(bear*pi/180),self.offAxisMeters[1]+LookRight*dist*cos(bear*pi/180),height]
		

		predist = -150
		prex = safeloc[0] + predist*cos(bear*pi/180)
		prey = safeloc[1] + predist*sin(bear*pi/180)
		pre = self.cord_System.toGPS([prex,prey,height])
		preloc = Locationwp().Set(pre[0],pre[1],height, 16)
		
		setangle = Locationwp()
		Locationwp.id.SetValue(setangle, 205)
		Locationwp.p2.SetValue(setangle, angle)
		
		offloc = self.cord_System.toGPS(safeloc)
		offloc = Locationwp().Set(offloc[0],offloc[1],height, 16)

		takephoto = Locationwp()
		Locationwp.id.SetValue(takephoto, 203)
		
		after1dist = 20
		prex = safeloc[0] + after1dist*cos(bear*pi/180)
		prey = safeloc[1] + after1dist*sin(bear*pi/180)
		post1 = self.cord_System.toGPS([prex,prey,height])
		post1 = Locationwp().Set(post1[0],post1[1],height, 16)
				
		resetangle = Locationwp()
		Locationwp.id.SetValue(resetangle, 205)
		Locationwp.p2.SetValue(resetangle, 0)
		
		postdist2 = 40
		prex = safeloc[0] + postdist2*cos(bear*pi/180)
		prey = safeloc[1] + postdist2*sin(bear*pi/180)
		post2 = self.cord_System.toGPS([prex,prey,height])
		postloc = Locationwp().Set(post2[0],post2[1],height, 16)
		
		print 'Coordinates set with angle ',angle*180/3.1415, ' and distance ', (dist**2+height**2)**.5
		return [preloc,setangle,offloc,takephoto,post1,resetangle,postloc]

	# done
	def offAxis(self):
		self.set_MP_wps(self.offAxiswps)
		while(self.cs.wpno < 3):
			time.sleep(.1)
		print '1'
		self.speak('Attempting Off Axis')

		while(self.cs.wpno < 7):
			time.sleep(.01)

		time.sleep(1)		

		while(self.cs.wp_dist > 40):
			time.sleep(.01)

	# done
	def payloaddropSet(self):
		bear = 20 * pi/180
		dist = 20 #function of alt and vel
		height = 35

		windoffset  = 0

		windbearing = 0
				
		distprevious2 = 110
		prey = self.dropMeters[1] + distprevious2*sin(bear) + windoffset*sin(windbearing)
		prex = self.dropMeters[0] + distprevious2*cos(bear) + windoffset*cos(windbearing)
		pre = [prex,prey,height]
		preGPS = self.cord_System.toGPS(pre)
		pre = Locationwp().Set(preGPS[0],preGPS[1],preGPS[2], 16)

		distafter = -50
		posty = self.dropMeters[1] + distafter*sin(bear) + windoffset*sin(windbearing)
		postx = self.dropMeters[0] + distafter*cos(bear) +  windoffset*cos(windbearing)
		post = [postx,posty,height]
		postGPS = self.cord_System.toGPS(post)
		post = Locationwp().Set(postGPS[0],postGPS[1],postGPS[2], 16)

		dropy = self.dropMeters[1] + dist*sin(bear) + windoffset*sin(windbearing)
		dropx = self.dropMeters[0] + dist*cos(bear) +  windoffset*cos(windbearing)
		drop = [dropx,dropy,height]
		dropGPS = self.cord_System.toGPS(drop)
		drop = Locationwp().Set(dropGPS[0],dropGPS[1],dropGPS[2], 16)
		
		
		dropWP = Locationwp()
		Locationwp.id.SetValue(dropWP, 183)
		Locationwp.p1.SetValue(dropWP, 5) # servo number
		Locationwp.p2.SetValue(dropWP, 1100) # ms

		OpenWP = Locationwp()
		Locationwp.id.SetValue(dropWP, 183)
		Locationwp.p1.SetValue(dropWP, 5)
		Locationwp.p2.SetValue(dropWP, 1100)

		CloseWP = Locationwp()
		Locationwp.id.SetValue(dropWP, 183)
		Locationwp.p1.SetValue(dropWP, 5)
		Locationwp.p2.SetValue(dropWP, 1100)

		# return [pre, OpenWP, drop, dropWP, post]
		return [pre, drop, dropWP, post]

	# done
	def payloadDrop(self):
		self.set_MP_wps(self.dropwps)
		while(self.cs.wpno < 3):
			time.sleep(.1)

		self.speak('Payload dropped')

		while(self.cs.wpno < 4):
			time.sleep(.01)
		
		while(self.cs.wp_dist > 40):
			time.sleep(.01)


	# done
	def landSet(self):

		descent_ratio = 17.0/150.0 #20 meter descent for every 150 meters traveled
		alt1 = 40.5
		alt2 = 27
		bear = 20 * pi/180

		dist1 = alt1/descent_ratio
		dist2 = alt2/descent_ratio

		pre1 = [dist1*cos(bear),dist1*sin(bear),alt1]
		pre2 = [dist2*cos(bear),dist2*sin(bear),alt2]
		pre1 = self.cord_System.toGPS(pre1)
		pre2 = self.cord_System.toGPS(pre2)

		pre1 = Locationwp().Set(pre1[0],pre1[1],alt1, 16)
		pre2 = Locationwp().Set(pre2[0],pre2[1],alt2, 16)
		landing = Locationwp().Set(self.Home[0],self.Home[1],0,21)

		return [pre1,pre2,landing]

	# done
	def Land(self):
		self.set_MP_wps(self.landingwps)
		self.speak('Landing')

		while(self.cs.wpno < 3):
			time.sleep(.1)




	def searchGridSet(self):
		lst = []

		cam = Locationwp()
		Locationwp.id.SetValue(cam, 206)
		Locationwp.p1.SetValue(cam, 40.0)
		lst.append(cam)

		wpfileLoc = 'data/SearchGridWps.waypoints'
		with open(wpfileLoc,"r") as globallist:
		
			if (globallist.readline().split()[1] != "WPL"):
				print "Nothing found"
		
			else:
				dat = globallist.readline()
				while(len(dat) > 1):
					dat = globallist.readline().split("	")
					
					if (int(dat[3]) == 16):
						print "16"
						print dat[8],dat[9],dat[10]
						lst.append(Locationwp().Set(float(dat[8]),float(dat[9]),float(dat[10]), 16))
		
		cam = Locationwp()
		Locationwp.id.SetValue(cam, 206)
		Locationwp.p1.SetValue(cam, 0)
		lst.append(cam)

		return lst

	def emergentwpsSet(self):
		lst = []
		lst.append(Locationwp().Set(self.emergentloc[0],self.emergentloc[1],self.emergentloc[2], 16))

		cam = Locationwp()
		Locationwp.id.SetValue(cam, 203)

		lst.append(cam)
		return lst