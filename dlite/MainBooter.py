import sys
import time
import os


Mission = True

def newPathInfo():
	with open('flight_information.txt',"r") as shortfile:
		dat = shortfile.readline().split(' ')
		print dat
		if (float(dat[1]) == 1):
			return True
	return False

while(Mission):
	if(newPathInfo()):
		print "Running up Dstar"
		os.system('./main.exe')
		print 'finished dlite'

	time.sleep(.1)