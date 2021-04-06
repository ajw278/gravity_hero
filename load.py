#Python 2/3 compatibility
from __future__ import print_function  

try:
	#import future        # pip install future
	#import builtins      # pip install future
	#import past          # pip install future
	#import six      
	import sys
	import os
	from socket import *
	import pygame, sys
	from pygame.locals import *
	import numpy as np
except ImportError as err:
	print("Couldn't load module: %s" % (err))
	exit(2)

def load_png(name):
	""" Load image and return image object"""
	fullname = os.path.join('graphics', name)
	try:
		image = pygame.image.load(fullname)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	except pygame.error:
		print('Cannot load image:', fullname)
		sys.exit()
	return image, image.get_rect()


def angledegs(anglerad):
	return 360.*anglerad/(2.*np.pi)
