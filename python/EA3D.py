import pi3d
class EA3D:
    def __init__(self):
        # setup 3d
        self.backgroundRed = 0.0
	self.backgroundGreen = 0.0 
	self.backgroundBlue = 0.0
        self.backgroundAlpha = 1.0

        self.DISPLAY = pi3d.Display.create(frames_per_second = 25,background = (0.0, 0.0, 0.0, 1.0))
        mylight = pi3d.Light(lightpos=(-2.0, -1.0, 10.0), lightcol=(1.0, 1.0, 0.8), lightamb=(0.25, 0.2, 0.3))

        self.shader = pi3d.Shader("uv_light")
        flatshader = pi3d.Shader("uv_flat")
        self.scenes  = {}
        self.scene = 0
        self.scale = 2.
        self.xloc = 1.0
        self.yloc = 1.0
        self.zloc = 15.0
        self.rotationX = 0.0
        self.rotationY = 0.0
        self.rotationZ = 0.0
        self.vrcamxloc = 1.0
        self.vrcamyloc = 1.0

    def loadObjectInScene(self,filename,sceneID):
	model  = pi3d.Model(file_string=filename, x=0, y=-1, z=-40, sx=2., sy=2., sz=2.)
        model.set_shader(self.shader)
	model.position(self.xloc,self.yloc, self.zloc)
	model.scale(self.scale,self.scale,self.scale)
	model.rotateToX(self.rotationX)
	model.rotateToY(self.rotationY)
	model.rotateToZ(self.rotationZ)
        self.scenes.update({sceneID : model})

	print "loaded "+ filename + " in "+ sceneID

    def removeScene(self,sceneID):
	del self.scenes[sceneID]

    def setScene(self,sceneID):
        self.scene = sceneID
	print "switch to scene: "+ str(sceneID)

    def posX(self, x):
        self.xloc = x
        for o in self.scenes:	
		self.scenes[o].position(self.xloc,self.yloc, self.zloc)

    def posY(self,y):
        self.yloc = y	
        for o in self.scenes:	
		self.scenes[o].position(self.xloc, self.yloc, self.zloc)

    def posZ(self,z):
        self.zloc = z	
        for o in self.scenes:	
		self.scenes[o].position(self.xloc, self.yloc, self.zloc)

    def cameraX(self,x):
        self.vrcamxloc = x
        from pi3d.Camera import Camera
        vrcamera = Camera.instance()
        if vrcamera:
            vrcamera.position((self.vrcamxloc,self.vrcamyloc,1.0))

    def cameraY(self,y):
        self.vrcamyloc = y	
        from pi3d.Camera import Camera
        vrcamera = Camera.instance()
        if vrcamera:
            vrcamera.position((self.vrcamxloc,self.vrcamyloc,1.0))
	
    def rotX(self,x):
        self.rotationX = x	
        for o in self.scenes:	
	  	self.scenes[o].rotateToX(x)

    def rotY(self,y):
        self.rotationY = y
        for o in self.scenes:	
	  	self.scenes[o].rotateToY(y)

    def rotZ(self,z):
        self.rotationZ = z
        for o in self.scenes:	
		self.scenes[o].rotateToZ(z)

    def setScale(self,s):
        self.scale = s	
        for o in self.scenes:	
		self.scenes[o].scale(self.scale,self.scale,self.scale)


        
    def setBackground(self,r,g,b,a):
        #self.DISPLAY = pi3d.Display.create(frames_per_second = 25,background = (self.backgroundRed,self.backgroundGreen, self.backgroundBlue, self.backgroundAlpha))
	self.DISPLAY.set_background(r,g,b,a)
	#print "set background to "+ str(r) + " "+str(g)+ " "+str(b)+" "+str(a) 

    def oscHandler(self, addr, tags, stuff, source):
        if isinstance(stuff[0],basestring):
            if stuff[0] == "posX":
                if isinstance(stuff[1],float):
                   self.posX(stuff[1])
            elif stuff[0] == "posY":
                if isinstance(stuff[1],float):
                    self.posY(stuff[1])
            elif stuff[0] == "posZ":
                if isinstance(stuff[1],float):
                    self.posZ(stuff[1])
            elif stuff[0] == "rotationX":
                if isinstance(stuff[1],float):
                    self.rotX(stuff[1])
            elif stuff[0] == "rotationY":
                if isinstance(stuff[1],float):
                    self.rotY(stuff[1])
            elif stuff[0] == "rotationZ":
                if isinstance(stuff[1],float):
                    self.rotZ(stuff[1])
            elif stuff[0] == "scale":
                if isinstance(stuff[1],float):
                    self.setScale(stuff[1])
            elif stuff[0] == "backgroundRed":
                if isinstance(stuff[1],float):
		    self.backgroundRed = stuff[1]
                    self.setBackground(self.backgroundRed, self.backgroundGreen, self.backgroundBlue, self.backgroundAlpha)
            elif stuff[0] == "backgroundGreen":
                if isinstance(stuff[1],float):
		    self.backgroundGreen = stuff[1]
                    self.setBackground(self.backgroundRed, self.backgroundGreen, self.backgroundBlue, self.backgroundAlpha)
            elif stuff[0] == "backgroundBlue":
                if isinstance(stuff[1],float):
		    self.backgroundBlue = stuff[1]
                    self.setBackground(self.backgroundRed, self.backgroundGreen, self.backgroundBlue, self.backgroundAlpha)
            elif stuff[0] == "backgroundAlpha":
                if isinstance(stuff[1],float):
		    self.backgroundAlpha = stuff[1]
                    self.setBackground(self.backgroundRed, self.backgroundGreen, self.backgroundBlue, self.backgroundAlpha)
	    elif stuff[0] == "loadModel":
		if isinstance(stuff[1],basestring):
			if isinstance(stuff[2],basestring):
				self.loadObjectInScene(stuff[1],stuff[2])

            elif stuff[0] == "camera":
                if isinstance(stuff[1],basestring):
                    if stuff[1] == "posX":
                        if isinstance(stuff[2],float):
                            self.cameraX(stuff[2])
                    if stuff[1] == "posY":
                        if isinstance(stuff[2],float):
                            self.cameraY(stuff[2])
            elif stuff[0] == "scene":
                 self.setScene(stuff[1])

            elif stuff[0] == "removeScene":
                 self.removeScene(stuff[1])
	    else: 
		print "unhandled command:" + stuff[0]
