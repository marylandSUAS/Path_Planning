#!/usr/bin/env python

import rospy
import math
from math import cos, pi



def toMeters(GPS): 
	start = [38.1459, -76.4264]
	rad_Earth = 20909000.0
	dlng = (pi/180)*rad_Earth*cos(38.1459*pi/180);
	dlat = (pi/180)*rad_Earth
	
	x = (GPS[1]-start[1])*dlng
	y = (GPS[0]-start[0])*dlat
	if len(GPS < 3):
		return [x,y]
	else:
		return [x,y,GPS[2]]

def toGPS(Meters):
	start = [38.1459, -76.4264]
	rad_Earth = 20909000.0
	dlng = (pi/180)*rad_Earth*cos(38.1459*pi/180);
	dlat = (pi/180)*rad_Earth
	
	lng = (Meters[0]/dlng)+start[1]
	lat = (Meters[1]/dlat)+start[0]
	if len(Meters < 3):
		return [x,y]
	else:
		return [lat,lng,Meters[2]]

def toMeters_list(gps)
	temp = []
	for pnt in gps:
		temp.append(toMeters(pnt))
	return temp

def toGPS_list(meters)
	temp = []
	for pnt in meters:
		temp.append(toMeters(pnt))
	return temp

class Waypoint():
	def __init__(self,id=16,loc = None,id1=0,id2=0,id3=0,id4=0,id5=0,id6=0,id7=0,id8=0):
		self.Location = loc
		self.Location = loc
		self.prev_loc = []
		self.avoid = True
		self.id = 16
		self.param1 = id1
		self.param2 = id2
		self.param3 = id3
		self.param4 = id4
		self.param5 = id5
		self.param6 = id6
		self.param7 = id7
		self.param8 = id8
		self.intermediate = False
		# photos,photo
		self.actions = None
		self.actions_loc = None
		# self.WP_num = 0

class Mission_Profile:
	def __init__(self,mission):
		self.Mission = mission
		self.path = []
		# wps, drop, offAxis, emergent, grid 
		self.order = ['wps','drop','offAxis','emergent','grid']
		


class Mission:

	def __init__(self,start,mission_loc):

		self.home = []
		self.WPs = []
		self.drop = []
		self.bounds = []
		self.grid = []
		self.offAxis = []
		self.Emergent = []
		self.Obstacles = []

		if mission_file is None:
			self.mission_loc = 'missions/current_mission.txt'
		else:
			self.mission_loc = mission_file

		self.mission_call()


	def mission_call(self):
		with open(self.mission_loc,'r') as missionFile:
			
			
			self.home = map(float,missionFile.readline().split(' '))
			
			self.drop = [0.0,0.0]

			self.offAxis = self.toMeters(map(float,missionFile.readline().split(' '))self.home)

			self.Emergent = self.toMeters(map(float,missionFile.readline().split(' ')),self.home)
			
			temp = missionFile.readline().split(',')
			for pnt in temp:
				self.WPs.append(toMeters(map(float,pnt.split(' ')),self.home))

			temp = missionFile.readline().split(',')
			for pnt in temp:
				self.bounds.append(toMeters(map(float,pnt.split(' ')),self.home))

			temp = missionFile.readline().split(',')
			for pnt in temp:
				self.grid.append(toMeters(map(float,pnt.split(' ')),self.home))
			
			temp = missionFile.readline().split(',')
			for pnt in temp:
				self.Obstacles.append(toMeters(map(float,pnt.split(' ')),self.home))
			
			# mission_file.readlines()

		
	def toMeters(self,GPS,start): 
		start = [38.1459, -76.4264]
		rad_Earth = 20909000.0
		dlng = (pi/180)*rad_Earth*cos(38.1459*pi/180);
		dlat = (pi/180)*rad_Earth
		
		x = (GPS[1]-start[1])*dlng
		y = (GPS[0]-start[0])*dlat
		return [x,y,GPS[2]]

	def toGPS(self,Meters,start):
		start = [38.1459, -76.4264]
		rad_Earth = 20909000.0
		dlng = (pi/180)*rad_Earth*cos(38.1459*pi/180);
		dlat = (pi/180)*rad_Earth
		
		lng = (Meters[0]/dlng)+start[1]
		lat = (Meters[1]/dlat)+start[0]
		return [lat,lng,Meters[2]]


def getMission(loc):

	print "Service call failed"



	if loc is not None:
		missionFileLoc = 'missions/current_mission.txt'
	else:
		missionFileLoc = 'missions/'+loc
	# drop
	# offAxis
	# Emergent
	# WPs
	# grid
	# bounds
	# Obstacles
	with open(loc,'w') as missionFile:

			missionFile.write(' '.join(map(str, drop)))
			missionFile.write(' '.join(map(str, offAxis)))
			missionFile.write(' '.join(map(str, Emergent)))

			temp = []
			for pnt in WPs:
				temp.append(' '.join(map(str, pnt)))
			missionFile.write(','.join(temp))
			
			temp = []
			for pnt in grid:
				temp.append(' '.join(map(str, pnt)))
			missionFile.write(','.join(temp))
			
			temp = []
			for pnt in bounds:
				temp.append(' '.join(map(str, pnt)))
			missionFile.write(','.join(temp))
			
			temp = []
			for pnt in Obstacles:
				temp.append(' '.join(map(str, pnt)))
			missionFile.write(','.join(temp))
			
			# File_object.writelines(L) for L = [str1, str2, str3] 




class visual:

    def __init__(self,start):
        self.pygame.init()
        self.scale = .5
        self.size = [1280, 720]

        self.screen = pygame.display.set_mode(size)
        # pygame.display.set_caption("Example code for the draw module")


    
    def draw_mission(self,mission):
    	self.screen.fill(WHITE)
    	self.draw_mission_class(self,mission)
    	self.pygame.display.flip()

    def draw_mission_profile(self,mission,mission_profle):
		self.screen.fill(WHITE)
    	self.draw_mission_class(mission)
    	self.draw_mission_prof(mission_profle)
    	self.pygame.display.flip()

    def draw_mission_prof(mission_profle):
    	pass

    def draw_mission_class(self,mission):

 		BLACK = ( 0, 0, 0)
		WHITE = (255, 255, 255)
		GREEN = (0, 255, 0)
		RED = ( 255, 0, 0)
        
        wps = mission.WPs*self.scale
        dropPoint = mission.drop*self.scale
        boundry = mission.bounds*self.scale
        search_grid = mission.grid*self.scale
        offAxis = mission.offAxis*self.scale
        emergent = mission.Emergent*self.scale
        obstacles = mission.Obstacles*self.scale
        
        # Clear the screen and set the screen background
        
        
        self.pygame.draw.polygon(screen, (255,200,200), boundry, 5)

        self.pygame.draw.polygon(screen, (200,200,200), search_grid, 5)
        
        self.pygame.draw.lines(self.screen, (50,50,255), False, wps, 5)
        
        for pnt in wps:
            pygame.draw.circle(screen, (50,50,255), pnt, 5)
        
        pygame.draw.circle(screen, (255,0,0), offAxis, 10)
        pygame.draw.circle(screen, (0,255,0), emergent, 10)
        pygame.draw.circle(screen, (0,0,0), dropPoint, 10)

        for obs in obstacles:
			pygame.draw.circle(screen, (0,0,0), obs[1:2], obs[4])        	

        
        

        # pygame.draw.arc(screen, (255,255,0),  [210, 75, 150, 125], 3*pi/2, 2*pi, 2)
        
        # myfont = pygame.font.SysFont('Comic Sans MS', 30)
        # textsurface = myfont.render('Some Text', False, (0, 0, 0))
        # self.screen.blit(textsurface,(0,0))


        # clock = pygame.time.Clock()
        # clock.tick(10)
         
        
        # for event in pygame.event.get(): # User did something
        #     if event.type == pygame.QUIT: # If user clicked close
        #         done=True # Flag that we are done so we exit this loop
     
         
        
        # pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
        # pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2) 
        # pygame.draw.ellipse(screen, RED, [300, 10, 50, 20]) 
        # pygame.draw.arc(screen, BLACK,[210, 75, 150, 125], 0, pi/2, 2)
         
    def exit(self):
        self.pygame.quit()


