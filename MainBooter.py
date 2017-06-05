import sys
import time
import os


Mission = True
y = 1#Good
r = 2#redo
n = 3#bad
stop = 4#break

global checkpath
checkpath = 'M:/Autopilot/Dstar/senario.txt'

def newPathInfo():
	with open(checkpath,"r") as File:
		dat = File.readline()
		if (dat == "1"):
			return True
		#elif(dat == "0"):
			#return False
		#else:
			#print "neither choices found"
		return False

while(Mission)
	if(newPathInfo)
		print "Running up Dstar"
		os.system('./main.exe')

		'''
		while(True):
			temp = input("Looks good? y = yes, r = redo, n = no good")
			if (temp == y):
				print "Continuing"
				break
			elif(temp == r):
				print "retrying"	
				break
			elif (temp == n):
				print ":("
				break
			elif (temp == stop):
				break
				Mission = False
			else:
				print "Try again"
		'''

	time.sleep(.5)

	