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


sys.path.append('C:\Users\derek_000\Documents\Python27\Lib')


class Avoider:
	
	def __init__(self,start):
		self.dataPath = 'dstar/flight_information.txt'		

		self.Safety = 6
		self.cruise = 16



	def getPath(loc,loc2,Moving,timeout):
	if (Moving == False):

	else:



	def getMovingObstacles(self,WPlst,TimeToStart):
		Time = 0	#dist_CS(lst[0])/self.cruise 
		timeError = 1
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
				closestplus,locplus = dcaAddtime(Pos1,Vel1,Pos2,Vel2,Time+timeError)
				closestmin,locmin = dcaAddtime(Pos1,Vel1,Pos2,Vel2,Time-timeError)

				print closest,'	',loc,'	',movObs[j][3]+self.Safety
				if (closest < movObs[j][3]+self.Safety or closestplus < movObs[j][3]+self.Safety or closestmin < movObs[j][3]+self.Safety):
					loc.append(movObs[j][3]+self.Safety)
					locplus.append(movObs[j][3]+self.Safety)
					locmin.append(movObs[j][3]+self.Safety)

					ImportantmovObs.append(loc)
					ImportantmovObs.append(locplus)
					ImportantmovObs.append(locmin)

		Time = Time + dist_list(WPlst[i],WPlst[i+1])/self.cruise

		return ImportantmovObs


	def startSenario(self,wps,moving):
		