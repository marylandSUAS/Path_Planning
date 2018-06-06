import math
from math import cos, pi

import MissionPlanner
from MissionPlanner.Utilities import Locationwp
import MAVLink

# GPS Meter Converter
# All conversions are done 
	# north is positive Y
	# east is positive X

class Cord_System:

	def __init__(self,start):
		self.Home = start
		rad_Earth = 6378160.0
		self.dlng = (pi/180)*rad_Earth*cos(start[0]*pi/180);
		self.dlat = (pi/180)*rad_Earth
		# d's are large
		# print 1/self.dlat
		# print 1/self.dlng

	def MetertoWp(self,meter):
		tempGPS = self.toGPS(meter)
		temp = Locationwp().Set(tempGPS[0],tempGPS[1],tempGPS[2], 16)
		return temp

	def GPStoWp(self,GPS):
		temp = Locationwp().Set(GPS[0],GPS[1],GPS[2], 16)
		return temp

	def toMeters(self,GPS): 
		x = (GPS[1]-self.Home[1])*self.dlng
		y = (GPS[0]-self.Home[0])*self.dlat
		if(len(GPS) == 4):
			return [x,y,GPS[2],GPS[3]]
		else:
			return [x,y,GPS[2]]

	def toGPS(self,Meters):
		lng = (Meters[0]/self.dlng)+self.Home[1]
		lat = (Meters[1]/self.dlat)+self.Home[0]
		if(len(Meters) == 4):
			return [lat,lng,Meters[2],Meters[3]]
		else:
			return [lat,lng,Meters[2]]


# test = Cord_System([39.0829973,-76.9045262,100.0])

# GPSpoint = [39.0836885,-76.9029611,50.0]

# Meterspoint = [50,50,50]

# print 'OGpoint: ',GPSpoint
# one = test.toMeters(GPSpoint)
# print one
# two = test.toGPS(one)
# print 'Meters:  ',two
