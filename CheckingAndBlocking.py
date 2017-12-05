import re

smoothPathFile = open('smooth_path.txt', 'r')
newFlightInformationFile = open('flight_information_new.txt', 'w')
flightInformationFile = open('flight_information.txt', 'r')

collisions = {}
waypointList = smoothPathFile.readlines()

coordSearch = re.compile('\w\b\.\w*')
tagSearch = re.compile('^[a-z]*')

def distPointLine(obstacle, waypoint):
    px = re.findall(coordSearch, waypoint)[0]
    py = re.findall(coordSearch, waypoint)[1]
    pz = re.findall(coordSearch, waypoint)[2]
    
    q1x = re.findall(coordSearch, obstacle)[0]
    q1y = re.findall(coordSearch, obstacle)[1]
    q1z = re.findall(coordSearch, obstacle)[2]
    
    q2x = re.findall(coordSearch, obstacle)[3]
    q2y = re.findall(coordSearch, obstacle)[4]
    q2z = re.findall(coordSearch, obstacle)[5]
    
    return((((px - q1x)*(q1y - q2y) - (py - q1y)*(q1x - q2x))^2 + ((px - q1x)*(q1z - q2z) - (pz - q1z)*(q1x - q2x))^2 + ((py - q1y)*(q1z - q2z) - (pz - q1z)*(q1y - q2y))^2)^(1/2)/((q1x - q2x)^2 + (q1y - q2y)^2 + (q1z - q2z)^2)^(1/2))

def distLineLine(obstacle, waypoint1, waypoint2):
    p1x = re.findall(coordSearch, waypoint1)[0]
    p1y = re.findall(coordSearch, waypoint1)[1]
    p1z = re.findall(coordSearch, waypoint1)[2]

    p2x = re.findall(coordSearch, waypoint2)[0]
    p2y = re.findall(coordSearch, waypoint2)[1]
    p2z = re.findall(coordSearch, waypoint2)[2]
    
    q1x = re.findall(coordSearch, obstacle)[0]
    q1y = re.findall(coordSearch, obstacle)[1]
    q1z = re.findall(coordSearch, obstacle)[2]
    
    q2x = re.findall(coordSearch, obstacle)[3]
    q2y = re.findall(coordSearch, obstacle)[4]
    q2z = re.findall(coordSearch, obstacle)[5]

    return(((((p1x - p2x)*(q1y - q2y) - (p1y - p2y)*(q1x - q2x))*(p1z - q1z) - ((p1x - p2x)*(q1z - q2z) - (p1z - p2z)*(q1x - q2x))*(p1y - q1y) + ((p1y - p2y)*(q1z - q2z) - (p1z - p2z)*(q1y - q2y))*(p1x - q1x))^2)^(1/2)/(((p1x - p2x)*(q1y - q2y) - (p1y - p2y)*(q1x - q2x))^2 + ((p1x - p2x)*(q1z - q2z) - (p1z - p2z)*(q1x - q2x))^2 + ((p1y - p2y)*(q1z - q2z) - (p1z - p2z)*(q1y - q2y))^2)^(1/2))

    def distLineVerticalLine(obstacleX, obstacleY, waypoint1, waypoint2):
        p1x = re.findall(coordSearch, waypoint1)[0]
        p1y = re.findall(coordSearch, waypoint1)[1]
        p1z = re.findall(coordSearch, waypoint1)[2]
        p2x = re.findall(coordSearch, waypoint2)[0]
        p2y = re.findall(coordSearch, waypoint2)[1]
        p2z = re.findall(coordSearch, waypoint2)[2]

        q1x = obstacleX
        q2x = obstacleY

        return((((p1x - p2x)*(p1y - q1y) - (p1y - p2y)*(p1x - q1x))^2)^(1/2)/((p1x - p2x)^2 + (p1y - p2y)^2)^(1/2))

#Check to see if any smooth path waypoint is in an obstacle
for waypoint in smoothPathFile:
    for obstacle in flightInformationFile:
        if re.findall(obstacle, tagSearch)[0] == 'static':
            distance = sqrt((re.findall(coordSearch, waypoint)[0] - re.findall(coordSearch, obstacle)[0])**2 + (re.findall(coordSearch, waypoint)[1] - re.findall(coordSearch, obstacle)[1])**2)
            if distance < re.findall(coordsearch, obstacle)[4] and re.findall(coordsearch, waypoint)[3] < re.findall(coordsearch, obstacle)[3]:
                collisions[obstacle] = distance
        if re.findall(tagSearch, obstacle)[0] == 'dynamic':
            if distPointLine(obstacle, waypoint) < re.findall(coordSearch, obstacle)[6] and sqrt((re.findall(coordSearch, waypoint)[0] - (re.findall(coordSearch, obstacle)[0] + re.findall(coordSearch, obstacle)[3])/2)**2 + (re.findall(coordSearch, waypoint)[1] - (re.findall(coordSearch, obstacle)[1] + re.findall(coordSearch, obstacle)[4])/2)**2 + (re.findall(coordSearch, waypoint)[2] - (re.findall(coordSearch, obstacle)[2] + re.findall(coordSearch, obstacle)[5])/2)**2) < sqrt((re.findall(coordSearch, obstacle)[6])**2 + (sqrt((re.findall(coordSearch, obstacle)[0] - re.findall(coordSearch, obstacle)[3])**2 + (re.findall(coordSearch, obstacle)[1] - re.findall(coordSearch, obstacle)[4])**2 + (re.findall(coordSearch, obstacle)[2] - re.findall(coordSearch, obstacle)[5])**2)/2)**2): 
                collisions[obstacle] = distPointLine(obstacle, waypoint)

#Check to see if the line connecting smooth path waypoints is too close to obstacle
for n in range(len(waypointList) - 1):
    for obstacle in obstaclesFile:
        if re.findall(obstacle, tagSearch)[0] == 'static':
            if distLineVerticalLine(re.findall(coordSearch, obstacle)[0], re.findall(coordSearch, obstacle)[1], waypointList[n], waypointList[n + 1]) < re.findall(coordSearch, obstacle)[4]:
                collisions.append(obstacle)
        if re.findall(tagSearch, obstacle)[0] == 'dynamic':
            if distLineLine(obstacle, waypointList[n], waypointList[n+1]) < re.findall(coordSearch, obstacle)[6]:               #Find a way to reference waypoint + 1
                collisions[obstacle] = distLineLine(obstacle, waypointList[n], waypointList[n+1])

if len(collisions) == 0:
    newFlightInformationFile.write('We\'re A okay, boss')

elif len(collisions) > 0:
    for obstacle in collisions:
        if obstacle == static:
            newFlightInformationFile.write("static " + re.findall(coordSearch, obstacle)[0] + " " + re.findall(coordSearch, obstacle)[1] + " " + re.findall(coordSearch, obstacle)[2] + " " + re.findall(coordSearch, obstacle)[3])
        if obstacle == dynamic:
            newFlightInformationFile.write("dynamic " + re.findall(coordSearch, obstacle)[0] + " " + re.findall(coordSearch, obstacle)[1] + " " + re.findall(coordSearch, obstacle)[2] + " " + re.findall(coordSearch, obstacle)[3])


