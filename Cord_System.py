import math
from math import cos, pi
# GPS Meter Converter
# All conversions are done 
	# north is positive Y
	# east is positive X
class Cord_System:

	def __init__(self,start):
		self.Home = start
		rad_Earth = 6378160
		self.dlng = (pi/180)*rad_Earth*cos(start[0]*pi/180);
		self.dlat = (pi/180)*rad_Earth
		# print 1/self.dlat
		# print 1/self.dlng

	def toMeters(self,GPS):
		x = (GPS[1]-self.Home[1])/self.dlng;
		y = (GPS[0]-self.Home[0])/self.dlat;
		
		return [x,y,GPS[2]]


	def toGPS(self,Meters):
		lng = Meters[0]/self.dlng;
		lat = Meters[1]/self.dlat;
		
		return [lat,lng,Meters[2]]


# test = Cord_System([72,-46,0])

# GPSpoint = [.0001,.0001,50]
# Meterspoint = [50,50,50]

# print test.toMeters(GPSpoint)
# print test.toGPS(Meterspoint)