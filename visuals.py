#!/usr/bin/env python

import rospy
import pygame
from math import pi
import Cord_System




class visual:

    def __init__(self,start):
        self.pygame.init()
        
        self.size = [400, 300]
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Example code for the draw module")


        self.dlng = (pi/180)*rad_Earth*cos(start[0]*pi/180);
        
    def draw_mission(self,mission):

        self.WPs = []
        self.drop = []
        self.bounds = []
        self.grid = []
        self.offAxis = []
        scale = .5
        wps = mission.WPs*scale
        dropPoint = mission.drop*scale
        boundry = mission.bounds*scale
        search_grid = mission.grid*scale
        offAxis = mission.offAxis*scale
        emergent = mission.Emergent*scale
        
        # Clear the screen and set the screen background
        self.screen.fill(WHITE)
        
        self.pygame.draw.polygon(screen, [100,100,100], boundry, 5)

        self.pygame.draw.polygon(screen, [255,0,255], search_grid, 5)
        
        self.pygame.draw.lines(self.screen, [255,255,0], False, wps, 5)
        
        for pnt in wps:
            pygame.draw.circle(screen, BLUE, pnt, 10)
        
        pygame.draw.circle(screen, BLUE, offAxis, 10)
        pygame.draw.circle(screen, BLUE, emergent, 10)
        pygame.draw.circle(screen, BLUE, dropPoint, 10)
        
        

        pygame.draw.arc(screen, RED,  [210, 75, 150, 125], 3*pi/2, 2*pi, 2)
        

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

        '''
        clock = pygame.time.Clock()
        
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)
         
        
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
     
        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.
         
        
        # Draw on the screen a GREEN line from (0,0) to (50.75) 
        # 5 pixels wide.
        pygame.draw.line(screen, GREEN, [0, 0], [50,30], 5)
     
        # Draw on the screen a GREEN line from (0,0) to (50.75) 
        # 5 pixels wide.
        pygame.draw.lines(screen, BLACK, False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)
        
        # Draw on the screen a GREEN line from (0,0) to (50.75) 
        # 5 pixels wide.
        pygame.draw.aaline(screen, GREEN, [0, 50],[50, 80], True)

        # Draw a rectangle outline
        pygame.draw.rect(screen, BLACK, [75, 10, 50, 20], 2)
         
        # Draw a solid rectangle
        pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])
         
        # Draw an ellipse outline, using a rectangle as the outside boundaries
        pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2) 

        # Draw an solid ellipse, using a rectangle as the outside boundaries
        pygame.draw.ellipse(screen, RED, [300, 10, 50, 20]) 
     
        # This draws a triangle using the polygon command
        
        # Draw an arc as part of an ellipse. 
        # Use radians to determine what angle to draw.
        pygame.draw.arc(screen, BLACK,[210, 75, 150, 125], 0, pi/2, 2)
        pygame.draw.arc(screen, GREEN,[210, 75, 150, 125], pi/2, pi, 2)
        pygame.draw.arc(screen, BLUE, [210, 75, 150, 125], pi,3*pi/2, 2)
        
        # Draw a circle
        
        
        
        '''
         
    def exit(self):
        self.pygame.quit()
