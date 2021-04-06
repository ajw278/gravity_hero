#Python 2/3 compatibility
from __future__ import print_function

try:
	#import future        # pip install future
	#import builtins      # pip install future
	#import past          # pip install future
	#import six      
	import sys
	from motions import *
	import numpy as np
	import random
	import math
	import os
	import getopt
	from socket import *
	import pygame, sys
	from pygame.locals import *
	from load import *
	import time
except ImportError as err:
	print("Couldn't load module: %s" % (err))
	sys.exit(2)

ANGLECONST = np.pi/2.

def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

def RESET_ROTATED_RECT(old_rect,rotated_image):
    old_pos=old_rect.left
    newrect=rotated_image.get_rect()
    newrect.left=old_pos
    return newrect

def rotate(gameObject, angle, rotations={},reinit=0):
    #print(rotations.get(gameObject))
    r = rotations.get(gameObject,0) + angle
    #print("Angle given: ", angle, "Rotations: ", rotations)
    if reinit == 1:
         rotations[gameObject] = angle
         r= angle
    else:
         rotations[gameObject]=r
    return pygame.transform.rotate(gameObject, r)


class Planet(pygame.sprite.Sprite):
	def __init__(self, startpos, name, mass, radius, SCW, SCH, orbitdat, directions, spd):
		pygame.sprite.Sprite.__init__(self)
		self.x =  int(startpos[0])
		self.y =  int(startpos[1])
		self.pos = orbitdat
		self.posind = 0
		self.start =  startpos
		self.rad = radius*float(SCW/100)
		self.image, self.rect = load_png(name +'.png')
		self.image = pygame.transform.scale(self.image, (int(self.rad), int(self.rad)))
		self.rad = self.rad/math.sqrt(3.)
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.rect.center = (self.x, self.y)
		self.dirs = directions
		self.vector=directions[0]
		self.vels = spd
		self.speed =spd[0]
		self.name = name
		self.area = screen.get_rect()
		self.mass = mass
		self.state = 'in'
		self.sch = SCH
		self.scw = SCW
		self.reinit()

	def isin(self, SCW, SCH):
		newpos = (self.x,self.y)
		if ((newpos[1] >-self.rad or abs(self.vector  + np.pi/2.)>np.pi/2.) and  (newpos[0] > -self.rad or abs(self.vector  + np.pi)>np.pi/2. or abs(self.vector - np.pi)>np.pi/2.) and (newpos[1] < SCH + self.rad or abs(self.vector  - np.pi/2.)>np.pi/2.) and (newpos[0]< SCW+ self.rad or abs(self.vector)>np.pi/2.)):
			return True
		else:
			return False

	def reinit(self):
		self.posind = 0
		self.state = 'in'
		self.update(self.scw, self.sch, 'start')
		
	def update(self, SCW, SCH, pstate):
		if self.posind >= len(self.pos) and pstate != 'start':
			#print("Reinitialisation due to overun of indexing in start.")
			self.posind = 0
		elif self.posind >= len(self.pos):
			#print("Reinitialisation due to overun of indexing.")
			self.posind = 0
		self.x = self.pos[self.posind][0]
		self.y = self.pos[self.posind][1]
		self.speed = self.vels[self.posind]
		self.vector = self.dirs[self.posind]
		self.posind+=1
		newpos = (self.x,self.y)
		if self.isin(SCW,SCH) or pstate != 'start':
	                self.rect.center = newpos
		else:
			self.state = 'off'
		


class Rocket(pygame.sprite.Sprite):
	"""'Rocket' which follows gravity
	Returns: rocket object
	Functions: rotateup, rotatedown, powerup, powerdown, fire
	Attributes: startpos, direction"""

	def __init__(self, dir0, dmax, mxpwer, rocket, radius, xstrt, ystrt,SCW, SCH, SCRECT, slow, rotspd):
		pygame.sprite.Sprite.__init__(self)
		#Do not need all the direction attributes... sort at some point
		self.x = xstrt
		self.y = ystrt
		self.direction = dir0
		self.dirmax = dir0+dmax
		self.dirmin = dir0-dmax
		self.d0 = dir0
		#Reason we need dirpoint as well as direction is that while not fired, direction != dirpoint
		self.dirpoint = dir0
		self.dirchange =0.0
		self.dirchangestat=0.0
		self.rotfact = rotspd
		self.lives = rocket
		self.rad = radius*SCW/30
		self.image, self.rect = load_png('Rocket.png')
		self.image = pygame.transform.scale(self.image, (int(self.rad), int(self.rad)))
		newimage =rotate(self.image, angledegs(-1.0*(self.dirpoint+ANGLECONST)))
		self.image = newimage
		self.image0 =self.image
		self.rad = self.rad/50.
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.sfactor = slow
		self.timer = 1
		self.crangle = 0.0

		#self.crashpic, self.crashrect = load_png('Crash.png')
		#self.crashpic = pygame.transform.scale(self.crashpic, (int(self.rad), int(self.rad)))

		#Want to change this at some point (area rectangle)
		self.area = SCRECT
		self.maxpower = mxpwer
		self.state="start"
		self.startvel=1
		self.speed =0.
		self.area = SCRECT
		self.x0 = xstrt
		self.y0 = ystrt
		self.strt = 0
		self.reinit()

	def reinit(self):
		pygame.event.clear()
		self.state = "start"
		self.timer =1
		self.x=self.x0
		self.y=self.y0
		self.dirpoint=self.d0
		self.dirchange = 0.0
		self.dirchangestat =0.0
		self.direction =self.d0
		self.speed=0.
		self.startvel=1
		self.image = self.image0
		self.strt =1
		self.rect = self.image.get_rect()
		self.rect.center=(self.x, self.y)

	def crash(self, planx, plany, planr, deltax, deltay, SCH):
		self.image, self.rect = load_png('Crash.png')
		if planr > SCH/35:
			self.image = pygame.transform.scale(self.image, (25, 25))
		else:
			factor = int(25*float(planr)/float(SCH/35))
			self.image = pygame.transform.scale(self.image, (factor, factor))
		self.speed = 0
		angle = math.atan2(deltay,deltax)
		self.crangle = angle
		self.x = planx + planr*np.cos(angle)
		self.y = plany + planr*np.sin(angle)
		newimage =rotate(self.image, angledegs(-1.0*(math.atan2(deltay,deltax) +np.pi/2.)))
		self.image = newimage
		self.rect = self.image.get_rect()
		self.rect.center= (self.x,self.y)
		self.state ='crashed'

	def land(self, planx, plany, planr, deltax, deltay):
		self.image, self.rect = load_png('Flag.png')
		self.image = pygame.transform.scale(self.image, (25, 25))
		self.speed = 0
		angle = math.atan2(deltay,deltax)
		self.crangle = angle
		self.x = planx + planr*np.cos(angle)
		self.y = plany + planr*np.sin(angle)
		newimage =rotate(self.image, angledegs(-1.0*(math.atan2(deltay,deltax) +np.pi/2.)))
		self.image = newimage
		self.rect = self.image.get_rect()
		self.rect.center= (self.x,self.y)
		self.state ='success'

	def crashdate(self, planx, plany, planr):
		self.x = planx + planr*np.cos(self.crangle)
		self.y = plany + planr*np.sin(self.crangle)
		self.rect.center = (self.x, self.y)
		pygame.event.pump()

	def landate(self, planx, plany, planr):
		self.x = planx + planr*np.cos(self.crangle)
		self.y = plany + planr*np.sin(self.crangle)
		self.rect.center = (self.x, self.y)
		pygame.event.pump()

	def update(self, SCH, SCW, rotflag=0):
		#self.direction = self.direction +self.dirchange

		if self.state=="start":
			self.dirpoint = self.dirpoint + self.dirchangestat
		elif self.state =="fired":
			self.dirpoint = self.direction

		if abs(self.dirchange)>1e-4 and self.state=="fired":
			if self.strt ==1:
				newimage = rotate(self.image0, angledegs(0.0), reinit=1)
				self.strt =0
			newimage = rotate(self.image0, angledegs(-1.0*self.dirchange))
			self.image = newimage
			self.dirchange = 0.

		if (abs(self.dirchangestat)>1e-10 and self.state == "start") or rotflag== 1:
			newimage = self.image0
			if self.strt ==1:
				newimage = rotate(self.image0, angledegs(0.0), reinit=1)
				self.strt =0
			else:
				newimage = rotate(newimage,angledegs(-1.0*(self.dirchangestat)))
			self.image = newimage
			self.dirchangestat = 0.

		#self.rect = RESET_ROTATED_RECT(self.rect,self.image)
		self.rect = self.image.get_rect()
		newpos = self.calcnewpos(self.direction, self.speed)
		if newpos[0] -self.rad>-40 and  newpos[1] - self.rad>=-40 and self.rad+newpos[0] < SCH+40 and newpos[1]+self.rad<SCW+40:
	                self.rect.center = newpos
		elif self.state == 'fired':
			self.state = 'off'
		pygame.event.pump()

	def calcnewpos(self,vector, speed):
		
		(dx,dy) = (speed*math.cos(vector),speed*math.sin(vector))
		(self.x, self.y) = (self.x +dx, self.y +dy)	
		
		return (self.x,self.y)

	def fire(self):
		self.state = "fired"
		self.speed, self.direction = add_vels(self.speed, self.sfactor*self.startvel,self.direction, self.dirpoint)
		#speedx = -self.speed*np.sin(self.direction) - self.startvel*np.sin(self.direction)
		#speedy = self.speed*np.cos(self.direction) + self.startvel*np.cos(self.direction)

	def powerup(self):
		if self.startvel < self.maxpower:
			self.startvel += 1

	def powerdown(self):
		if self.startvel >1:
			self.startvel -=1

	def rotleft(self):
		if self.dirpoint > self.dirmin and self.state=="start":
			self.dirchangestat = -np.pi/450.0 *self.rotfact
		
	def rotright(self):
		if self.dirpoint < self.dirmax and self.state=="start":
			self.dirchangestat = +np.pi/450.0 *self.rotfact
	
	def rotnone(self):
		self.dirchangestat =0.0

	def accelerate(self, forcex, forcey):
		speedx = float(self.speed)*math.cos(self.direction) + forcex
		speedy = float(self.speed)*math.sin(self.direction) + forcey
		self.speed = (float(math.sqrt(speedx**2+speedy**2)))
		self.dirchange = math.atan2(speedy, speedx) - self.direction
		self.direction = math.atan2(speedy, speedx)

	def mockfire(self,mspd, mdir):
		return add_vels(self.speed, self.sfactor*mspd, self.direction, mdir)
	
