import pyomxplayer
import picamera
class EACamera:
	def __init__(self):
		self.omx = None
		self.camera = None
		# dont know if these are good starting values
		self.vflip = 0
		self.hflip = 0
		self.framerate = 25
		self.saturation = 0
		self.sharpness = 0
		self.shutter = 0
		self.x = 0
		self.y = 0
		self.width = 800
		self.height = 600
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
		if (self.omx != None):
			self.omx.stop()
		if (self.camera != None):
			self.camera.close()

	def start(self):
		if (self.camera == None):# initialize the camera to given values
			self.camera = picamera.PiCamera()
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
		else:
			self.camera.start_preview()

	def stop(self):
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
	
	# --- video player functions ---
	def playVideo(self,videofile):
		if (self.omx != None):
			self.omx.stop()
		self.omx = pyomxplayer.OMXPlayer(videofile)
	
	def stopVideo(self):
		self.omx.stop()

	def pauseVideo(self):
		self.omx.toggle_pause()
	
	def fasterVideo(self):
		self.omx.set_faster()
	def slowerVideo(self):
		self.omx.set_slower()
