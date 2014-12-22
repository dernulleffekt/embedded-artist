import pyomxplayer
class EAVideo:
	def __init__(self):
		self.omx = None
		
	def close(self):
		if (self.omx != None):
			self.omx.stop()

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

        def oscHandler(self,addr, tags, stuff, source):
                if isinstance(stuff[0],basestring):
                        if stuff[0] == "play":
                                if isinstance(stuff[1],basestring):
                                        self.playVideo(stuff[1])
                        elif stuff[0] == "pause":
                                self.pauseVideo()
                        elif stuff[0] == "stop":
                                self.stopVideo()
                        elif stuff[0] == "faster":
                                self.fasterVideo()
                        elif stuff[0] == "slower":
                                self.slowerVideo()
                                
                        
