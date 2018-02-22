import re

def closestPoint(gl, st, ob):
    lin = [gl[0]-st[0],gl[1]-st[1],gl[2]-st[2]]
    length = ((lin[0])**2+(lin[1])**2+(lin[2])**2)**.5
    ln = [lin[0]/length,lin[1]/length,lin[2]/length]
    t = (((ob[0]-st[0])*ln[0])+((ob[1]-st[1])*ln[1])+(ln[2]*(ob[2]-st[2])))/(ln[0]**2+ln[1]**2+ln[2]**2)
    if (t < 0):
        t = 0
    elif(t > length):
        t = length;
    cp = [st[0]+ln[0]*t,st[1]+ln[1]*t,st[2]+ln[2]*t]
    return cp

def distPointLine(wp2, wp1, point):
    cp = closestPoint(gl, st, ob)
    d = ((ob[0]-cp[0])**2+(ob[1]-cp[1])**2+(ob[2]-cp[2])**2)**.5
    return d

def dist_static(wp1,wp2,ob):
    cp = closestPoint(wp1, wp2, ob)
    if(cp[2] > ob[2]):
        return ((ob[0]-cp[0])**2+(ob[1]-cp[1])**2+(ob[2]-cp[2])**2)**.5
    else:
        return distLineLine(ob,[ob[0],ob[1],0], wp1, wp2,ob[4])
        

def distLineLine(ob1, ob2, wp1, wp2,radius):
    

    while(sqrt((ob2[0]-ob1[0])^2+(ob2[1]-ob1[1])^2+(ob2[2]-ob1[2])^2) > radius/1.5):
        
        ob15 = [ob1[0]+ob2[0]/2,ob1[1]+ob2[1]/2,ob1[2]+ob2[2]/2]
        d1 = distPointLine(wp1,wp2,ob1)
        d2 = distPointLine(wp1,wp2,ob15)
        d3 = distPointLine(wp1,wp2,ob2)

        if (d2 < d3):
            ob2 = ob15
        else:
            ob1 = ob15

    finalDist1 = distPointLine(wp1,wp2,ob1)
    finalDist2 = distPointLine(wp1,wp2,ob2)
    if (finalDist2 < finalDist):
        return finalDist2
    else:
         return finalDist1


# return is_bad,expaned Static, expanded Dynamic
def Check(static_obs,dynamic_obs,vehicle_wps):

    static_collisions = []
    dynamic_collisions = []
    waypointList = vehicle_wps
    addition = 3

    for k in range(len(vehicle_wps)-1):
        for obstacle in static_obs:

            if (dist_static(vehicle_wps[k],vehicle_wps[k+1],obstacle) < 0):
                static_collisions.append(True)
            else:
                static_collisions.append(False)


    for k in range(vehicle_wps-1):
        for obstacle in dynamic_obs:

            # if dist between path and dynamic line
            if (distLineLine(obstacle, [obstacle[3],obstacle[4],obstacle[5]], vehicle_wps[k], vehicle_wpsk[k+1]) < obstacle[6]):
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
            final_dynamic_obs.append([dynamic_obs[k][0],dynamic_obs[k][1],dynamic_obs[k][2],dynamic_obs[k][3],dynamic_obs[k][4],dynamic_obs[k][5],dynamic_obs[k][6]+addition])
            is_bad = True  
        else:
            final_dynamic_obs.append(dynamic_obs[k])
    


        return is_bad, final_static_obs, final_dynmic_obs


st1 = [0,0,50,10]
st2 = [-10,30,50,8]
st3 = [20,-30,50,5]
statics = [st1,st2,st3]

dy1 = [-80,10,50,-80,-10,50,10]
dy2 = [-60,10,50,-60,-10,50,10]
dy3 = [-40,10,50,-40,-10,50,10]
dynamics = [dy1,dy2,dy3]

vwps = [[-150,0,50],[150,0,50]]

chk = Check(statics,dynamics,vwps)
print chk