from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import multiprocessing
import time
import cv2
import numpy as np
import OSC

class EACamera:
	# opencv functions

	def nothing(self,*arg, **kw):
    		pass

	def clock(self):
    		return cv2.getTickCount() / cv2.getTickFrequency()

	def draw_motion_comp(self,vis, (x, y, w, h), angle, color):
    		cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 255, 0))
    		r = min(w/2, h/2)
    		cx, cy = x+w/2, y+h/2
    		angle = angle*np.pi/180
    		cv2.circle(vis, (cx, cy), r, color, 3)
    		cv2.line(vis, (cx, cy), (int(cx+np.cos(angle)*r), int(cy+np.sin(angle)*r)), color, 3)



	def __init__(self):
		self.camera = None
		self.MHI_DURATION = 0.5
		self.DEFAULT_THRESHOLD = 32
		self.MAX_TIME_DELTA = 5.9
		self.MIN_TIME_DELTA = 0.05
		self.thrs = 32
		# dont know if these are good starting values
		self.vflip = 0
		self.hflip = 0
		self.framerate = 25
		self.saturation = 0
		self.sharpness = 0
		self.shutter = 0
		self.x = 0
		self.y = 0
		self.width = 640
		self.height = 480
		self.zoomX = 0.0
		self.zoomY = 0.0
		self.zoomW = 1.0
		self.zoomH = 1.0
		self.fullscreen = False
		self.alpha = 128
		self.effect = 0
		self.effects = [ 
		'none','negative','solarize','sketch','denoise','emboss','oilpaint','hatch','gpen','pastel','watercolor','film','blur','saturation','colorswap','washedout','posterise','colorpoint','colorbalance','cartoon','deinterlace1','deinterlace2']

	def close(self):
		if (self.camera != None):
			self.camera.close()

	def start(self):
                print "start camera"
		if (self.camera == None):# initialize the camera to given values
			self.camera = picamera.PiCamera()
			self.camera.resolution = (self.width,self.height)
			self.camera.start_preview()
			self.camera.framerate = self.framerate
			self.camera.preview_fullscreen = self.fullscreen
			self.camera.preview_window = (self.x,self.y,self.width,self.height)
			self.camera.preview_alpha = self.alpha
			self.camera.hflip = self.hflip
			self.camera.vflip = self.vflip
			self.camera.saturation = self.saturation
			self.camera.sharpness = self.sharpness
			self.camera.shutter_speed = self.shutter
			self.camera.image_effect = self.effects[self.effect]
			# initialize OSC
			#self.client = OSC.OSCClient()
			#self.client.connect( ('127.0.0.1', 9000) ) # note that the argument is a tupple and not two arguments
			self.initialGrab = True

		else:
			self.camera.start_preview()

	def processFrame(self):
		time.sleep(2)
		print "start frame processing"
		self.rawCapture = PiRGBArray(self.camera)
		while (self.camera != None):
		 #for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			print "a frame"

			self.camera.capture(self.rawCapture, format = "bgr", use_video_port=True )
			image = self.rawCapture.array
			if self.initialGrab:
				self.h, self.w = image.shape[:2]
				self.prev_frame = image.copy()
    				self.motion_history = np.zeros((self.h, self.w), np.float32)
    				hsv = np.zeros((self.h, self.w, 3), np.uint8)
    				hsv[:,:,1] = 255
				self.initialGrab = False
        			self.rawCapture.truncate(0)
   			else:
				frame_diff = cv2.absdiff(image, self.prev_frame)
				self.prev_frame = image.copy()
        			gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
				ret, motion_mask = cv2.threshold(gray_diff, self.thrs, 1, cv2.THRESH_BINARY)
				self.timestamp = self.clock()
        			cv2.updateMotionHistory(motion_mask, self.motion_history, self.timestamp, self.MHI_DURATION)
        			mg_mask, mg_orient = cv2.calcMotionGradient( self.motion_history, self.MAX_TIME_DELTA, self.MIN_TIME_DELTA, apertureSize=5 )
        			seg_mask, seg_bounds = cv2.segmentMotion(self.motion_history, self.timestamp, self.MAX_TIME_DELTA)

				for i, rect in enumerate([(0, 0, self.w, self.h)] + list(seg_bounds)):
            				x, y, rw, rh = rect
            				area = rw*rh
            				if area < 16**2:#64
                				continue
            				silh_roi   = motion_mask   [y:y+rh,x:x+rw]
            				orient_roi = mg_orient     [y:y+rh,x:x+rw]
            				mask_roi   = mg_mask       [y:y+rh,x:x+rw]
            				mhi_roi    = self.motion_history[y:y+rh,x:x+rw]
            				if cv2.norm(silh_roi, cv2.NORM_L1) < area*0.05:
                				continue
            				angle = cv2.calcGlobalOrientation(orient_roi, mask_roi, mhi_roi, self.timestamp, self.MHI_DURATION)
            				#color = ((255, 0, 0), (0, 0, 255))[i == 0]
            				#draw_motion_comp(image, rect, angle, color)
	    				if i>0 and i < 5: 
						address = "/CV"+str(i)
						#msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
						#msg.setAddress(address)
						if isinstance(x, np.generic):
    							value = np.asscalar(x)
						else:
							value = x
						#msg.append(value)
						#client.send(msg) # now we dont need to tell the client the address anymore
						print "%s %s" % (address , value)

        				# show the frame
					#cv2.flip(image,0,image)
        				#cv2.imshow('EArtist', image)
        				#cv2.imshow('motempl', gray_diff)

        				#key = cv2.waitKey(1) & 0xFF

        				# clear the stream in preparation for the next frame
       				self.rawCapture.truncate(0)
			if (self.camera == None):
				break;
			print "restart or end processing frame"
		print "done with process frame"



	def stop(self):
                print "stop camera"
		if (self.camera != None):
			self.camera.stop_preview()
			self.camera.close()
			self.camera = None

	def setAlpha(self,alpha):
		if (self.camera != None):
			self.camera.preview_alpha = alpha
		self.alpha = alpha

	def setFrame(self,x,y,width,height):
		if (self.camera != None):
			self.camera.preview_fullscreen = False
			self.camera.preview_window = (x,y,width,height)
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.fullscreen = False

	# full needs to be boolean
	def setFullscreen(self,full):
		if (self.camera != None):
			self.camera.preview_fullscreen = full
		self.fullscreen = full

	# flip needs to be a boolean	
	def setHFlip(self,flip):
		if (self.camera != None):
			self.camera.hflip = flip
		self.hflip = flip

	def setVFlip(self,flip):
		if (self.camera != None):
			self.camera.vflip = flip
		self.vflip = flip

	def setX(self,x):
		self.x = x
		if (self.camera != None):
			self.camera.preview_window = (self.x,self.y,self.width,self.height)
	def setY(self,y):
		self.y = y
		if (self.camera != None):
			self.camera.preview_window = (self.x,self.y,self.width,self.height)
	def setWidth(self,w):
		self.width = w
		if (self.camera != None):
			self.camera.preview_window = (self.x,self.y,self.width,self.height)
	def setHeight(self,h):
		self.height = h
		if (self.camera != None):
			self.camera.preview_window = (self.x,self.y,self.width,self.height)

	# ------ camera settings --------
	# saturation is integer between -100 and 100
	def setSaturation(self,sat):
		self.saturation = sat
		if (self.camera != None):
			self.camera.saturation = sat
	
	# sharpness is integer between -100 and 100
	def setSharpness(self,sharp):
		self.sharpness = sharp
		if (self.camera != None):
			self.camera.sharpness = sharp
	
	# 0 is auto
	def setShutterspeed(self,shutter):
		self.shutter = shutter
		if (self.camera != None):
			self.camera.shutter_speed = shutter

	def setEffect(self,effect):
		self.effect = effect
		if (self.camera != None):
			if (effect > -1) and (effect < len(self.effects) ):
				self.camera.image_effect = self.effects[effect]

	def setFramerate(self,rate):
		self.framerate = rate
		if (self.camera != None):
			self.camera.framerate = rate

	def setZoomX(self,x):
		self.zoomX = x
		if (self.camera != None):
			self.camera.zoom = (self.zoomX,self.zoomY,self.zoomW,self.zoomH)

	def setZoomY(self,y):
		self.zoomY = y
		if (self.camera != None):
			self.camera.zoom = (self.zoomX,self.zoomY,self.zoomW,self.zoomH)

	def setZoomW(self,w):
		self.zoomW = w
		if (self.camera != None):
			self.camera.zoom = (self.zoomX,self.zoomY,self.zoomW,self.zoomH)

	def setZoomH(self,h):
		self.zoomH = h
		if (self.camera != None):
			self.camera.zoom = (self.zoomX,self.zoomY,self.zoomW,self.zoomH)
	
        def oscHandler(self, addr, tags, stuff, source):
                if isinstance(stuff[0],basestring):
                        if stuff[0] == "alpha":
                                if isinstance(stuff[1],int):
                                        self.setAlpha(stuff[1])
                        elif stuff[0] == "effect":
                                if isinstance(stuff[1],int):
                                        self.setEffect(stuff[1])
                        elif stuff[0] == "saturation":
                                if isinstance(stuff[1],int):
                                        self.setSaturation(stuff[1])
                        elif stuff[0] == "sharpness":
                                if isinstance(stuff[1],int):
                                        self.setSharpness(stuff[1])
                        elif stuff[0] == "shutter":
                                if isinstance(stuff[1],int):
                                        self.setShutterspeed(stuff[1])
                        elif stuff[0] == "x":
                                if isinstance(stuff[1],int):
                                        self.setX(stuff[1])
                        elif stuff[0] == "y":
                                if isinstance(stuff[1],int):
                                        self.setY(stuff[1])
                        elif stuff[0] == "width":
                                if isinstance(stuff[1],int):
                                        self.setWidth(stuff[1])
                        elif stuff[0] == "height":
                                if isinstance(stuff[1],int):
                                        self.setHeight(stuff[1])
                        elif stuff[0] == "fullscreen":
                                if isinstance(stuff[1],int):
                                        if stuff[1] == 0:
                                                self.setFullscreen(False)
                                        else:
                                                self.setFullscreen(True)
                                                
                        elif stuff[0] == "framerate":
                                if isinstance(stuff[1],int):
                                        self.setFramerate(stuff[1])
                        elif stuff[0] == "hflip":
                                if isinstance(stuff[1],int):
                                        if stuff[1] == 0:
                                                self.setHFlip(False)
                                        else:
                                                self.setHFlip(True)
                        elif stuff[0] == "vflip":
                                if isinstance(stuff[1],int):
                                        if stuff[1] == 0:
                                                self.setVFlip(False)
                                        else:
                                                self.setVFlip(True)
                        elif stuff[0] == "zoomx":
                                if isinstance(stuff[1],float):
                                        self.setZoomX(stuff[1])
                        elif stuff[0] == "zoomy":
                                if isinstance(stuff[1],float):
                                        self.setZoomY(stuff[1])
                        elif stuff[0] == "zoomw":
                                if isinstance(stuff[1],float):
                                        self.setZoomW(stuff[1])
                        elif stuff[0] == "zoomh":
                                if isinstance(stuff[1],float):
                                        self.setZoomH(stuff[1])
                                        
                        elif stuff[0] == "switch":
                                if isinstance(stuff[1],int):
                                        if stuff[1]>0:
                                                self.start()
                                        else:
                                                self.stop()
