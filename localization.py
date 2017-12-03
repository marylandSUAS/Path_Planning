import math

xVels = [0,0,0,0,0]
yVels = [0,0,0,0,0]
ZVels = [0,0,0,0,0]

thetas = [0,0,0,0,0]
phis = [0,0,0,0,0]

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

