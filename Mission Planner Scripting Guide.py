import sys
import math
from math import pi,sin,cos,atan,atan2
import clr
import System
from System import Byte


clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") #includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink


#SPEAKING
#need to enable this
MissionPlanner.MainV2.speechEnable = True
#call this with the string you want it to say
MissionPlanner.MainV2.speechEngine.SpeakAsync(string)


#WAYPOINT OBJECTS
Locationwp().Set(latitude,longitude,altitude, 16)

'''
Waypoint type IDs
16 Waypoint
21 land
82 Spline Waypoint
18 Loiter Turns
19 Loiter Turns
17 Loiter Unlim
20 Return to Launch
22 takeoff
93 delay
the rest can be found through the following line but change TAKEOFF to the type of waypoint as found in mission planner
'''
int(MAVLink.MAV_CMD.TAKEOFF)

'''
Each waypoint has an id,parameters 1-4,lat,lng, and alt
the use if each of these value can be found under the tabs in the mission creation
these can be changed through the following lines
https://github.com/ArduPilot/MissionPlanner/blob/master/ExtLibs/Utilities/locationwp.cs
'''
WP = Locationwp()
Locationwp.id.SetValue(WP, input value)
Locationwp.p1.SetValue(WP, input value)
Locationwp.p2.SetValue(WP, input value)
Locationwp.p3.SetValue(WP, input value)
Locationwp.p4.SetValue(WP, input value)
Locationwp.lat.SetValue(WP, input value)
Locationwp.lng.SetValue(WP, input value)
Locationwp.alt.SetValue(WP, input value)
#can call any other these values through WpName.value
#example WP.alt to get altitude


#example how to set a takeoff point
#to = Locationwp()
#Locationwp.id.SetValue(to, int(MAVLink.MAV_CMD.TAKEOFF))
#Locationwp.p1.SetValue(to, 15)
#Locationwp.alt.SetValue(to, 40)

#example setting a do set servo command
#dropWP = Locationwp()
#Locationwp.id.SetValue(dropWP, 183)
#Locationwp.p1.SetValue(dropWP, 13)
#Locationwp.p2.SetValue(dropWP, 1900)


#setting waypoints
MAV.setWPTotal(number)	
#sets the max number of wps that are going to be uploaded before reset

MAV.setWP(WPObject,WPnumber,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
#to set a waypoint, upload a WP object and the desired WP number in order

MAV.setWPCurrent(1)
#sets the wp number that it is currently going towards

#In order to set a set of waypoints you have to set a new home location, WPTotal, and reset current WP to 1
#Uploading waypoint number 0 is setting home
#if you upload waypoints without uploading a new home and wpTotal they will not upload
#they also absolutely have to be uploaded in WP order
#if it finishes the waypoints or it is trying to go to a waypoint that doesnt exist it will switch modes to RTL

#example to upload a new set of waypoints
MAV.setWPTotal(number)	
MAV.setWP(HomeWp,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
MAV.setWPCurrent(1)
MAV.setWP(NextWp,1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)


#Script Commands
Script.Sleep(miliseconds)
#delay in miliseconds

Script.GetParam(ParamName)
#find the value of the parameter as defined in the Mission Planner param tree

Script.ChangeParam(ParamName,Value)
#Changes Params

Script.getParamList(ParamName,Value)
#Changes Params

Script.ChangeMode("Mode")
#Changes mode the vechile is in givin a string of the mode
#"Manual", "Auto", "Guided", "Loiter"

Script.WaitFor("string",timeout)
Script.WaitFor('Message String',30000)
#not sure how to use this.  Look into the script examples

Script.SendRC(channel,PWM,sendnow)
#sets a servo with channel(int), PWM(int), sendnow(bool)


#MAV commands
MAV.setParam(ParamName,Value)
#same as changeparam

MAV.GetParam(name)
MAV.GetParam(index)
#same as get param

MAV.Stopall(bool)
#stops all processes

MAV.setWPACK()
#acknologes waypoints.  Not sure what this does really

MAV.setWPCurrent(int)

MAV.doAction(object,actionid)
#http://ardupilot.org/dev/docs/plane-commands-in-guided-mode.html

MAV.doARM(bool)
#arms/disarms vechicle

MAV.doCommand(int(MAVLink.MAV_CMD.WaypointType),p1,p2,p3,p4,lat,lng,alt)
#does mav waypoints

MAV.getWPCount()
#returns number of waypoints

MAV.getWP(WpNumber)
#returns the Waypoint object of that waypoint number

MAV.setWP(WPObject,WPnumber,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)

MAV.setWPTotal(number)

MAV.setGuidedModeWP(LocationWpObject)
#changes mode to guided mode and will travel to this location if flying already

MAV.setMode("Mode")
#changes more to string of mode
#"Manual", "Auto", "Guided", "Loiter"

MAV.setDigicamControl(bool)


#Current State
#allows you to get the current state of almost thing on the vehicle
#call through cs.
#find the full list of possible thing to call here	
https://github.com/ArduPilot/MissionPlanner/blob/master/CurrentState.cs
#some usefull ones here
cs.lat
cs.lng
cs.alt
cs.nav_bearing
cs.nav_roll
cs.nav_pitch
cs.wpno #current waypoint number
cs.satcount
cs.gpshdop
cs.mode
cs.wp_dist
cs.DistToHome
cs.timeInAir
cs.distTraveled
cs.climbrate
cs.landed
cs.connected
cs.messages
cs.messages.Clear



#example simple mission
home = Locationwp().Set(-34.9805,117.8518,0, 16)
to = Locationwp()
Locationwp.id.SetValue(to, 22)
Locationwp.p1.SetValue(to, 15)
Locationwp.alt.SetValue(to, 50)
wp1 = Locationwp().Set(-35,117.8,50, 16)
wp2 = Locationwp().Set(-35,117.89,50, 16)
wp3 = Locationwp().Set(-35,117.85,20, 16)

MAV.setWPTotal(5)
MAV.setWP(home,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
MAV.setWP(to,1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
MAV.setWP(wp1,2,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
MAV.setWP(wp2,3,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
MAV.setWP(wp3,4,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
MAV.setWPACK();