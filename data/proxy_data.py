# Module to receive MAVLink packets and forward telemetry via interoperability.
# Packet details at http://mavlink.org/messages/common#GLOBAL_POSITION_INT.

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


def proxy_mavlink(device,):
    """Receives packets over the device and forwards telemetry via the client.

    Args:
        device: A pymavlink device name to forward.
        client: Interop Client with which to send telemetry packets.
    """
    # Create the MAVLink connection.
    mav = mavutil.mavlink_connection(device, autoreconnect=True)


    while True:
        # Get packet.
        msg = mav.recv_match(type='GLOBAL_POSITION_INT',
                             blocking=True,
                             timeout=10.0)
        if msg is None:
            logger.critical(
                'Did not receive MAVLink packet for over 10 seconds.')
            sys.exit(-1)
        # Convert to telemetry.
            telemTEMP = [mavlink_latlon(msg.lat), mavlink_latlon(msg.lon), mavlink_alt(msg.alt),mavlink_heading(msg.hdg)]
            print(telemTEMP)
            with open('../../Gui/currentLoc.txt',"w") as staticObjFile:
                staticObjFile.write(str(telemTEMP[0]))
                staticObjFile.write(str(' '))
                staticObjFile.write(str(telemTEMP[1]))
                staticObjFile.write(str(' '))
                staticObjFile.write(str(telemTEMP[2]))
                staticObjFile.write(str(' '))
                staticObjFile.write(str(telemTEMP[3]))






proxy_mavlink('127.0.0.1:14550')