import re
import time
from math import pi,sin,cos,atan,fabs,atan2,asin,acos

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

def distPointLine(wp1, wp2, ob):
    cp = closestPoint(wp1, wp2, ob)
    d = ((ob[0]-cp[0])**2+(ob[1]-cp[1])**2+(ob[2]-cp[2])**2)**.5
    return d

def dist_static(wp1,wp2,ob):
    cp = closestPoint(wp1, wp2, ob)
    dist2D = ((cp[0]-ob[0])**2+(cp[1]-ob[1])**2)**.5    

    if(dist2D > ob[3]):
        return ob[3]+5
        
    xdist = ((ob[3])**2-(dist2D)**2)**.5
    phi = atan2(wp2[2]-wp1[2],((wp2[1]-wp1[1])**2+(wp2[0]-wp1[0])**2)**.5)
    z1 = cp[2]+xdist*sin(phi)
    z2 = cp[2]-xdist*sin(phi)

    if(z1 > ob[2] and z2 > ob[2]):
        return ob[3]+5
    else:
        return dist2D
        

def distLineLine(ob1, ob2, wp1, wp2,radius):
    

    while(sqrt((ob2[0]-ob1[0])**2+(ob2[1]-ob1[1])**2+(ob2[2]-ob1[2])**2) > radius/1.5):
        
        ob15 = [(ob1[0]+ob2[0])/2,(ob1[1]+ob2[1])/2,(ob1[2]+ob2[2])/2]
        d1 = distPointLine(wp1,wp2,ob1)
        d2 = distPointLine(wp1,wp2,ob15)
        d3 = distPointLine(wp1,wp2,ob2)

        if (d2 < d3):
            ob2 = ob15
        else:
            ob1 = ob15

    finalDist1 = distPointLine(wp1,wp2,ob1)
    finalDist2 = distPointLine(wp1,wp2,ob2)
    if (finalDist2 < finalDist1):
        return finalDist2
    else:
         return finalDist1


def genPath(vehicle_wps,thetaOG):

    if(thetaOG == None):
        theta = atan2(vehicle_wps[1][1]-vehicle_wps[0][1],vehicle_wps[1][0]-vehicle_wps[0][0])
        print 'new theta'
    else:
        theta = thetaOG
        print 'OG'

    wpto = 1
    stepsize = 3.0
    maxtheta = asin(stepsize/30)

    loc = vehicle_wps[0]
    # theta = thetaOG
    path = [loc]
    while(wpto < len(vehicle_wps)):
        dist = ((loc[0]-vehicle_wps[wpto][0])**2+(loc[1]-vehicle_wps[wpto][1])**2)**.5
        linDist = dist
        heightDif = vehicle_wps[wpto][2]-loc[2]
        counter = 0
        while(dist > stepsize):
            dtheta = atan2(vehicle_wps[wpto][1]-loc[1],vehicle_wps[wpto][0]-loc[0])
            print dtheta,' ',theta
            diftheta = dtheta-theta
            
            if (fabs(diftheta) > maxtheta):
                theta = theta+maxtheta*diftheta/fabs(diftheta)
            else:
                theta = theta+diftheta

            step = [stepsize*cos(theta),stepsize*sin(theta)]


            loc = [loc[0]+step[0],loc[1]+step[1],vehicle_wps[wpto][2]+heightDif*(1-(dist/linDist))]
            path.append(loc)

            dist = ((loc[0]-vehicle_wps[wpto][0])**2+(loc[1]-vehicle_wps[wpto][1])**2)**.5

            counter = counter+1
            if (counter > 150):
                print 'failed'
                return


        wpto = wpto+1
    return path


# return is_bad,expaned Static, expanded Dynamic
def Check(static_obs,dynamic_obs,vehicle_wps,direc):

    static_collisions = []
    dynamic_collisions = []
    addition = 3

    if(len(vehicle_wps) < 2):
        return False,static_obs,dynamic_obs

    path = genPath(vehicle_wps,direc)


    dynamic_collisions = []
    for obstacle in dynamic_obs:
        temp = False
        for point in path:
            if (((obstacle[0]-point[0])**2+(obstacle[1]-point[1])**2+(obstacle[2]-point[2])**2)**.5 < obstacle[3]):
                temp = True

        dynamic_collisions.append(temp)


    static_collisions = []
    for obstacle in static_obs:
        temp = False
        for point in path:
            if (((obstacle[0]-point[0])**2+(obstacle[1]-point[1])**2)**.5 < obstacle[3] and point[2] < obstacle[2]):
                temp = True

        static_collisions.append(temp)
     

    
    # for obstacle in static_obs:
    #     for k in range(len(vehicle_wps)-1):
    #         temp = False

    #         tempdist = dist_static(vehicle_wps[k],vehicle_wps[k+1],obstacle)
    #         # print 'dist = ',tempdist
    #         # print obstacle[3]
    #         if (tempdist < obstacle[3]):
    #             temp = True

    #     if(temp):
    #         static_collisions.append(True)
    #         # print 'static collision'
    #     else:
    #         static_collisions.append(False)
    #         # print 'no static collision'


    # for obstacle in dynamic_obs:
    #     for k in range(len(vehicle_wps)-1):

    #         temp = False


    #         # if dist between path and dynamic line
    #         tempdist = distLineLine(obstacle, [obstacle[3],obstacle[4],obstacle[5]], vehicle_wps[k], vehicle_wps[k+1],obstacle[6])
    #         # print 'tempdist = ',tempdist
    #         if (tempdist < obstacle[6]):
    #             temp = True

    #     if(temp):
    #         # print 'dynamic collision'
    #         dynamic_collisions.append(True)
    #     else:
    #         # print 'no dynamic collision'
    #         dynamic_collisions.append(False)


    print 'static collisions', static_collisions
    print 'dynamic_collisions', dynamic_collisions

    is_bad = False
    final_static_obs = []
    for k in range(len(static_collisions)):
        if (static_collisions[k]):
            final_static_obs.append([static_obs[k][0],static_obs[k][1],static_obs[k][2],static_obs[k][3]+addition])
            is_bad = True  

        else:
            final_static_obs.append(static_obs[k])


    final_dynamic_obs = []
    for k in range(len(dynamic_collisions)):
        if (dynamic_collisions[k]):
            final_dynamic_obs.append([dynamic_obs[k][0],dynamic_obs[k][1],dynamic_obs[k][2],dynamic_obs[k][3],dynamic_obs[k][4],dynamic_obs[k][5],dynamic_obs[k][6]+addition])
            is_bad = True  
        else:
            final_dynamic_obs.append(dynamic_obs[k])
    
    return is_bad, final_static_obs, final_dynamic_obs


# st1 = [0,1,55,10]
# st2 = [-10,30,50,8]
# st3 = [20,-30,50,5]
# statics = [st1,st2,st3]

# dy1 = [-80,10,50,-80,-10,50,10]
# dy2 = [-60,10,50,-60,-10,50,10]
# dy3 = [-40,10,50,-40,-10,50,10]
# dynamics = [dy1,dy2,dy3]
# # dynamics = []


# wps = [[-150,0,50],[0,100,50],[150,0,50]]
# startTime = time.time()
# # path = genPath(wps,-pi*.25)



# # BFile = open('Output_Path_gen.txt',"w")
        
# # for point in path:
# #     BFile.write(str(point))
# #     BFile.write('\n')    
                
# # BFile.close()

# is_bad, final_static_obs, final_dynamic_obs = Check(statics,dynamics,wps,None)
# print 'time taken: ', time.time()-startTime
# print is_bad
# print final_static_obs
# print final_dynamic_obs