import re

# def getCoords(inputLine):
    # return([float(n) for n in re.findall(re.compile('\w*\.\w*'), inputLine)])

def distPointLine(point, wp1, wp2):
    px = point[0]
    py = point[1]
    pz = point[2]
    
    q1x = wp1[0]
    q1y = wp1[1]
    q1z = wp1[2]
    
    q2x = wp2[3]
    q2y = wp2[4]
    q2z = wp2[5]
    
    return(
        (((px-q1x)*(q1y-q2y) - (py-q1y)*(q1x-q2x))**2 + \
        ((px-q1x)*(q1z-q2z) - (pz-q1z)*(q1x-q2x))**2 + \
        ((py-q1y)*(q1z-q2z) - (pz-q1z)*(q1y-q2y))**2)**(1/2) / \
        ((q1x-q2x)**2 + (q1y-q2y)**2 + (q1z-q2z)**2)**(1/2))


def distLineLine(obstacle1, obstacle2, waypoint1, waypoint2):
    p1x = waypoint1[0] 
    p1y = waypoint1[1] 
    p1z = waypoint1[2]

    p2x = waypoint2[0]
    p2y = waypoint2[1] 
    p2z = waypoint2[2]
    
    q1x = obstacle1[0] 
    q1y = obstacle1[1]
    q1z = obstacle1[2] 
    
    q2x = obstacle2[1] 
    q2y = obstacle2[1] 
    q2z = obstacle2[2] 

    return(
        ((((p1x-p2x)*(q1y-q2y) - (p1y-p2y)*(q1x-q2x))*(p1z-q1z) - \
        ((p1x-p2x)*(q1z-q2z) - (p1z-p2z)*(q1x-q2x))*(p1y-q1y) + \
        ((p1y-p2y)*(q1z-q2z) - (p1z-p2z)*(q1y-q2y))*(p1x-q1x))**2)**(1/2) / \
        (((p1x-p2x)*(q1y-q2y) - (p1y-p2y)*(q1x-q2x))**2 + \
        ((p1x-p2x)*(q1z-q2z) - (p1z-p2z)*(q1x-q2x))**2 + \
        ((p1y-p2y)*(q1z-q2z) - (p1z-p2z)*(q1y-q2y))**2)**(1/2))


def distLineVerticalLine(obXY, waypoint1, waypoint2):
    p1x = waypoint1[0]
    p1y = waypoint1[1]
    p1z = waypoint1[2]

    p2x = waypoint2[0]
    p2y = waypoint2[1]
    p2z = waypoint2[2]

    q1x = obXY[0]
    q1y = obXY[1]

    return(
        (((p1x-p2x)*(p1y-q1y) - (p1y-p2y)*(p1x-q1x))**2)**(1/2) / \
        ((p1x-p2x)**2 + (p1y-p2y)**2)**(1/2)) 


# return is_bad,expaned Static, expanded Dynamic
def Check(static_obs,dynamic_obs,vehicle_wps):

    static_collisions = []
    dynamic_collisions = []
    waypointList = vehicle_wps
    addition = 3

    for k in range(vehicle_wps-1):
        for obstacle in static_obs:
            collisions = False

            # if dist between line and static
            if (distPointLine(obstacle, vehicle_wps[k], vehicle_wpsk[k+1]) < obstacle[2]):
                collisions = True
            # if dist between line and static
            if (distLineLine(obstacle, [obstacle[0],obstacle[1],0], vehicle_wps[k], vehicle_wpsk[k+1]) < obstacle[2]):
                collisions = True

            if collisions:
                static_collisions.append(True)
            else:
                static_collisions.append(False)


    for k in range(vehicle_wps-1):
        for obstacle in dynamic_obs:
            collisions = False

            # if dist between path and dynamic points
            if (distPointLine([obstacle[0],obstacle[1],obstacle[2],obstacle[6]], vehicle_wps[k], vehicle_wpsk[k+1]) < obstacle[6]):
                collisions = True
            if (distPointLine([obstacle[3],obstacle[4],obstacle[5],obstacle[6]], vehicle_wps[k], vehicle_wpsk[k+1]) < obstacle[6]):
                collisions = True 
            # if dist between path and dynamic line
            if (distLineLine(obstacle, [obstacle[3],obstacle[4],obstacle[5]], vehicle_wps[k], vehicle_wpsk[k+1]) < obstacle[6]):
                collisions = True            

            if collisions:
                static_collisions.append(True)
            else:
                static_collisions.append(False)


    is_bad = False
    final_static_obs = []
    for k in range(static_collisions):
        if (static_collisions[k]):
            final_static_obs.append([static_obs[k][0],static_obs[k][1],static_obs[k][2],static_obs[k][3]+addition])
            is_bad = True  
        else:
            final_static_obs.append(static_obs[k])


    final_dynamic_obs = []
    for k in range(dynamic_collisions):
        if (dynamic_collisions[k]):
            final_dynamic_obs.append([static_obs[k][0],static_obs[k][1],static_obs[k][2],static_obs[k][3]+addition])
            is_bad = True  
        else:
            final_dynamic_obs.append(dynamic_obs[k])
    


        return is_bad, final_static_obs, final_dynmic_obs