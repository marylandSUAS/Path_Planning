import sys
import time
import os


Mission = True
# y = 1#Good
# r = 2#redo
# n = 3#bad
# stop = 4#break


def newPathInfo():
	with open('flight_information.txt',"r") as shortfile:
		dat = shortfile.readline().split(" ")
		# print dat
		if (dat[1] == "1"):
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
		os.system('./main.exe')

	time.sleep(.02)