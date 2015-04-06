""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation
modified by Embedded Artists 2014

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""

import socket
import serial
import OSC
import time, threading
import EANet
import EA3D
# init the camera
from EACamera import EACamera
from EAVideo import EAVideo
from EA3D import EA3D

camera = EACamera()
camera.setAlpha(64)
camera.setFrame(100,100,640,480)

video = EAVideo()

# setting up the 3d graphics
graphics = EA3D()

### Arduino
UART = serial.Serial("/dev/ttyAMA0", baudrate=9600)

# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
# ip address of the raspi, localhost wouldn't work, because, well, its local
receive_address = EANet.get_interface_ip("eth0:1"), 9000
print "OSC going to listen on %s" % receive_address[0]

# OSC Server. there are three different types of server. 
s = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking



# define a message-handler function for the server to call.
def arduino_handler(addr, tags,stuff,source):
	global UART
    	#print "data %s" % stuff
        #UART.write(stuff)
        #UART.write("\n")
	#if len(stuff) == 1:
        UART.write(stuff[0]);
        UART.write("\n")
        #if len(stuff) == 2:
	#        UART.write(stuff[0]);
	#	UART.write(str(stuff[1]));
		
def printing_handler(addr, tags, stuff, source):
    print "---"
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff

# define a message-handler function for the server to call.
	

    
# this registers a 'default' handler (for unmatched messages), 
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()

s.addMsgHandler("/arduino", arduino_handler) # adding our function
s.addMsgHandler("/print", printing_handler) # adding our function

s.addMsgHandler("/3d", graphics.oscHandler) # adding our function

s.addMsgHandler("/camera", camera.oscHandler) # adding our function

s.addMsgHandler("/video", video.oscHandler) # adding our function

# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr


# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
# create server thread
st = threading.Thread( target = s.serve_forever )
st.start()

try :
    while graphics.DISPLAY.loop_running():
	graphics.DISPLAY.clear()
	i = 1
	if (graphics.scene < 2): # scene 2 implicit empty 
  		for o in graphics.objects[graphics.scene]:	
			o.draw()
	  		o.rotateIncX((graphics.rotationX+i)*0.01)
			o.rotateIncY((graphics.rotationY+i)*0.12)
			o.rotateIncZ((graphics.rotationZ-i)*0.02)
			o.position(graphics.xloc, graphics.yloc, 15.0)
			i = i + 1
	elif (graphics.scene == 3):
		graphics.mysphere.draw()
		
	time.sleep(0.01)	
except KeyboardInterrupt :
    camera.close()
    video.close()
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    UART.close()
    print "Done"
