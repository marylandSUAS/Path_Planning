import re

smoothPathFile = open('smooth_path.txt', 'r')
rawPathFile = open('raw_path.txt', 'r')
newFlightInformationFile = open('flight_information_new.txt', 'w')
flightInformationFile = open('flight_information.txt', 'r')

collisions = []

coordSearch = re.compile('\w\b\.\w*')
tagSearch = re.compile('^[a-z]*')

#Check to see if any smooth path waypoint is in an obstacle
for waypoint in smoothPathFile:
    for obstacle in flightInformationFile:
        if re.finall(obstacle, tagSearch)[0] == 'static':
            if sqrt((re.findall(waypoint, coordsearch)[0] - re.finall(coordsearch, obstacle)[0])**2 + (re.findall(coordsearch, waypoint)[1] - re.finall(coordsearch, obstacle)[1])**2) < re.findall(coordsearch, obstacle)[4] and re.findall(coordsearch, waypoint)[3] < re.findall(coordsearch, obstacle)[3]:
                collisions.append(obstacle)
        if re.findall(tagSearch, obstacle)[0] == 'dynamic':
            if 'distance from line connecting the two waypoins' < re.findall(coordSearch, obstacle)[7]:
                collisions.append(obstacle)

#Check to see if the line connecting smooth path waypoints is too close to obstacle
for waypoint in smoothPathFile:
    for obstacle in obstaclesFile:
        if re.finall(obstacle, tagSearch)[0] == 'static':
            if '''distance from line connecting waypoint and waypoint +1 and vertical
            line at (obstacle.x, obstacle.y)''' < re.findall(coordSearch, obstacle)[4]:
                collisions.append(obstacle)
        if re.findall(tagSearch, obstacle)[0] == 'dynamic':
            if '''distance from line connecting waypoint and waypoint +1 and line
            connecting the two obstacle waypoints''' < re.findall(coordSearch, obstacle)[7]:
                collisions.append(obstacle)

if len(collisions) == 0:
    newFlightInformationFile.write('We\'re A okay, boss')

elif len(collisions) > 0:
    for obstacle in collisions:
        if obstacle == static:
            newFlightInformationFile.write('Insert new obstacle data here')
        if obstacle == dynamic:
            newFlightInformationFile.write('Insert new obstacle data here')


