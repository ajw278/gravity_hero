from __future__ import print_function  

import sys
import operator

def scoreupdate(path, newscore, initials):
	f = open(path, 'r')
	
	namelist = []
	scorelist =[]
	scd = {}
	l=0
	for line in f:
		if len(line) > 1:
			name, score = line.split()
			scd[l] =int(score), name
			l+=1

	scd[l] = int(newscore), initials
	
	sort_scores = sorted(scd.items(), key=operator.itemgetter(1), reverse =True)
	f.close()

	f = open(path, 'w')
	scoretext = ''
	for i in range(min(10,len(sort_scores))):
		print(sort_scores[i][1][1], sort_scores[i][1][0], file =f)
	f.close()	

	return 0

def getscores(path):
	f = open(path, 'r')
	
	namelist = []
	scorelist =[]
	scd = {}
	l=0
	for line in f:
		if len(line) > 1:
			name, score = line.split()
			scd[l] =int(score), name
			l+=1

	sort_scores = sorted(scd.items(), key=operator.itemgetter(1), reverse =True)
	
	scoretext = []
	for i in range(min(10,len(sort_scores))):
		scoretext .append(str(sort_scores[i][1][1]) + 2*(8 - len(sort_scores[i][1][1]))*"." + "......" +2*(4-len(str(sort_scores[i][1][0])))*"."+ str(sort_scores[i][1][0]))
	f.close()	

	return scoretext

def ishighscore(newscore, path):
	f = open(path, 'r')
	
	namelist = []
	scorelist =[]
	scd = {}
	minscore = 100000
	l=0
	for line in f:
		if len(line) > 1:
			name, score = line.split()
			score = int(score)
			if score < minscore:
				minscore=score
			scd[l] =score, name
			l+=1
	
	sort_scores = sorted(scd.items(), key=operator.itemgetter(1), reverse =True)
	f.close()

	if len(sort_scores)<10:
		return True
	elif newscore > minscore:
		return True
	else:
		return False



