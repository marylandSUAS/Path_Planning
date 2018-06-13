
import sys
import time
from pymavlink import mavutil


def mavlink_latlon(degrees):
    """Converts a MAVLink packet lat/lon degree format to decimal degrees."""
    return float(degrees) / 1e7


def mavlink_alt(dist):
    """Converts a MAVLink packet millimeter format to decimal feet."""
    return dist * 0.00328084


def mavlink_heading(heading):
    """Converts a MAVLink packet heading format to decimal degrees."""
    return heading / 100.0


def proxy_mavlink(device):
    
    mav = mavutil.mavlink_connection(device, autoreconnect=True)

    while True:
        msg = mav.recv_match(type='GLOBAL_POSITION_INT',blocking=True,timeout=10.0)

        if msg is None:
            print 'Did not receive MAVLink packet for over 10 seconds.'
        else:

        telemetry = [mavlink_latlon(msg.lat), mavlink_latlon(msg.lon), mavlink_alt(msg.alt),mavlink_heading(msg.hdg)]

        with open('../data/currentLoc.txt',"w") as staticObjFile:
            staticObjFile.write(str(telemetry[0]))
            staticObjFile.write(str(' '))
            staticObjFile.write(str(telemetry[1]))
            staticObjFile.write(str(' '))
            staticObjFile.write(str(telemetry[2]))
            staticObjFile.write(str(' '))
            staticObjFile.write(str(telemetry[3]))