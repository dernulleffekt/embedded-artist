import pyomxplayer
import picamera
class EACamera:
	def __init__(self):
		self.omx = None
		self.camera = picamera.PiCamera()
		self.camera.framerate = 25
		# dont know if these are good starting values
		self.x = 0
		self.y = 0
		self.width = 800
		self.height = 600
		self.zoomX = 0.0
		self.zoomY = 0.0
		self.zoomW = 1.0
		self.zoomH = 1.0

		self.effects = [ 
		'none','negative','solarize','sketch','denoise','emboss','oilpaint','hatch','gpen','pastel','watercolor','film','blur','saturation','colorswap','washedout','posterise','colorpoint','colorbalance','cartoon','deinterlace1','deinterlace2']

	def close(self):
		if (self.omx != None):
			self.omx.stop()

	def start(self):
		self.camera.start_preview()

	def stop(self):
		self.camera.stop_preview()
	def setAlpha(self,alpha):
		self.camera.preview_alpha = alpha

	def setFrame(self,x,y,width,height):
		self.camera.preview_fullscreen = False
		self.camera.preview_window = (x,y,width,height)
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	# full needs to be boolean
	def setFullscreen(self,full):
		self.camera.preview_fullscreen = full

	# flip needs to be a boolean	
	def setHFlip(self,flip):
		self.camera.hflip = flip

	def setVFlip(self,flip):
		self.camera.vflip = flip
	
	def setX(self,x):
		self.x = x
		self.camera.preview_window = (self.x,self.y,self.width,self.height)
	def setY(self,y):
		self.y = y
		self.camera.preview_window = (self.x,self.y,self.width,self.height)
	def setWidth(self,w):
		self.width = w
		self.camera.preview_window = (self.x,self.y,self.width,self.height)
	def setHeight(self,h):
		self.height = h
		self.camera.preview_window = (self.x,self.y,self.width,self.height)

	# ------ camera settings --------
	# saturation is integer between -100 and 100
	def setSaturation(self,sat):
		self.camera.saturation = sat
	
	# sharpness is integer between -100 and 100
	def setSharpness(self,sharp):
		self.camera.sharpness = sharp
	
	# 0 is auto
	def setShutterspeed(self,shutter):
		self.camera.shutter_speed = shutter

	def setEffect(self,effect):
		self.camera.image_effect = self.effects[effect]

	def setFramerate(self,rate):
		self.camera.framerate = rate

	def setZoomX(self,x):
		self.zoomX = x
		self.camera.zoom = (self.zoomX,self.zoomY,self.zoomW,self.zoomH)

	def setZoomY(self,y):
		self.zoomY = y
		self.camera.zoom = (self.zoomX,self.zoomY,self.zoomW,self.zoomH)

	def setZoomW(self,w):
		self.zoomW = w
		self.camera.zoom = (self.zoomX,self.zoomY,self.zoomW,self.zoomH)

	def setZoomH(self,h):
		self.zoomH = h
		self.camera.zoom = (self.zoomX,self.zoomY,self.zoomW,self.zoomH)
	
	# --- video player functions ---
	def playVideo(self,videofile):
		self.omx = pyomxplayer.OMXPlayer(videofile)
	
	def stopVideo(self):
		self.omx.stop()

	def pauseVideo(self):
		self.omx.toggle_pause()
	
	def fasterVideo(self):
		self.omx.set_faster()
	def slowerVideo(self):
		self.omx.set_slower()
