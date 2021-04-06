#!/usr/bin/env python

"""
GRAVITY HERO -- educational game designed for Cambridge Science Festival
A. Winter, Institute of Astronomy
03/02/2016


Things to do:
	- Time element (scores based on time??)
	- More levels
"""

#Python 2/3 compatibility
from __future__ import print_function  

try:
	import sys

	#import future        # pip install future
	#import builtins      # pip install future
	#import past          # pip install future
	#import six           # pip install six

	import random
	import math
	import os
	import getopt
	from socket import *
	import pygame

	from leveldata import *
	from objects import *
	from pygame.locals import *
	from motions import *
	from menu import *
	from score import *
except ImportError as err:
	print("Couldn't load module: %s" % (err))
	sys.exit(2)

#____________________Set constants of the game______________________________#
#MAXLEV is number of levels +1
MAXLEV = 4
MAXLIFE = 5
MAXPOWER = 10

pygame.init()

#Frames per second setting
FPS = 30

#_____________________________Game Initialisation________________________________#

fpsClock = pygame.time.Clock()

#Initialise window
infoObj = pygame.display.Info()
SCW = infoObj.current_w
SCH = infoObj.current_h
DISPLAYSURF = pygame.display.set_mode((SCH, SCH), FULLSCREEN, 32)
SCRECT = DISPLAYSURF.get_rect()
pygame.display.set_caption('Gravity Hero')
SCWA = SCW
SCW =SCH
FPS = FPS* float(SCH)/1200.
#_________________________________Formatting_______________________________#
#Colours
BLACK = (  0,   0,   0)
TRANSP = (0, 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
DARKERGREEN = (50, 200, 50)
BLUE = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
DARKRED = (100,   0,   0)

#Assign fonts
SMALLTEXT = SCH/30
MIDTEXT = SCH/25
LARGETEXT = SCH/15
MASSIVETEXT = SCH/8
titlefontObj = pygame.font.Font('./fonts/Capture_it.ttf', 75)
levelfontObj = pygame.font.Font('./fonts/Capture_it.ttf', 26)

mbg = pygame.image.load("./graphics/MainBG.jpg")
mbg = pygame.transform.scale(mbg, (SCW, SCH))
ebg = pygame.image.load("./graphics/EndGame.jpg")
ebg = pygame.transform.scale(ebg, (SCW, SCH))
cbg = pygame.image.load("./graphics/CompGame.jpg")
cbg = pygame.transform.scale(cbg, (SCW, SCH))

#____________________________Default Options________________________________#
GUIDE = True
INTRO = True

#________________________________Checks_____________________________________#
#Perform level checks
l=1
while l<MAXLEV:
	levdat(l, SCW, SCH, (0,0))
	l+=1


def main():
	GOPT = GUIDE
	ITERATIONS = 100
	IOPT = INTRO
	SCW=SCH	
	CENTER = (SCW/2, SCH/2)
	#Text setup  - render 2nd argument anti-aliasing
	titletextX = SCW/2
	titletextY = SCH
	titletextSurfaceObj, titletextRectObj = textobj('GRAVITY HERO ' , MASSIVETEXT, (titletextX, titletextY))
	titletextRectObj.center = (titletextX, titletextY) 
	opttextSurfObj, optextRect = textobj('OPTIONS' , MASSIVETEXT, (SCW/2, SCH/10))

	complevSurfaceObj = titlefontObj.render('LEVEL COMPLETE!  ', True, DARKERGREEN)
	complevtextRectObj = complevSurfaceObj.get_rect()
	complevtextX = SCW/2
	complevtextY = SCH
	complevtextRectObj.center = (complevtextX, complevtextY) 

	endgametextX = SCW/2
	endgametextY = SCH
	endgametextSurfaceObj, endgametextRectObj = textobj('YOU RAN OUT OF ROCKETS!', LARGETEXT, (endgametextX, endgametextY)) 

	wingametextSurfaceObj = titlefontObj.render('CONGRATULATIONS - YOU WIN!  ', True, DARKERGREEN)
	wingametextRectObj = wingametextSurfaceObj.get_rect()
	wingametextX = SCW/2
	wingametextY = SCH
	wingametextRectObj.center = (endgametextX, endgametextY) 

	# Create 3 diffrent menus.  One of them is only text, another one is only
	# images, and a third is -gasp- a mix of images and text buttons!  To
	# understand the input factors, see the menu file
	menu = cMenu(SCW/2-(LARGETEXT-10)*4, 2*SCH/7, 20, 5, 'vertical', 100, DISPLAYSURF,
	       [('Start Game', 1, None),
		('High Scores', 3, None),
		('Options', 4, None),
		('Help',  2, None),
		('Exit',       5, None)], TRANSP, LARGETEXT-5)

	# Center the menu on the draw_surface (the entire screen here)
	#menu.set_center(True, True)

	# Center the menu on the draw_surface (the entire screen here)
	menu.set_alignment('center', 'center')

	
	optmenu = cMenu(SCW/2-(LARGETEXT-5)*4, 2*SCH/7, 5, 15+LARGETEXT, 'vertical', 100, DISPLAYSURF,
	       [('Guidance System', 1, None),
		('Level Intro', 2, None),
		('Menu', 3, None),
		('Exit',       4, None)], TRANSP, LARGETEXT-5)

	# Center the menu on the draw_surface (the entire screen here)
	#optmenu.set_center(False, True)

	# Center the menu on the draw_surface (the entire screen here)
	optmenu.set_alignment('center', 'center')


	pausemenu = cMenu(SCW/2, SCH/2, 20, 5, 'vertical', 100, DISPLAYSURF,
	       [('Resume Game', 1, None),
		('Return to Main Menu',       2, None),
		('Exit', 3, None)], TRANSP, LARGETEXT)

	pausemenu.set_center(True, True)
	pausemenu.set_alignment('center', 'center')

	levelmenu  = cMenu(SCW/8, 4*SCH/5, SCW/8, 5, 'horizontal', 100, DISPLAYSURF,
	       [('Continue', 1, None),
		('End Game',       2, None),
		('Exit', 3, None)], TRANSP, MIDTEXT)

	#levelmenu.set_center(True,True)
	#levelmenu.set_alignment('center', 'bottom')

	HSmenu  = cMenu(SCW/8, 4*SCH/5, SCW/8, 5, 'horizontal', 100, DISPLAYSURF,
	       [('Main Menu', 1, None),
		('Play Again',       2, None),
		('Exit', 3, None)], TRANSP, MIDTEXT)

	#HSmenu.set_center(True,True)
	#HSmenu.set_alignment('bottom', 'bottom')


	# Create the menu state variables 
	state = 0
	prev_state = 1

	# rect_list is the list of pygame.Rect's that will tell pygame where to
	# update the screen (there is no point in updating the entire screen if only
	# a small portion of it changed!)
	rect_list = []

	# Ignore mouse motion (greatly DARKERGREENuces resources when not needed)
	pygame.event.set_blocked(pygame.MOUSEMOTION)

	#Starting level
	level = 1
	#Lives
	rocket = MAXLIFE
	#Final level +1
	levelMax = MAXLEV
	#Max power for rocket
	rocketpower = MAXPOWER
	flag=0
	newlevflag=0
	hsflag =0
	hsflag2=0
	GAMESTATE = 'menu'

	#Player score
	PScore =0	
	tbonus =0

	PUP = 0
	PDO =0
	PL =0
	PR =0

	#Run game loop
	while True:
		for e in pygame.event.get():
			if (e.type is KEYDOWN and e.key == K_RETURN and (e.mod&(KMOD_LALT|KMOD_RALT)) != 0):
				toggle_fullscreen()
	
		SCW = SCH	
		leveltext = levelfontObj.render("Level {0}, Rockets {1}".format(level, rocket), 1, DARKERGREEN)
		
		if GAMESTATE == 'finish':
			DISPLAYSURF.blit(mbg, (CENTER[0]-SCW/2,CENTER[1]-SCH/2))
			if ishighscore(PScore, './data/scores.dat') and hsflag == 0:
				hsflag =1
				newname = ask("Your name", mbg, PScore)
				scoreupdate('./data/scores.dat', PScore, newname)
				PScore = 0
			else:
				GAMESTATE = 'highscores'
				PScore = 0
				hsflag =0
		elif GAMESTATE == 'highscores':			
			if hsflag2 ==0:
				scoDARKERGREENat = getscores( './data/scores.dat')
				hsflag2 =1
				scoretext=[]
				scorerect = []
				hstext, hstextrect = textobj("HIGHSCORES", LARGETEXT, (SCW/ 2, 50))
				for i in range(len(scoDARKERGREENat)):
					newtext, newrect = textobj(str(i+1)+". "+ scoDARKERGREENat[i], MIDTEXT, (SCW/ 2, 50 + (LARGETEXT+10)+ (MIDTEXT+5)*i))
					scoretext.append(newtext)
					scorerect.append(newrect)

			if prev_state != state:
				DISPLAYSURF.blit(mbg, (CENTER[0]-SCW/2,CENTER[1]-SCH/2))
				DISPLAYSURF.blit(hstext, hstextrect)
				for i in range(len(scoDARKERGREENat)):
					DISPLAYSURF.blit(scoretext[i], scorerect[i])
				pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
				prev_state = state

			# Get the next event
			e = pygame.event.wait()

			if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
				if state == 0:
					rect_list, state = HSmenu.update(e, state)
				elif state == 1:
					GAMESTATE = 'menu'
					state = 0
					prev_state=1
					hsflag2 = 0
					newlevflag=0
				elif state ==2:
					hsflag2 =0
					prev_state=1
					GAMESTATE = 'play'
					#Starting level
					level = 1
					#Lives
					rocket = MAXLIFE
					complevtextX = SCW/2
					complevtextY = SCH
					endgametextX = SCW/2
					endgametextY = SCH
					wingametextX = SCW/2
					wingametextY = SCH
					newlevflag =2
					flag=0	
					state =0
				else:
					pygame.quit()
					sys.exit()

			# Quit if the user presses the exit button
			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# Update the screen
			pygame.display.update(rect_list)
		elif GAMESTATE == 'menu':
			if titletextY > SCH/10:
				DISPLAYSURF.blit(mbg, (CENTER[0]-SCW/2,CENTER[1]-SCH/2))
				#DISPLAYSURF.fill(BLACK)
				DISPLAYSURF.blit(titletextSurfaceObj, titletextRectObj)
				titletextY -= SCH/100
				titletextRectObj.top=titletextY
		 # Check if the state has changed, if it has, then post a user event to
		# the queue to force the menu to be shown at least once
			else:
				if prev_state != state:
					DISPLAYSURF.blit(mbg, (CENTER[0]-SCW/2,CENTER[1]-SCH/2))
					DISPLAYSURF.blit(titletextSurfaceObj, titletextRectObj)
					pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
					prev_state = state

				# Get the next event
				e = pygame.event.wait()

				# Update the menu, based on which "state" we are in - When using the menu
				# in a more complex program, definitely make the states global variables
				# so that you can refer to them by a name
				if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
					if state == 0:
						rect_list, state = menu.update(e, state)
					elif state == 1:
						#Starting level
						level = 1
						PScore =0
						#Lives
						rocket = MAXLIFE
						complevtextX = SCW/2
						complevtextY = SCH
						endgametextX = SCW/2
						endgametextY = SCH
						wingametextX = SCW/2
						wingametextY = SCH
						newlevflag =2
						flag=0	
						GAMESTATE = 'play'
						state = 0
					elif state == 2:
						GAMESTATE = 'help'
						level = 1
						#Lives
						rocket = MAXLIFE
						complevtextX = SCW/2
						complevtextY = SCH
						endgametextX = SCW/2
						endgametextY = SCH
						wingametextX = SCW/2
						wingametextY = SCH
						newlevflag =2
						flag=0	
						state =0
					elif state ==3:
						GAMESTATE = 'highscores'
						#Starting level
						level = 1
						#Lives
						rocket = MAXLIFE
						complevtextX = SCW/2
						complevtextY = SCH
						endgametextX = SCW/2
						endgametextY = SCH
						wingametextX = SCW/2
						wingametextY = SCH
						newlevflag =2
						flag=0	
						state =0
					elif state ==4:
						GAMESTATE = 'options'
						state=0
					else:
						terminate()

				# Quit if the user presses the exit button
				if e.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				# Update the screen
				pygame.display.update(rect_list)
		elif GAMESTATE == 'help':
			if prev_state != state:
				helptxt = helptext()
				DISPLAYSURF.blit(mbg, (CENTER[0]-SCW/2,CENTER[1]-SCH/2))
				hstext, hstextrect = textobj("HELP", LARGETEXT, (SCW/ 2, 50))
				DISPLAYSURF.blit(hstext, hstextrect)
				for i in range(len(helptxt)):
					newtext, newrect = textobj(helptxt[i], MIDTEXT, (SCW/ 2, 50 + (LARGETEXT+10)+ (MIDTEXT+5)*i))
					DISPLAYSURF.blit(newtext, newrect)
					
				pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
				prev_state = state

			# Get the next event
			e = pygame.event.wait()

			if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
				if state == 0:
					rect_list, state = HSmenu.update(e, state)
				elif state == 1:
					GAMESTATE = 'menu'
					state = 0
					prev_state=1
					hsflag2 = 0
					newlevflag=0
				elif state ==2:
					hsflag2 =0
					prev_state=1
					GAMESTATE = 'play'
					#Starting level
					level = 1
					#Lives
					rocket = MAXLIFE
					complevtextX = SCW/2
					complevtextY = SCH
					endgametextX = SCW/2
					endgametextY = SCH
					wingametextX = SCW/2
					wingametextY = SCH
					newlevflag =2
					flag=0	
					state =0
				else:
					pygame.quit()
					sys.exit()

			# Quit if the user presses the exit button
			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# Update the screen
			pygame.display.update(rect_list)
		elif GAMESTATE == 'options':
			if prev_state != state:
				DISPLAYSURF.blit(mbg, (CENTER[0]-SCW/2,CENTER[1]-SCH/2))
				DISPLAYSURF.blit(opttextSurfObj,optextRect)
				if GOPT:
					gopttext, goptrect = textobj('ON', LARGETEXT-5, (SCW/2, 2*SCH/7 + LARGETEXT))
				else:
					gopttext, goptrect = textobj('OFF', LARGETEXT-5, (SCW/2, 2*SCH/7 + LARGETEXT))
				if IOPT:
					iopttext, ioptrect = textobj('ON', LARGETEXT-5, (SCW/2, 2*SCH/7 + 13*LARGETEXT/4))
				else:
					iopttext, ioptrect = textobj('OFF', LARGETEXT-5, (SCW/2, 2*SCH/7 + 13*LARGETEXT/4))
				DISPLAYSURF.blit(gopttext, goptrect)
				DISPLAYSURF.blit(iopttext, ioptrect)
				pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
				prev_state = state

			# Get the next event
			e = pygame.event.wait()

			# Update the menu, based on which "state" we are in - When using the menu
			# in a more complex program, definitely make the states global variables
			# so that you can refer to them by a name
			if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
				if state == 0:
					rect_list, state = optmenu.update(e, state)
				elif state == 1:
					GOPT += 1
					GOPT = GOPT%2
					state = 0
				elif state == 2:
					IOPT += 1
					IOPT = IOPT%2
					state = 0
				elif state ==3:
					GAMESTATE = 'menu'
					state = 0
				else:
					terminate()

			# Quit if the user presses the exit button
			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# Update the screen
			pygame.display.update(rect_list)
		elif GAMESTATE == 'pausemenu':
			if prev_state != state:
				pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
				prev_state = state

			# Get the next event
			e = pygame.event.wait()

			# Update the menu, based on which "state" we are in - When using the menu
			# in a more complex program, definitely make the states global variables
			# so that you can refer to them by a name
			if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
				if state == 0:
					rect_list, state = pausemenu.update(e, state)
				elif state == 1:
					GAMESTATE = 'play'
					state = 0
					prev_state=1
				elif state ==2:
					GAMESTATE = 'menu'
					state =0
				else:
					pygame.quit()
					sys.exit()

			# Quit if the user presses the exit button
			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# Update the screen
			pygame.display.update(rect_list)
		elif GAMESTATE == 'play':
			CENTER = (SCW/2, SCH/2)
			SCW=SCH
			if flag ==0 and newlevflag ==0  and rocket>0 and level < levelMax and rocket>0:
					#Initialise level
					DISPLAYSURF.fill(BLACK)
					DISPLAYSURF.blit(LEVELDAT['BG'], (0, 0))
					DISPLAYSURF.blit(leveltext, (CENTER[0]-SCW/2+5, 10))
					homeplanet = 1
					
					pno=0		
					for planflag in LEVELDAT['FLAGS']:
						if planflag == 3:
							MCENT = LEVELDAT['MASS'][pno]
						pno+=1

					planets = ()

					#Gravity force (G)
					GFACT = LEVELDAT['GVAL']
					#initialise planets
					pno=0
					posplanet = []
					planetradii = []
					while pno < LEVELDAT['PLANETNo']:
						if LEVELDAT['FLAGS'][pno]!=3:
							posplanet.append(PlanetOrbit(MCENT, GFACT, LEVELDAT['RSTRTPOS'][pno][0], LEVELDAT['RSTRTPOS'][pno][1], SCW, SCH, CENTER, mtype = LEVELDAT['MTYPE'][pno], size = LEVELDAT['SFACTOR'], flag=0, xdisp = LEVELDAT['XDISP'], ydisp = LEVELDAT['YDISP'], perioddiff = LEVELDAT['DORBS']))
						else:
							posplanet.append(PlanetOrbit(MCENT, GFACT,LEVELDAT['RSTRTPOS'][pno][0], LEVELDAT['RSTRTPOS'][pno][1], SCW, SCH, CENTER, flag = 1,xdisp = LEVELDAT['XDISP'], ydisp = LEVELDAT['YDISP']))
						planets = planets+ (Planet(LEVELDAT['STRTPOS'][pno], LEVELDAT['NAMES'][pno], LEVELDAT['MASS'][pno], LEVELDAT['RADII'][pno], SCW, SCH, posplanet[pno][0],posplanet[pno][1], posplanet[pno][2]),)

						if LEVELDAT['FLAGS'][pno] == 1:
							refplanet = planets[pno]
						elif LEVELDAT['FLAGS'][pno] ==2:
							targetplanet = planets[pno]
						elif LEVELDAT['FLAGS'][pno]==3:
							centralplanet = planets[pno]
						planetradii.append(planets[pno].rad)
						pno+=1

					#Fix player to planet
					xcnst = np.cos(LEVELDAT['POSANGLE'])*(refplanet.rad)
					ycnst = np.sin(LEVELDAT['POSANGLE'])*(refplanet.rad)
					plyrstartx = refplanet.x +xcnst
					plyrstarty = refplanet.y + ycnst 

					# Initialise player
					global player
					player = Rocket(LEVELDAT['PLYRDIR'], LEVELDAT['PLYRSWIV'], LEVELDAT['MAXPOW'], rocket, LEVELDAT['PLYRRAD'], plyrstartx, plyrstarty, SCW, SCH, SCRECT, LEVELDAT['RSLOW'], LEVELDAT['ROTFACTOR'])

					planetmasses=[]
					for planet in planets:
						planetmasses.append(planet.mass)
					planetsprites = pygame.sprite.RenderPlain(planets)
					playersprite = pygame.sprite.RenderPlain(player)

					ITERATIONS = LEVELDAT['NITER']
					flag =1
			elif level == levelMax:
				DISPLAYSURF.blit(cbg, (0,0))
				DISPLAYSURF.blit(wingametextSurfaceObj, wingametextRectObj)
				wingametextY -= SCH/100
				wingametextRectObj.top=wingametextY
				if wingametextY < -100:
					GAMESTATE='finish'
			elif newlevflag == 1:
				DISPLAYSURF.blit(mbg, (0,0))
				DISPLAYSURF.blit(complevSurfaceObj, complevtextRectObj)
				complevtextY -= SCH/100
				complevtextRectObj.top=complevtextY
				if complevtextY < -100:
					newlevflag = 2
			elif level < levelMax:
				if newlevflag ==2:
					rocket = MAXLIFE
					LEVELDAT = levdat(level, SCW, SCH, CENTER)
					if IOPT:
						levelheadSurfObj, levelheadRectObj =  textobj("LEVEL {0}".format(level), LARGETEXT, (SCW/2,SCH/9))
						levtextSurfaceObj = []
						levtextRectObj = []
						for i in range(len(LEVELDAT['TEXT'])):
							levtextSurfaceObj_tmp, levtextRectObj_tmp = textobj(LEVELDAT['TEXT'][i], SMALLTEXT, (SCW/2,SCH/5+i*(SMALLTEXT+5)))
							levtextSurfaceObj.append(levtextSurfaceObj_tmp)
							levtextRectObj.append(levtextRectObj_tmp)
						if prev_state != state:
							DISPLAYSURF.blit(mbg, (0,0))
							DISPLAYSURF.blit(levelheadSurfObj, levelheadRectObj)
							for i in range(len(LEVELDAT['TEXT'])):
								DISPLAYSURF.blit(levtextSurfaceObj[i], levtextRectObj[i])
							pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
							prev_state = state

						# Get the next event
						e = pygame.event.wait()

						# Update the menu, based on which "state" we are in - When using the menu
						# in a more complex program, definitely make the states global variables
						# so that you can refer to them by a name
						if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
							if state == 0:
								rect_list, state = levelmenu.update(e, state)
							elif state == 1:
								GAMESTATE = 'play'
								state = 0
								prev_state=1
								newlevflag=0
							elif state ==2:
								GAMESTATE = 'menu'
								state =0
							else:
								pygame.quit()
								sys.exit()

						# Quit if the user presses the exit button
						if e.type == pygame.QUIT:
							pygame.quit()
							sys.exit()

						# Update the screen
						pygame.display.update(rect_list)
					else:
						newlevflag =0
				elif player.lives == 0:
					DISPLAYSURF.blit(ebg, (0,0))
					DISPLAYSURF.blit(endgametextSurfaceObj, endgametextRectObj)
					endgametextY -= SCH/100
					endgametextRectObj.top=endgametextY
					if endgametextY < -80:
					#Need to change this to a menu
						GAMESTATE='finish'
				else:
					if player.state =="start":
						flighttime = 0
						indices = []
						for planet in planets:
							indices.append(planet.posind)
						if GOPT:
							mockspeed, mockdir = add_vels(refplanet.speed, player.startvel,refplanet.vector, player.dirpoint)	
							tspd, tdir = player.mockfire(mockspeed, mockdir)
							vectors = orbitintegrator((player.x, player.y),tspd, tdir, planetmasses, planetradii, posplanet, indices, GFACT, SCW, SCH, LEVELDAT['MODGRAV'], iterations=ITERATIONS)
							if len(vectors) > 5:
								guide = pygame.draw.lines(DISPLAYSURF, GREEN, False, vectors,1)
						if LEVELDAT['SROT']==0:
							player.x = refplanet.x + xcnst
							player.y = refplanet.y + ycnst
						elif not LEVELDAT['STATIC']:
							player.x = refplanet.x + np.cos(refplanet.vector+LEVELDAT['POSANGLE']-np.pi/2.)*(refplanet.rad+player.rad)*2.
							player.y = refplanet.y + np.sin(refplanet.vector+LEVELDAT['POSANGLE']-np.pi/2.)*(refplanet.rad+player.rad)*2.
							if refplanet.posind >0 and refplanet.posind < len(refplanet.dirs):
								player.dirchangestat = refplanet.dirs[refplanet.posind]-refplanet.dirs[refplanet.posind-1] 
							elif refplanet.posind == 0:
								player.dirchangestat = refplanet.dirs[refplanet.posind]-refplanet.dirs[len(refplanet.dirs)-1] 
							elif refplanet.posind == len(refplanet.dirs):
								player.dirchangestat = refplanet.dirs[0]-refplanet.dirs[refplanet.posind-1] 
							player.dirmax = refplanet.vector+LEVELDAT['PLYRDIR']-np.pi/2. + LEVELDAT['PLYRSWIV']
							player.dirmin = refplanet.vector+LEVELDAT['PLYRDIR']-np.pi/2. -  LEVELDAT['PLYRSWIV']
							if player.dirmin > np.pi:
								player.dirmin = 2.*np.pi-player.dirmin
							if player.dirmax >np.pi:
								player.dirmax = 2.*np.pi - player.dirmax
							player.update(SCH,SCW)
						if GOPT:
							if len(vectors)>5:
								pygame.display.update(guide)
						for planet in planets:
							if planet.state == 'off':
								print("Reinitialisation from start.")
								for planet in planets:
									planet.reinit()
								player.reinit()
								player.x = plyrstartx
								player.y = plyrstarty
								break
						pressed = pygame.key.get_pressed()
						if pressed[pygame.K_SPACE]:
							player.startvel, player.dirpoint = add_vels(refplanet.speed, player.startvel,refplanet.vector, player.dirpoint)
							player.fire()
						elif pressed[pygame.K_UP] and PUP==0:
							player.powerup()
							PUP=1
							PDO =0
							PL =0
							PR =0
						elif pressed[pygame.K_DOWN] and PDO ==0:
							player.powerdown()
							PUP=0
							PDO =1
							PL =0
							PR =0
						elif pressed[pygame.K_LEFT] and PL ==0:
							player.rotleft()
							PUP=0
							PDO =0
							PL =1
							PR =0
						elif pressed[pygame.K_RIGHT] and PR ==0:
							player.rotright()
							PUP=0
							PDO =0
							PL =0
							PR =1
						elif pressed[pygame.K_ESCAPE]:
							PUP=0
							PDO =0
							PL =0
							PR =0
							GAMESTATE = 'pausemenu'
						elif pressed[pygame.K_c] and  pressed[pygame.K_h] and pressed[pygame.K_e] and  pressed[pygame.K_a] and pressed[pygame.K_t]:
							GOPT =1
							ITERATIONS=2000
							player.rotnone()
							PUP=0
							PDO =0
							PL =0
							PR =0
							PR =0
						elif pressed[pygame.K_r]:
							GOPT =1
							ITERATIONS = LEVELDAT['NITER']
							player.rotnone()
							PUP=0
							PDO =0
							PL =0
							PR =0
							PR =0
						elif pressed[pygame.K_n]:
							GOPT =0
							ITERATIONS = LEVELDAT['NITER']
							player.rotnone()
							PUP=0
							PDO =0
							PL =0
							PR =0
							PR =0
						else:
							player.rotnone()
							PUP=0
							PDO =0
							PL =0
							PR =0
					#Player launches - calculate forces from planets
					elif player.state == "fired":
						flighttime+=1
						tbonus = int(500*float(LEVELDAT['TLIM']-flighttime)/float(LEVELDAT['TLIM']))
						if GOPT:
							vectors=[]
						if player.timer ==1:
							deltax = []
							deltay = []
							for planet in planets:
								deltax.append(player.x - planet.x)
								deltay.append(player.y - planet.y)

							forcex, forcey = force(planetmasses, deltax, deltay, GFACT, SCW, SCH, modified = LEVELDAT['MODGRAV'])
							player.accelerate(forcex,forcey)

							if not CollisionDetect(player, refplanet):
								homeplanet=0

							#Detect if planet is colliding
							pno=0
							for planet in planets:
								if planet != targetplanet and CollisionDetect(player, planet):
								#Add explosion or something here
									player.lives-=1
									homeplanet=1
									crashplan = planet
									player.crash(crashplan.x, crashplan.y, crashplan.rad, deltax[pno], deltay[pno], SCH)
									tbonus =0
								elif planet == targetplanet and CollisionDetect(player, planet):
									crashplan = planet
									player.land(crashplan.x, crashplan.y, crashplan.rad, deltax[pno], deltay[pno])
									PScore += tbonus
									tbonus =0
								pno +=1

							if not targetplanet.isin(SCW, SCH) or flighttime>LEVELDAT['TLIM']:
								player.state = 'off'
					elif player.state =='crashed':
						if player.timer == 0:
							for planet in planets:
								planet.reinit()
							player.reinit()
							player.x = plyrstartx
							player.y = plyrstarty
							rocket = player.lives
						else:
							player.timer += 1
							if player.timer ==60:
								player.timer = 0
							
							player.crashdate(crashplan.x, crashplan.y, crashplan.rad)
							playersprite.draw(DISPLAYSURF)
					elif player.state =='success':
						if player.timer == 0:
							PScore += 100 + player.lives *50
							level +=1
							newlevflag=1
							flag=0
						else:
							player.timer += 1
							if player.timer ==60:
								player.timer = 0
							
							player.landate(crashplan.x, crashplan.y, crashplan.rad)
							playersprite.draw(DISPLAYSURF)

					elif player.state =='off':
						for planet in planets:
							planet.reinit()
						player.reinit()
						player.x = plyrstartx
						player.y = plyrstarty
						player.lives -=1
						rocket = player.lives
					
					if rocket != 0:
						DISPLAYSURF.fill(BLACK)
						DISPLAYSURF.blit(LEVELDAT['BG'], (CENTER[0]-SCW/2,0))
						DISPLAYSURF.blit(leveltext, (5+CENTER[0]-SCW/2, 10))
						if player.state =='start' and GOPT:
							if len(vectors)>10:
								pygame.draw.lines(DISPLAYSURF, GREEN, False, vectors,2)
								#pygame.display.update(guide)

						if player.state != 'crashed' and player.state != 'success':
							playersprite.update(SCW, SCH)
						
						if not player.state == 'start':
							planetsprites.update(SCW, SCH, player.state)
						elif player.state == 'start' and not LEVELDAT['STATIC']:
							planetsprites.update(SCW, SCH, player.state)

						spritetext = levelfontObj.render("Power:  {0},  Direction: {1}".format(player.startvel, player.dirpoint), 1, DARKERGREEN)
						scoretext = levelfontObj.render("Score:  {0}".format(PScore), 1, DARKERGREEN)
						tbonustext = levelfontObj.render("Time Bonus:  {0}".format(tbonus), 1, DARKERGREEN)
						DISPLAYSURF.blit(spritetext, (CENTER[0]-SCW/2+5, 45))
						DISPLAYSURF.blit(scoretext, (CENTER[0]+SCW/2-SMALLTEXT*8,10))
						DISPLAYSURF.blit(tbonustext, (CENTER[0]+SCW/2-SMALLTEXT*8,45))

						playersprite.draw(DISPLAYSURF)
						planetsprites.draw(DISPLAYSURF)

					pygame.display.flip()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
		fpsClock.tick(FPS)



#______________________________Screen Functions_____________________________#

def textobj(message, size, position):
	fontObj = pygame.font.Font('./fonts/Capture_it.ttf',int( size))
	textObj = fontObj.render(message, 1, DARKERGREEN)
	textRect = textObj.get_rect()
	textRect.midtop = position
	return textObj, textRect

def ask(question, bg, PScore):
	"ask(question) -> answer"
	current_string = ""
	left = (SCW / 2) +156
	top = (SCH / 2) + 100

	scoretext = titlefontObj.render("High Score:  {0}".format(PScore), 1, DARKERGREEN)
	scorerect = scoretext.get_rect()
	scorerect.midtop = (SCW/ 2, 150)
	foundname =False
	while foundname ==False:
		DISPLAYSURF.blit(bg, (0,0))
		DISPLAYSURF.blit(scoretext , scorerect)
		#swear = profanityFilter(current_string)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				inkey = event.key
				if inkey == K_BACKSPACE:
					if len(current_string) >0:
						current_string = current_string[:-1]
				elif (inkey == K_RETURN or inkey == K_KP_ENTER) and len(current_string)>0: # and swear[1]==False:
					foundname =True
				elif inkey == pygame.K_ESCAPE:
					terminate()
				elif inkey in range(97,123):
					if len(current_string)<10:
						current_string += chr(inkey)
						current_string = current_string.strip()	
		#swear = profanityFilter(current_string)	
		message = question + ": " + current_string #swear[0]
		#if swear[1]==True:
		#	current_string=""
		messtext= titlefontObj.render(message, True, DARKERGREEN)
		messtextrect = messtext.get_rect()
		messtextrect.midtop = (SCW/ 2, SCH/2 + 150)
		DISPLAYSURF.blit(messtext, messtextrect)
		pygame.display.update()

	return current_string # this is the answer    


def terminate():
	pygame.quit()
	sys.exit()

#_________________________END OF SCREEN FUNCTIONS__________________________#


if __name__ == '__main__':
    main()
