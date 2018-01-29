import math
import time
import threading



class movingObs:
	def __init__(self,fileReadLoc):
		self.fileLoc = fileReadLoc
		self.loger = threading.Thread(target=self.run)
		self.Reading = False

		# read file
		# make new objects for each file
		self.moving_Obstacles = []

		self.hz = 2

	def start(self):
		self.Reading = True
		self.loger.start()

	def stop():
		self.Reading = False

	def run():
		while(self.Reading):
			with open(self.fileLoc,"r") as ob_File:
				for i in range(size(self.moving_Obstacles)) 
					Ob_data = ob_File.readline().split(" ")
					self.moving_Obstacles(i).addXVelocity(Ob_data(1))
					self.moving_Obstacles(i).addYVelocity(Ob_data(2))
					self.moving_Obstacles(i).addZVelocity(Ob_data(3))

			time.sleep(self.hz)


	# is called by avoidance script to check if any obstacles might interfere.  If so it call in the obstacle
	# locate itself and return the position as a function of position and velocity at closest approach
	def check_for_collision(self,pos,vel,goal):
		potential_obstacles = []
		# check each obstacle for collision
		# return obstacles that might and where



class dynamics_Ob:
	def __init__(self,hertz):


		self.xVels = [0,0,0,0,0,0,0,0,0,0]
		self.yVels = [0,0,0,0,0,0,0,0,0,0]
		self.ZVels = [0,0,0,0,0,0,0,0,0,0]
		self.Vels = [0,0,0,0,0,0,0,0,0,0]

		self.thetas = [0,0,0]
		self.phis = [0,0,0]

		self.top_speed = 0
		self.slow_speed = 1000

		self.hz = hertz






	def addLoc(self,X,Y,Z):
	# def addLoc(X,Y,Z,time):
		update_lists(X,Y,Z)
		update_angles()



	def update_lists(self,X,Y,Z):
		self.xVels.pop()
		self.yVels.pop()
		self.zVels.pop()
		self.xVels.append(0,X)
		self.yVels.append(0,Y)
		self.zVels.append(0,Z)
		temp_V = math.sqrt((self.xVels[0]-self.xVels[1])**2 + (self.yVels[0]-self.yVels[1])**2 + (self.zVels[0]-self.zVels[1])**2)
		self.Vels.pop()
		self.Vels.append(0,temp_V)
		
		if (temp_V < slow_speed):
			slow_speed = temp_V
		elif (temp_V > top_speed):
			top_speed = temp_V
		# average last 30s
		
	def update_angles(self):
		# find angles/ set last angle

	def check_for_node(self):
		# if node is not within error
		# log node
		# log last angles







	def addXVelocity(vel):
		temp = xVels[1:len(xVels)]
		temp.append(vel)
		xVels = temp

	def addYVelocity(vel):
		temp = yVels[1:len(yVels)]
		temp.append(vel)
		yVels = temp

	def addZVelocity(vel):
		temp = zVels[1:len(zVels)]
		temp.append(vel)
		zVels = temp

	def addXVelocity(theta):
		temp = thetas[1:len(thetas)]
		temp.append(theta)
		thetas = temp

	def addXVelocity(phi):
		temp = phis[1:len(phis)]
		temp.append(phi)
		phis = temp

	def getVelocityX(initX, finalX, deltaTime):
		return (finalX - initX)//deltaTime

	def getVelocityY(initY, finalY, deltaTime):
		return (finalY - initY)//deltaTime

	def getVelocityZ(initZ, finalZ, deltaTime):
		return (finalZ - initZ)//deltaTime

	def getVelocity(initX, finalX, initY, finalY, initZ, finalZ, deltaTime):
		return math.sqrt(getVelocityX(initX, finalX, deltaTime)**2 + getVelocityY(initY, finalY, deltaTime)**2 + getVelocityZ(initZ, finalZ, deltaTime)**2)

	def getTheta(initX, finalX, initY, finalY, initZ, finalZ, deltaTime):
		velX = (finalX - initX)//deltaTime
		velY = (finalY - initY)//deltaTime
		return math.atan(velY/velX)

	def getPhi(initY, finalY, initZ, finalZ, deltaTime):
		velY = (finalY - initY)//deltaTime
		velZ = (finalZ - initZ)//deltaTime
		return math.atan(velZ/velY)

	def getProjectedX(initX, finalX, initY, finalY, initZ, finalZ, deltaTime, projectedTime):
		return getVelocityX() * projectedTime * math.cos(getTheta(initX, finalX, initY, finalY, initZ, finalZ, deltaTime))

	def getProjectedY(initX, finalX, initY, finalY, initZ, finalZ, deltaTime, projectedTime):
		return getVelocityY() * projectedTime * math.sin(getTheta(initX, finalX, initY, finalY, initZ, finalZ, deltaTime))

	def getProjectedZ(initX, finalX, initY, finalY, initZ, finalZ, deltaTime, projectedTime):
		return getVelocityZ() * projectedTime * math.cos(getPhi(initX, finalX, initY, finalY, initZ, finalZ, deltaTime))

