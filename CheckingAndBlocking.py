import re

smoothPathFile = open('smooth_path.txt', 'r')
newFlightInformationFile = open('new_flight_information.txt', 'w')
flightInformationFile = open('flight_information.txt', 'r')

collisions = {}
waypointList = smoothPathFile.readlines()
obstacleList = flightInformationFile.readlines()

coordSearch = re.compile('\w*\.\w*')
tagSearch = re.compile('^[a-z]*')

def getCoords(inputLine):
    return([float(n) for n in re.findall(coordSearch, inputLine)])

def distPointLine(obstacle, waypoint):
    px = getCoords(waypoint)[0]
    py = getCoords(waypoint)[1]
    pz = getCoords(waypoint)[2]
    
    q1x = getCoords(obstacle)[0]
    q1y = getCoords(obstacle)[1]
    q1z = getCoords(obstacle)[2]
    
    q2x = getCoords(obstacle)[3]
    q2y = getCoords(obstacle)[4]
    q2z = getCoords(obstacle)[5]
    
    return(
        (((px-q1x)*(q1y-q2y) - (py-q1y)*(q1x-q2x))**2 + \
        ((px-q1x)*(q1z-q2z) - (pz-q1z)*(q1x-q2x))**2 + \
        ((py-q1y)*(q1z-q2z) - (pz-q1z)*(q1y-q2y))**2)**(1/2) / \
        ((q1x-q2x)**2 + (q1y-q2y)**2 + (q1z-q2z)**2)**(1/2))

def distLineLine(obstacle, waypoint1, waypoint2):
    p1x = getCoords(waypoint1)[0]
    p1y = getCoords(waypoint1)[1]
    p1z = getCoords(waypoint1)[2]

    p2x = getCoords(waypoint2)[0]
    p2y = getCoords(waypoint2)[1]
    p2z = getCoords(waypoint2)[2]
    
    q1x = getCoords(obstacle)[0]
    q1y = getCoords(obstacle)[1]
    q1z = getCoords(obstacle)[2]
    
    q2x = getCoords(obstacle)[3]
    q2y = getCoords(obstacle)[4]
    q2z = getCoords(obstacle)[5]

    return(
        ((((p1x-p2x)*(q1y-q2y) - (p1y-p2y)*(q1x-q2x))*(p1z-q1z) - \
        ((p1x-p2x)*(q1z-q2z) - (p1z-p2z)*(q1x-q2x))*(p1y-q1y) + \
        ((p1y-p2y)*(q1z-q2z) - (p1z-p2z)*(q1y-q2y))*(p1x-q1x))**2)**(1/2) / \
        (((p1x-p2x)*(q1y-q2y) - (p1y-p2y)*(q1x-q2x))**2 + \
        ((p1x-p2x)*(q1z-q2z) - (p1z-p2z)*(q1x-q2x))**2 + \
        ((p1y-p2y)*(q1z-q2z) - (p1z-p2z)*(q1y-q2y))**2)**(1/2))

def distLineVerticalLine(obstacleX, obstacleY, waypoint1, waypoint2):
    p1x = getCoords(waypoint1)[0]
    p1y = getCoords(waypoint1)[1]
    p1z = getCoords(waypoint1)[2]
    p2x = getCoords(waypoint2)[0]
    p2y = getCoords(waypoint2)[1]
    p2z = getCoords(waypoint2)[2]

    q1x = obstacleX
    q1y = obstacleY

    return(
        (((p1x-p2x)*(p1y-q1y) - (p1y-p2y)*(p1x-q1x))**2)**(1/2) / \
        ((p1x-p2x)**2 + (p1y-p2y)**2)**(1/2))

def component(obstacle, waypoint):
    px = getCoords(waypoint)[0]
    py = getCoords(waypoint)[1]
    pz = getCoords(waypoint)[2]

    q1x = getCoords(obstacle)[0]
    q1y = getCoords(obstacle)[1]
    q1z = getCoords(obstacle)[2]
    
    q2x = getCoords(obstacle)[3]
    q2y = getCoords(obstacle)[4]
    q2z = getCoords(obstacle)[5]

    return(
        ((q1x-q2x)*(q1x/2-px+q2x/2) + (q1y-q2y)*(q1y/2-py+q2y/2) + \
        (q1z-q2z)*(q1z/2-pz+q2z/2)) / ((q1x-q2x)**2+(q1y-q2y)**2 + \
        (q1z - q2z)**2)**(1/2))  

#Check to see if any smooth path waypoint is in an obstacle
for waypoint in smoothPathFile:
    for obstacle in obstacleList:
        if re.findall(tagSearch, obstacle)[0] == 'static':
            distance = ((getCoords(waypoint)[0] - \
                         getCoords(obstacle)[0])**2 + \
                         (getCoords(waypoint)[1] - \
                         getCoords(obstacle)[1])**2)**(1/2)
            if distance < getCoords(obstacle)[4] and \
            getCoords(waypoint)[3] < \
            getCoords(obstacle)[3]:
                collisions[obstacle] = distance
        if re.findall(tagSearch, obstacle)[0] == 'dynamic':
            if distPointLine(obstacle, waypoint) < \
            getCoords(obstacle)[6] and \
            ((getCoords(waypoint)[0] - \
            (getCoords(obstacle)[0] + \
            getCoords(obstacle)[3])/2)**2 + \
            (getCoords(waypoint)[1] - \
            (getCoords(obstacle)[1] + \
            getCoords(obstacle)[4])/2)**2 + \
            (getCoords(waypoint)[2] - \
            (getCoords(obstacle)[2] + \
            getCoords(obstacle)[5])/2)**2)**(1/2) < \
            getCoords(obstacle)[6] + \
            ((getCoords(obstacle)[0] - \
            getCoords(obstacle)[3])**2 + \
            (getCoords(obstacle)[1] - \
            getCoords(obstacle)[4])**2 + \
            (getCoords(obstacle)[2] - \
            getCoords(obstacle)[5])**2)**(1/2)/2: 
                collisions[obstacle] = distPointLine(obstacle, waypoint)

#Check if line connecting smooth path waypoints is too close to obstacle
for n in range(len(waypointList) - 1):
    for obstacle in obstacleList:
        if re.findall(tagSearch, obstacle)[0] == 'static':
            distance = distLineVerticalLine(
                obstacleX=getCoords(obstacle)[0],
                obstacleY=getCoords(obstacle)[1],
                waypoint1=waypointList[n],
                waypoint2=waypointList[n + 1])
            if  distance < getCoords(obstacle)[3] and \
            getCoords(waypointList[n])[2] < getCoords(obstacle)[2] and \
            getCoords(waypointList[n + 1])[2] < getCoords(obstacle)[2]:
                collisions[obstacle] = distance
        if re.findall(tagSearch, obstacle)[0] == 'dynamic':
            if distLineLine(obstacle, waypointList[n],
            waypointList[n+1]) < getCoords(obstacle)[6] and \
            (component(obstacle, waypointList[n]) < \
            getCoords(obstacle)[6] + \
            ((getCoords(obstacle)[0] - \
            getCoords(obstacle)[3])**2 + \
            (getCoords(obstacle)[1] - \
            getCoords(obstacle)[4])**2 + \
            (getCoords(obstacle)[2] - \
            getCoords(obstacle)[5])**2)**(1/2)/2 or \
            component(obstacle, waypointList[n+1]) < \
             getCoords(obstacle)[6] + \
            ((getCoords(obstacle)[0] - \
            getCoords(obstacle)[3])**2 + \
            (getCoords(obstacle)[1] - \
            getCoords(obstacle)[4])**2 + \
            (getCoords(obstacle)[2] - \
            getCoords(obstacle)[5])**2)**(1/2)/2):
                collisions[obstacle] = distLineLine(
                    obstacle=obstacle,
                    waypoint1=waypointList[n],
                    waypoint2=waypointList[n+1])

if len(collisions) > 0:
    for obstacle in collisions:
        if re.findall(tagSearch, obstacle)[0] == 'static':
            newFlightInformationFile.write(
                "stati" + re.findall('c\d*', obstacle)[0] + " " + \
                str(getCoords(obstacle)[0]) + " " + \
                str(getCoords(obstacle)[1]) + " " + \
                str(getCoords(obstacle)[2]) + " " + \
                str((2*getCoords(obstacle)[3]) - \
                collisions[obstacle]) + '\n')
        if re.findall(tagSearch, obstacle)[0] == 'dynamic':
            newFlightInformationFile.write(
                "dynami" + re.findall('c\d*', obstacle)[0] + " " + \
                str(getCoords(obstacle)[0]) + " " + \
                str(getCoords(obstacle)[1]) + " " + \
                str(getCoords(obstacle)[2]) + " " + \
                str(getCoords(obstacle)[3]) + " " + \
                str(getCoords(obstacle)[4]) + " " + \
                str(getCoords(obstacle)[5]) + " " + \
                str((2*int(getCoords(obstacle)[6])) - \
                collisions[obstacle]) + '\n')

smoothPathFile.close()
flightInformationFile.close()
newFlightInformationFile.close()

