import sys
import time
import os


Mission = True

def newPathInfo():
	with open('dlite/flight_information.txt',"r") as shortfile:
		dat = shortfile.readline().split(' ')
		print dat
		if (float(dat[1]) == 1):
			return True
	return False

counter = 0
while(Mission):
	if (counter == 100):
		counter = 0
		print 'Waiting for scenario'
	counter = counter + 1

	if(newPathInfo()):
		print "Running up Dstar"
		os.system('./dlite/main.exe')
		print 'finished dlite'

	time.sleep(.1)