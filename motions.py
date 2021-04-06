#Python 2/3 compatibility
from __future__ import print_function 

try:
	#import future        # pip install future
	#import builtins      # pip install future
	#import past          # pip install future
	#import six  
	import sys    
	import math
	import numpy as np
	from collections import deque
except ImportError as err:
	print("Couldn't load module: %s" % (err))
	exit(2)


def orbitintegrator(startpos, startspeed, startdir, masses, radii, positions, indices,  GFACTOR, SCW, SCH, mod, iterations=1000, tjump=1):
	speed = startspeed
	direction = startdir
	outpos = []
	outpos.append((startpos[0]+speed*np.cos(direction), startpos[1]+speed*np.sin(direction)))
	for t in range(int(iterations/tjump-1)):
		j = tjump*t
		planetx = []
		planety =[]
		for p in range(len(masses)):
			dx = -positions[p][0][(j+indices[p])%len(positions[p][0])][0]+outpos[t][0]
			dy = -positions[p][0][(j+indices[p])%len(positions[p][0])][1]+outpos[t][1]
			planetx.append(dx)
			planety.append(dy)
			if dx**2 + dy**2 < radii[p]*7.:
				return outpos
		forcex, forcey = force(masses, planetx, planety, GFACTOR, SCW,SCH, modified=mod)
		speedx = speed*math.cos(direction) + forcex
		speedy = speed*math.sin(direction) + forcey
		speed =math.sqrt(speedx**2+speedy**2)
		direction = math.atan2(speedy, speedx)
		outpos.append((outpos[t][0]+speed*np.cos(direction),outpos[t][1]+speed*np.sin(direction)))


	return outpos

def force(masses, positionsx, positionsy, GFACTOR, SCW,SCH,modified=[]):
	totfx =0.0
	totfy =0.0
	GFACTOR*=1200./float(SCH)
	if len(modified)==0:
		modified = np.zeros(len(positionsx))
	for i in range(len(positionsx)):
		positionx =float(float(positionsx[i])/float(SCW))	
		positiony =float(float(positionsy[i])/float(SCH))
		direction = math.atan2(positiony, positionx) -np.pi
		rad = math.sqrt(positionx**2 + positiony**2)
		force = GFACTOR*masses[i]*(1./(rad**2) + modified[i]*rad)
		totfx += force*np.cos(direction)
		totfy += force*np.sin(direction)

	return totfx, totfy


def add_vels(speed1, speed2, dir1, dir2):
	vx = speed1*np.cos(dir1)+speed2*np.cos(dir2)
	vy = speed1*np.sin(dir1)+speed2*np.sin(dir2)
	speedtot= math.sqrt(vx**2+vy**2)
	dirtot = math.atan2(vy, vx)
	return speedtot, dirtot

def anal_orbit(noplans, masses, positions):
	positionarrays=[]
	if noplans != len(masses) or noplans != len(positions):
		print("Analytic orbits cannot be calculated. Array mismatch.")
		exit()
	#Note will need to be able to recognise when 'period' is over.
	#The array length will define the 'period' of the orbit - e.g. len(positionarrays[0])
	#Put xy coordinates in 'tuple' - e.g. positionarrays[0].append((x,y))	
	#Will need to insert a central star & start/destination.. flags for their treatment will need to be written into leveldata.
	#The flag for central star/centre of mass will need to be read here.
	return positionarrays

def PlanetOrbit(mcentre, G, theta0, radius, SCW, SCH, CENTER, mtype='orbit', size = 10000, buff=3.0, flag = 0, perioddiff = 0, xdisp = 0., ydisp=0.):
	if flag == 0:
		if mtype == 'orbit':
			if perioddiff ==1:
				size = int(size*pow((float(radius)/float(SCW)),1.5))
			#Create linspace between 0 and 2pi of size 'size'
			theta = np.linspace(theta0,2.*np.pi+theta0, num=size)
			xpos = SCW/2+radius*np.cos(theta)
			ypos = SCH/2+radius*(float(SCH)/float(SCW))*np.sin(theta)
		elif mtype == 'linL2R':
			if perioddiff ==1:
				size = int(size*pow((float(radius)/float(SCW)),1.5))
			else:
				size = int(size*(1.+buff))
			xfixed = SCW/2+ radius*np.cos(theta0)
			xpos = xfixed*np.ones(size)
			param = np.linspace(-0.5,0.5+buff, num=size)
			ypos = float(SCH/2) + float(SCH)*(xpos[0] -float(SCW/2))*param/float(SCW/2)
		elif mtype == 'linR2L':
			if perioddiff ==1:
				size = int(size*pow((float(radius)/float(SCW)),1.5))
			else:
				size = int(size*(1.+buff))
			xfixed = CENTER[0]+ radius*np.cos(theta0)
			xpos = xfixed*np.ones(size)
			param = np.linspace(-0.5,0.5+buff, num=size)
			ypos = float(SCH/2) - float(SCH)*(xpos[0] -float(SCW/2))*param/float(SCW/2)
		elif mtype == 'linU2D':
			if perioddiff ==1:
				size = int(size*pow((float(radius)/float(SCW)),1.5))
			else:
				size = int(size*(1.+buff))
			yfixed = SCH/2+ radius*np.sin(theta0)
			ypos = yfixed*np.ones(size)
			param = np.linspace(-0.5,.5+buff, num=size)
			xpos = float(SCW/2) + float(SCW)*(ypos[0] -float(SCH/2))*param/float(SCH/2)
		elif mtype =='linD2U':
			if perioddiff ==1:
				size = int(size*pow((float(radius)/float(SCW)),1.5))
			yfixed = SCH/2+ radius*np.sin(theta0)
			ypos = yfixed*np.ones(size)
			param = np.linspace(-0.5,.5+buff, num=size)
			xpos = float(SCW/2)  - float(SCW)*(ypos[0] -float(SCH/2))*param/float(SCH/2)
	
		positions = np.zeros((size-1,2))
		direction = np.zeros(size-1)
		speed = np.zeros(size-1)
		for i in range(size-1):
			positions[i] = (xpos[i]+xdisp,ypos[i]+ydisp)
			direction[i] = math.atan2(ypos[i+1]-ypos[i],xpos[i+1]-xpos[i])
			speed[i] = math.sqrt((ypos[i+1]-ypos[i])**2+(xpos[i+1]-xpos[i])**2)

	else:
		positions = np.zeros((size-1,2))
		direction = np.zeros(size-1)
		speed = np.zeros(size-1)
		for i in range(size-1):
			positions[i] = (SCW/2 + xdisp, SCH/2+ydisp)
	
		
	
	return positions, direction, speed
	

def CollisionDetect(rocket, Circle):
        if math.sqrt(((Circle.x-rocket.x)**2)  +  ((Circle.y-rocket.y)**2)  ) <= Circle.rad:
            return True

