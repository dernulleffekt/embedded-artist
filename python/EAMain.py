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
import pi3d
import EANet

# init the camera
from EACamera import EACamera
camera = EACamera()
camera.setAlpha(64)
camera.setFrame(100,100,640,480)

# setup 3d
DISPLAY = pi3d.Display.create(frames_per_second = 25,background = (0.0, 0.0, 0.0, 1.))
mylight = pi3d.Light(lightpos=(-2.0, -1.0, 10.0), lightcol=(1.0, 1.0, 0.8), lightamb=(0.25, 0.2, 0.3))

shader = pi3d.Shader("uv_light")
#sprite = pi3d.ImageSprite("camera.PNG", shader, w=10.0, h=10.0) # path relative to program dir
#sprite = pi3d.Cuboid(3.,3.,3.) # Sphere("earth", 0.0, 0.0, -10.0, 3.0, 24)
#mysphere = pi3d.Sphere(radius=1, sides=24, slices=24, name="sphere",
#        x=-4, y=2, z=10)
#mysphere = pi3d.Model(file_string='../../pi3dDemos/models/cow2.obj', name='napf', x=0, y=-1, z=40,
objects = []
objects.append([])
objects.append([])
scene = 0
scale = 2.
mysphere = pi3d.Model(file_string='dorn.obj', name='napf', x=0, y=-1, z=-40,
                sx=2., sy=2., sz=2.)
mysphere.set_shader(shader)
objects[0].append(mysphere)
count = 15
for i in range(count):
	clony=mysphere.clone()
	clony.position(i,-1,-40)
	objects[0].append(clony)

miene  = pi3d.Model(file_string='guteMiene.obj', name='miene', x=0, y=-1, z=-40,
                sx=2., sy=2., sz=2.)
miene.set_shader(shader)
objects[1].append(miene)
for i in range(count):
	clony=miene.clone()
	clony.position(i,-1,-40)
	objects[1].append(clony)
#mysphere.reparentTo(anchor)
#clony.reparentTo(mysphere)

# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
# ip address of the raspi, localhost wouldn't work, because, well, its local
receive_address = EANet.get_interface_ip("eth0"), 9000
print "OSC going to listen on %s" % receive_address[0]
xloc = 1.0;
yloc = 1.0;
rotationX = 0.0
rotationY = 0.0
rotationZ = 0.0
vrcamxloc = 1.0
vrcamyloc = 1.0
# OSC Server. there are three different types of server. 
s = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking


# this registers a 'default' handler (for unmatched messages), 
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()

### Arduino
UART = serial.Serial("/dev/ttyAMA0", baudrate=9600)

# define a message-handler function for the server to call.
def arduino_handler(addr, tags,stuff,source):
	global UART
	print "so ein Arduino Kram, ne"
    	print "with addr : %s" % addr
    	print "typetags %s" % tags
    	print "data %s" % stuff
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
def posx_handler(addr, tags, stuff, source):
    global xloc
    xloc = float(stuff[0])
    for o in objects[0]:	
		o.position(xloc, yloc, 15.0)

    for o in objects[1]:	
		o.position(xloc, yloc, 15.0)

def posy_handler(addr, tags, stuff, source):
    global yloc
    yloc = float(stuff[0])	
    for o in objects[0]:	
		o.position(xloc, yloc, 15.0)
	
    for o in objects[1]:	
		o.position(xloc, yloc, 15.0)

def VrCamPosX_handler(addr, tags, stuff, source):
    global vrcamxloc
    vrcamxloc = float(stuff[0])
    from pi3d.Camera import Camera
    vrcamera = Camera.instance()
    if vrcamera:
    	vrcamera.position((vrcamxloc,vrcamyloc,1.0))

def VrCamPosY_handler(addr, tags, stuff, source):
    global vrcamyloc
    vrcamyloc = float(stuff[0])	
    from pi3d.Camera import Camera
    vrcamera = Camera.instance()
    if vrcamera:
    	vrcamera.position((vrcamxloc,vrcamyloc,1.0))
	
def rotationX_handler(addr, tags, stuff, source):
    global rotationX
    rotationX = float(stuff[0])	
    i = 1
    for o in objects[0]:	
	  	o.rotateIncX((rotationX*i)*0.001)
		i = i + 1
    i = 1
    for o in objects[1]:	
	  	o.rotateIncX((rotationX*i)*0.001)
		i = i + 1

def rotationY_handler(addr, tags, stuff, source):
    global rotationY
    rotationY = float(stuff[0])
    i = 1;	
    for o in objects[0]:	
	  	o.rotateIncY((rotationY*i)*0.0012)
		i = i + 1
    i = 1;	
    for o in objects[1]:	
	  	o.rotateIncY((rotationY*i)*0.0012)
		i = i + 1

def rotationZ_handler(addr, tags, stuff, source):
    global rotationZ
    rotationZ = float(stuff[0])	
    i = 1;	
    for o in objects[0]:	
		o.rotateIncZ((rotationZ*i)*0.00132)
		i = i + 1
    i = 1;	
    for o in objects[1]:	
		o.rotateIncZ((rotationZ*i)*0.00132)
		i = i + 1

def scale_handler(addr, tags, stuff, source):
    global scale
    scale = float(stuff[0])	
    for o in objects[0]:	
		o.scale(scale,scale,scale)
    for o in objects[1]:	
		o.scale(scale,scale,scale)


def scene_handler(addr, tags, stuff, source):
    global scene
    scene = int(stuff[0])	

def cameraAlpha_handler(addr, tags, stuff, source):
    global camera
    camera.setAlpha(int(stuff[0]))		
 
def cameraEffect_handler(addr, tags, stuff, source):
    global camera
    camera.setEffect(int(stuff[0]))		
 
def cameraSaturation_handler(addr, tags, stuff, source):
    global camera
    camera.setSaturation(int(stuff[0]))		
 
def cameraSharpness_handler(addr, tags, stuff, source):
    global camera
    camera.setSharpness(int(stuff[0]))		
 
def cameraShutter_handler(addr, tags, stuff, source):
    global camera
    camera.setShutterspeed(int(stuff[0]))		
 
def cameraX_handler(addr, tags, stuff, source):
    global camera
    camera.setX(int(stuff[0]))		

def cameraY_handler(addr, tags, stuff, source):
    global camera
    camera.setY(int(stuff[0]))		

def cameraWidth_handler(addr, tags, stuff, source):
    global camera
    camera.setWidth(int(stuff[0]))		

def cameraHeight_handler(addr, tags, stuff, source):
    global camera
    camera.setHeight(int(stuff[0]))		

def cameraFramerate_handler(addr, tags, stuff, source):
    global camera
    camera.setFramerate(int(stuff[0]))		

def cameraHFlip_handler(addr, tags, stuff, source):
    global camera
    camera.setHFlip(bool(stuff[0]))		
def cameraVFlip_handler(addr, tags, stuff, source):
    global camera
    camera.setVFlip(bool(stuff[0]))		
def cameraFullscreen_handler(addr, tags, stuff, source):
    global camera
    camera.setFullscreen(bool(stuff[0]))		

def cameraZoomX_handler(addr, tags, stuff, source):
    global camera
    camera.setZoomX(float(stuff[0]))		

def cameraZoomY_handler(addr, tags, stuff, source):
    global camera
    camera.setZoomY(float(stuff[0]))		

def cameraZoomWidth_handler(addr, tags, stuff, source):
    global camera
    camera.setZoomW(float(stuff[0]))		

def cameraZoomHeight_handler(addr, tags, stuff, source):
    global camera
    camera.setZoomH(float(stuff[0]))		

def cameraSwitch_handler(addr, tags, stuff, source):
    global camera
    if bool(stuff[0]):
	camera.start();
    else:
	camera.stop()

def videoPlay_handler(addr, tags, stuff, source):
    global camera
    camera.playVideo(stuff[0])		

def videoPause_handler(addr, tags, stuff, source):
    global camera
    camera.pauseVideo()		

def videoStop_handler(addr, tags, stuff, source):
    global camera
    camera.stopVideo()		

def videoFaster_handler(addr, tags, stuff, source):
    global camera
    camera.fasterVideo()		

def videoSlower_handler(addr, tags, stuff, source):
    global camera
    camera.slowerVideo()		

s.addMsgHandler("/arduino", arduino_handler) # adding our function
s.addMsgHandler("/print", printing_handler) # adding our function
s.addMsgHandler("/3d/posX", posx_handler) # adding our function
s.addMsgHandler("/3d/posY", posy_handler) # adding our function
s.addMsgHandler("/3d/camera/x", VrCamPosX_handler) # adding our function
s.addMsgHandler("/3d/camera/y", VrCamPosY_handler) # adding our function
s.addMsgHandler("/3d/scale", scale_handler) # adding our function
s.addMsgHandler("/3d/rotationX", rotationX_handler) # adding our function
s.addMsgHandler("/3d/rotationY", rotationY_handler) # adding our function
s.addMsgHandler("/3d/scene", scene_handler) # adding our function
s.addMsgHandler("/3d/rotationZ", rotationZ_handler) # adding our function
s.addMsgHandler("/camera/alpha", cameraAlpha_handler) # adding our function
s.addMsgHandler("/camera/effect", cameraEffect_handler) # adding our function
s.addMsgHandler("/camera/saturation", cameraSaturation_handler) # adding our function
s.addMsgHandler("/camera/sharpness", cameraSharpness_handler) # adding our function
s.addMsgHandler("/camera/shutter", cameraShutter_handler) # adding our function
s.addMsgHandler("/camera/framerate", cameraFramerate_handler) # adding our function
s.addMsgHandler("/camera/x", cameraX_handler) # adding our function
s.addMsgHandler("/camera/y", cameraY_handler) # adding our function
s.addMsgHandler("/camera/width", cameraWidth_handler) # adding our function
s.addMsgHandler("/camera/height", cameraHeight_handler) # adding our function
s.addMsgHandler("/camera/switch", cameraSwitch_handler) # adding our function

s.addMsgHandler("/camera/zoomX", cameraZoomX_handler) # adding our function
s.addMsgHandler("/camera/zoomY", cameraZoomY_handler) # adding our function
s.addMsgHandler("/camera/zoomW", cameraZoomWidth_handler) # adding our function
s.addMsgHandler("/camera/zoomH", cameraZoomHeight_handler) # adding our function

s.addMsgHandler("/camera/hflip", cameraHFlip_handler) # adding our function
s.addMsgHandler("/camera/vflip", cameraVFlip_handler) # adding our function
s.addMsgHandler("/camera/fullscreen", cameraFullscreen_handler) # adding our function

s.addMsgHandler("/video/play", videoPlay_handler) # adding our function
s.addMsgHandler("/video/pause", videoPause_handler) # adding our function
s.addMsgHandler("/video/stop", videoStop_handler) # adding our function
s.addMsgHandler("/video/slower", videoSlower_handler) # adding our function
s.addMsgHandler("/video/faster", videoFaster_handler) # adding our function

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
    while DISPLAY.loop_running():
	DISPLAY.clear()
	i = 1
	if (scene < 2): # scene 2 implicit empty 
  		for o in objects[scene]:	
			o.draw()
	  		o.rotateIncX((rotationX+i)*0.01)
			o.rotateIncY((rotationY+i)*0.12)
			o.rotateIncZ((rotationZ-i)*0.02)
			#o.position(xloc, yloc, 15.0)
			i = i + 1
	
except KeyboardInterrupt :
    camera.close()
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
