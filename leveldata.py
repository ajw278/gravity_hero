#leveldata module for gravgame
#All level info eventually will be defined here

#Python 2/3 compatibility
from __future__ import print_function 

try:
	#import future        # pip install future
	#import builtins      # pip install future
	#import past          # pip install future
	#import six  
	import sys    
	import numpy as np
	import math
	import pygame
except ImportError as err:
	print("Couldn't load module: %s" % (err))
	exit(2)


#Assign colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
DARKRED = (75,   0,   0)

def levdat(level, SCW, SCH, CENTER):
	if level ==1:
		#Level text
		levtext = ["BEYOND MARS!", "Here's a good mission to see how gravity", "changes the motion of your rocket.", "What happens when you fly close to Mars?", "Try and land the rocket on the asteroid that's", "travelling past behind Mars.", " ", " ", " ", "Use the up/down keys to power your rocket up/down.", "Use the left/right keys to rotate the direction", "of your rocket. Ask the astronomers if you need help!"]
		#G for this level
		G = .0001
		#starting direction of the rocket 
		rocketpoint = 0.0
		#Normally set this the same as direction of rocket (this position angle relative to planet)
		rocketangle = 0.0
		#max rocket swivel - plus/minus (how far rocket can turn - should be less than 90 degrees)
		rocketswiv = np.pi/2.
		#Max power
		rockpow = 12
		#Flags for the planet treatments: 0 - regular, 1- starting planet, 2 - destination planet, 3 - central mass
		flags = [2, 1, 3]
		#rocket radius
		rockrad = .5
		#number of planets
		no_plans = 3
		modgrav=[0,0,0]
		#motion type - choose from orbit, lin[L2R/R2L/U2D/D2U] (move up and down rel to central mass with respective directions)
		mtype = ['linL2R','linL2R','linL2R']
		#planet masses
		masses = [4., 25., 25.0]
		#planet names - this needs to be the name of the image file (e.g. 'Mars', gives 'Mars.png')
		names = ['Asteroid', 'Earth', 'Mars']
		#Planet radii
		radii = [5. ,10., 8.]
		#planet positions in theta0, r	(from central mass)
		rpositions = [(0.0, SCW/10.), (np.pi, SCW/2.), (0.0, 0.0)]
		#x/y displacement (define offset of central mass)
		xdisp = SCW/5.
		ydisp = 0.
		#xyposition calculate (from defined r, theta0)
		positions  = []
		for i in range(len(rpositions)):
			if flags[i]!=3:
				positions.append((CENTER[0]+rpositions[i][1]*np.cos(rpositions[i][0]), CENTER[1]+rpositions[i][1]*(float(SCH)/float(SCW))*np.sin(rpositions[i][0])))
			else:
				positions.append((CENTER[0], CENTER[1]))
		#Slowing factor for planets - bigger=slower (too slow it will be jumpy)
		sfactor = 1000
		#Background
		bgfile = pygame.image.load("./graphics/Level1BG.jpg")
		bgfile = pygame.transform.scale(bgfile, (SCW, SCH))
		#special rotation - will rotate the rocket with the planet
		specialrocketrot = 0
		#different orbital period for different radii
		difforbs = 0
		#rocket speed factor
		rspdfact = float(1./1000.)
		rspdfact *= 1200.
		#Static ICs
		static = False
		#Rocket rotation rate factor
		rotrate = 10.
		#Guide length
		niters = 100
		#Frames limit before reset
		tlim = 1500
	elif level ==2:
		levtext = ["BINARY FLYBY!", "In this mission, we're going to try to", "get past a couple of white dwarfs and", "land on another the asteroid the other side.", " ", " ","In reality, a White Dwarf is about 100 times", "smaller (in radius) than the Sun.","This makes them roughly Earth-sized but they" ,  "still contain about half the material that the Sun does.", "They are very dense objects!"]
		G = .0001
		rocketpoint = 0.0
		rocketangle = 0.0
		rockpow =8
		rocketswiv = np.pi/2.5
		flags = [0, 0, 3, 1, 2]
		rockrad = .5
		no_plans = 5
		modgrav=[0,0,0,0,0]
		mtype = ['orbit','orbit','orbit', 'linR2L', 'linR2L']
		#Note that the central object is not physical here, I think I've coded out the need for it, but I can't remember so I'm leaving it in to be safe (and lazy!)
		masses = [50., 50., 0., 2., 2.]
		names = ['WhiteDwarf', 'WhiteDwarf', 'WhiteDwarf', 'Asteroid', 'Asteroid']
		radii = [10. ,10., 0., 3., 5.]
		rpositions = [(np.pi/2., SCW/10.), (-np.pi/2., SCW/10.), (0.0, 0.0), (np.pi, SCW/3.), (0.0, SCW/3.)]
		xdisp = 0.
		ydisp = 0.
		positions  = []
		for i in range(len(rpositions)):
			if flags[i]!=3:
				positions.append((int(SCW/2+rpositions[i][1]*np.cos(rpositions[i][0])), SCH/2+rpositions[i][1]*(float(SCH)/float(SCW))*np.sin(rpositions[i][0])))
			else:
				positions.append((SCW/2, SCH/2))
		sfactor = 1000
		#Background
		bgfile = pygame.image.load("./graphics/Level2BG.jpg")
		bgfile = pygame.transform.scale(bgfile, (SCW, SCH))
		specialrocketrot = 0
		difforbs = 0
		rspdfact = float(1./1000.)
		rspdfact *= 1200.
		static = False
		rotrate = 10.
		niters = 100
		tlim = 1500
	elif level ==3:
		levtext = ["SLINGSHOT TO JUPITER!", "In this mission, we're going to try to replicate", "a simple slingshot. The idea is to use the", "gravity of Earth/Mars to accelerate the rocket", "into a wider orbit, as shown in the Juno video,","and land on 'Jupiter' - the outer planet.", "It's tricky, but try to aim the rocket so it will come back", "around close to Earth to get as much", "acceleration as possible!", "Remember the planets will move once you've launched." " ", " ", "If you're having trouble,", "try asking one of the astronomers for help!"]
		G = .0001
		rocketpoint = 1.0053
		rocketangle = np.pi/2.
		rockpow =13
		rocketswiv = 0.3
		flags = [3,1, 0, 2]
		rockrad = .3
		no_plans = 4
		modgrav=[.0, 0.,0.,0.]
		mtype = ['orbit','orbit','orbit', 'orbit']
		masses = [9., 0.5, .5, 2., ]
		names = ['Sun', 'Earth', 'Mars', 'Jupiter']
		radii = [2.5 ,1., 0.8, 3.]
		rpositions = [(0.0, 0.),  (0.0, SCW/12.), (np.pi, SCW/8.), (2.*np.pi/3., float(SCW)/2.5)]
		xdisp = 0.
		ydisp = 0.
		positions  = []
		for i in range(len(rpositions)):
			if flags[i]!=3:
				positions.append((int(SCW/2+rpositions[i][1]*np.cos(rpositions[i][0])), SCH/2+rpositions[i][1]*(float(SCH)/float(SCW))*np.sin(rpositions[i][0])))
			else:
				positions.append((SCW/2, SCH/2))
		sfactor = 20000
		#Background
		bgfile = pygame.image.load("./graphics/Level3BG.jpg")
		bgfile = pygame.transform.scale(bgfile, (SCW, SCH))
		specialrocketrot = 1
		difforbs =1
		rspdfact = float(1./2800.)
		rspdfact *= 1200. #float(SCH)
		static = True
		rotrate = 1.
		niters = 1000
		tlim = 1500
	else:
		print("No input defined for level %d." %level)
		sys.exit()

	if len(masses) != no_plans or len(names)!=no_plans or len(positions) != no_plans:
		print("Planet arrays not defined correctly! Check level %d." %level)
		sys.exit()
	
	leveldict = {'PLANETNo': no_plans, 'NAMES': names, 'STRTPOS': positions, 'FLAGS': flags, 'PLYRDIR': rocketpoint, 'PLYRSWIV': rocketswiv, 'RADII': radii, 'PLYRRAD': rockrad, 'GVAL': G, 'MASS': masses, 'BG': bgfile, 'RSTRTPOS': rpositions, 'SFACTOR': sfactor, 'MTYPE': mtype, 'XDISP': xdisp, 'YDISP': ydisp, 'TEXT': levtext, 'MAXPOW': rockpow, 'SROT': specialrocketrot, 'DORBS': difforbs, 'MODGRAV': modgrav, 'RSLOW': rspdfact, 'STATIC': static, 'ROTFACTOR':rotrate, 'POSANGLE': rocketangle, 'NITER': niters, 'TLIM': tlim}

	return leveldict

def helptext():
	helptext = ["The object of the game is to land your", "spacecraft on the target using the", "gravitational forces of the objects", "around you.", "", "Use the left and right arrows to aim", "and the up and down arrows to", "power up and down.", "The green line is an orbit guide,", "it will tell you where the rocket will go.", "Remember to power up enough to escape", "the object you are on!"," ", "If you need any further instructions," ,"ask one of the astronomers!" ]
	
	return helptext
