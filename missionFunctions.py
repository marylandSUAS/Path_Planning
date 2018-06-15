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


		self.offAxisloc, self.emergentloc = self.getMissionData()
		# southern maryland
		# self.droploc = [38.3652078,-76.5366331,115]
		# competition
		self.droploc = [38.145842,-76.426375,115]
		self.dropMeters = self.cord_System.toMeters(self.droploc)
		self.dropbearing = 20 * pi/180
		self.dropwps = self.payloaddropSet()
		self.dropPlan = [True]
		self.dropPlan.extend([False]*(len(self.dropwps)-1))

		# southern maryland
		# self.offAxisloc = [38.3648986,-76.5373251,0.0]
		# competition
		# self.offAxisloc = [38.1476020,-76.4272070,100]
		self.offAxisheight = 200
		self.offAxisDist = 250
		self.offAxisbearing = -90 * pi/180
		self.LookRight = -1
		self.offAxisMeters = self.cord_System.toMeters(self.offAxisloc)
		self.offAxiswps = self.offAxisSet()
		self.offAxisPlan = [True]
		self.offAxisPlan.extend([False]*(len(self.offAxiswps)-1))


		# southern maryland
		# self.emergentloc = [38.3652078,-76.5366331,50]
		# competition
		# self.emergentloc = [38.1441594,-76.4251471,50]
		self.emergentMeters = self.cord_System.toMeters(self.emergentloc)
		self.emergentwps = self.emergentwpsSet()
		self.emergentPlan = [True]		
		# self.emergentPlan.extend([False]*(len(self.emergentPlan)-1))
		

		self.LandLoc = self.Home
		self.landbearing = -160 * pi/180
		self.landingwps = self.landSet()
		self.landingPlan = [False]*len(self.landingwps)


		self.TakeoffWps = self.takeoffSet()
		self.TakeoffPlan = [False]
		# self.takeoffPoint = []

		self.searchGridWps = self.searchGridSet()
		# self.searchGridPlan = [False]*len(self.searchGridWps)

		self.printMissionMeters()
		print "initalized mission functions"


	def speak(self,strin):
		MissionPlanner.MainV2.speechEngine.SpeakAsync(strin)		

	# done
	def set_MP_wps(self,wps):
		self.MAV.setWPTotal(len(wps)+1)	
		self.MAV.setWP(Locationwp().Set(self.Home[0],self.Home[1],self.Home[2], 16),0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)

		for i in range(len(wps)):
			Locationwp.alt.SetValue(wps[i], wps[i].alt * .3048)

			self.MAV.setWP(wps[i],1+i,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
			if (i+1 == 1):
				self.MAV.setWPCurrent(1)

		self.MAV.setMode("Auto")
		OFile = open('Path_Planning/GUI/waypoints.txt',"w")
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

		OFile = open('Path_Planning/GUI/waypoints.txt',"w")
		for i in range(len(wps)):
			if(i != 0):
				OFile.write(str('\n'))
			OFile.write(str(wps[i][0]))
			OFile.write(str(' '))
			OFile.write(str(wps[i][1]))
			OFile.write(str(' '))
			OFile.write(str(wps[i][2]))
		OFile.close()

	def getMissionData(self):
		OFile = open('Path_Planning/data/Mission_data.txt',"r")
		dat = []
		for i in range(4):
			temp = OFile.readline()
			# print temp
			dat.append(temp.split(' '))

		OFile.close()
		
		temp1 = [float(dat[2][1]),float(dat[2][2]),0.0]
		temp2 = [float(dat[3][1]),float(dat[3][2]),0.0]

		return temp1,temp2

	def printMissionMeters(self):
		OFile = open('Path_Planning/Gui/Mission_data.txt',"w")
		OFile.write(str(self.dropMeters[0])+' '+str(self.dropMeters[1]))
		OFile.write(str(self.offAxisMeters[0])+' '+str(self.offAxisMeters[1]))
		OFile.write(str(self.emergentMeters[0])+' '+str(self.emergentMeters[1]))
		OFile.close()


	# done
	def takeoffSet(self):
		to = Locationwp()
		Locationwp.id.SetValue(to, 22)
		Locationwp.p1.SetValue(to, 15)
		Locationwp.alt.SetValue(to, 100)
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
		
		bear = self.offAxisbearing
		LookRight = self.LookRight

		safeloc = [self.offAxisMeters[0]+LookRight*dist*cos(bear*pi/180),
					self.offAxisMeters[1]+LookRight*dist*sin(bear*pi/180),
					height]

		predist = -150
		prex = safeloc[0] + predist*cos((bear+90)*pi/180)
		prey = safeloc[1] + predist*sin((bear+90)*pi/180)

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
		prex = safeloc[0] + after1dist*cos((bear+90)*pi/180)
		prey = safeloc[1] + after1dist*sin((bear+90)*pi/180)
		post1 = self.cord_System.toGPS([prex,prey,height])
		post1 = Locationwp().Set(post1[0],post1[1],height, 16)
				
		resetangle = Locationwp()
		Locationwp.id.SetValue(resetangle, 205)
		Locationwp.p2.SetValue(resetangle, 0)
		
		postdist2 = 40
		prex = safeloc[0] + postdist2*cos((bear+90)*pi/180)
		prey = safeloc[1] + postdist2*sin((bear+90)*pi/180)
		post2 = self.cord_System.toGPS([prex,prey,height])
		postloc = Locationwp().Set(post2[0],post2[1],height, 16)

		# print 'Coordinates set with angle ',angle*180/3.1415, ' and distance ', (dist**2+height**2)**.5

		return [preloc,setangle,offloc,post1,resetangle,postloc]#,self.cord_System.MetertoWp(self.offAxisMeters)]

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
		bear = self.dropbearing + pi
		dist = 110.0 #function of alt and vel
		height = 115.0

		windoffset  = 0

		windbearing = 0
				
		distprevious2 = 250.0
		prey = self.dropMeters[1] + (distprevious2+dist)*sin(bear)
		prex = self.dropMeters[0] + (distprevious2+dist)*cos(bear)
		pre = [prex,prey,height]
		preGPS = self.cord_System.toGPS(pre)
		pre = Locationwp().Set(preGPS[0],preGPS[1],preGPS[2], 16)

		distafter = -120.0
		posty = self.dropMeters[1] + (distafter+dist)*sin(bear)
		postx = self.dropMeters[0] + (distafter+dist)*cos(bear)
		post = [postx,posty,height]
		postGPS = self.cord_System.toGPS(post)
		post = Locationwp().Set(postGPS[0],postGPS[1],postGPS[2], 16)

		dropy = self.dropMeters[1] + dist*sin(bear)
		dropx = self.dropMeters[0] + dist*cos(bear)
		drop = [dropx,dropy,height]
		dropGPS = self.cord_System.toGPS(drop)
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
		# return [pre, drop, dropWP, post]

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

		alt1 = 150
		alt2 = 65
		alt3 = 36

		bear = self.landbearing

		dist1 = 800
		dist2 = 550
		dist3 = 350

		pre1 = [dist1*cos(bear),dist1*sin(bear),alt1]
		pre2 = [dist2*cos(bear),dist2*sin(bear),alt2]
		pre3 = [dist3*cos(bear),dist3*sin(bear),alt3]

		pre1 = self.cord_System.toGPS(pre1)
		pre2 = self.cord_System.toGPS(pre2)
		pre3 = self.cord_System.toGPS(pre3)

		pre1 = Locationwp().Set(pre1[0],pre1[1],alt1, 16)
		pre2 = Locationwp().Set(pre2[0],pre2[1],alt2, 16)
		pre3 = Locationwp().Set(pre3[0],pre3[1],alt3, 16)
		landing = Locationwp().Set(self.Home[0],self.Home[1],0,21)

		return [pre1,pre2,pre3,landing]

	# done
	def Land(self):
		self.set_MP_wps(self.landingwps)
		self.speak('Landing')

		while(self.cs.wpno < 3):
			time.sleep(.1)


	def searchGridSet(self):
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

		self.searchGridPlan = [True,False,True,False,True,
							False,True,False,True,False,
							True,False,True,False,False]

		# print lst
		return lst


	def emergentwpsSet(self):
		lst = []
		lst.append(Locationwp().Set(self.emergentloc[0],self.emergentloc[1],self.emergentloc[2], 16))

		cam = Locationwp()
		Locationwp.id.SetValue(cam, 203)

		# lst.append(cam)
		return lst