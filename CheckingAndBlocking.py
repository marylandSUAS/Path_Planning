#smoothPathFile = open('insert smooth path waypoint file name here', 'r')
#rawPathFile = open('insert raw path waypoint file name here', 'r')
#osbtaclesFile = open('insert obstacle date file name here'', 'r')
adjustmentsFile = open('adjustments.txt', 'w')

collisions = []

#Check to see if any smooth path waypoint is in an obstacle
for waypoint in smoothPathFile:
    for obstacle in obstaclesFile:
        if obstacle == static:
            if abs(waypoint.x - obstacle.x) < obstacle.radius:
                collisions.append(obstacle)
            if abs(waypoint.y - obstacle.y) < obstacle.radius:
                collisions.append(obstacle)
        if obstacle == dynamic:
            if 'distance from line connecting the two waypoins' < obstacle.radius:
                collisions.append(obstacle)

#Check to see if the line connecting smooth path waypoints is too close to obstacle
for waypoint in smoothPathFile:
    for obstacle in obstaclesFile:
        if obstacle == static:
            if '''distance from line connecting waypoint and waypoint +1 and vertical
            line at (obstacle.x, obstacle.y)''' < obstacle.radius:
                collisions.append(obstacle)
        if obstacle == dynamic:
            if '''distance from line connecting waypoint and waypoint +1 and line
            connecting the two obstacle waypoints''' < obstacle.radius:
                collisions.append(obstacle)

if len(collisions) == 0:
    adjustmentsFile.write('We\'re A okay, boss')

else if len(collisions) > 0:
    for obstacle in collisions:
        if obstacle == static:
            adjustments.write('Insert new obstacle data here')                      #Possibly add an extra method to 'obstacle' class that returns its data as a tuple
        if obstacle == dynamic:
            adjustments.write('Insert new obstacle data here')


