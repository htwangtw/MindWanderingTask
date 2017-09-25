#!/usr/bin/env python

'''
v0.2
changed stimuli name

This is not the most elegant script of mine and the naming is a bit messy.
Please let me know if you have any question.
'''

'''
set parameters
'''
extend_resp_time = 0 # add 500 ms in all go trials if the experiment has special need. If you want the normal version, set to 0
n_endloop = 22 # the number of questions you ask at the end of the task

'''
generating trial list
'''
from numpy.random import randint, shuffle
import numpy as np
import glob
import pandas as pd
import csv
import os

def BlockList (nSwitch, nTT, nProbe, nMWQ, time):

	'''
	Best setting:
	9 * n minutes long block with one switch
	number of switch = 1 + 2*(n-1)
	number of go trials = 9 * n
	number of MWQ probes = 6 *n
	number of MWQ = 13 
	number of task (go trials + probes) = 15 * n
	'''

	#set: length of the expeirement
	nNT = round((time * 60 - 66.5 * nProbe - 3.8 * nTT - 2 * nSwitch)/2.5) - 1
	nCond = nSwitch + 1
	nTP = nTT + nProbe 

	#set trial labels
	'''
	F: fixation cross
	NT: non-task trial
	TT: task trial (go trials)
	MWQ: mind-wandering question
	QF: fixation cross during the experience sampling period. It is always 500 ms.
	END: the set of mind-wandering questions set at the end. 
	'''

	NT = ['F', 'NT']
	TT = ['F', 'TT']
	Probe = ['F'] + ['MWQ', 'QF']*(nMWQ-1) + ['MWQ']
	End = ['F'] + ['END', 'QF']*(n_endloop-1) + ['END']
    
	ntrials = 2 * (nNT + nTT + nSwitch) + len(Probe) * nProbe    #set: the number of total trials

	# create a random list of go trial and mind-wandering question 
	targORprobe = [TT] * nTT + [Probe] * nProbe
	shuffle(targORprobe)

	# set the number of no-go trials before showing the END questions 
	# and exlude in the count of trials while generating the list
	Nend = randint(2,5)  
	tempN_NT = nNT - Nend

	trials = []
	cur_ntrials = 0 

	i_switch = []
	for i in range(1, nCond):
		switch_at = round(nTP/nCond*i - 1, 0)
		i_switch.append(switch_at)

	while cur_ntrials != ntrials: #the loop will keep going until a list of correct number of trials created
		for i in range(0, len(targORprobe)):
			init_nNT = randint(2,5)
			if tempN_NT >= init_nNT:
				temp = NT * init_nNT
				trials += temp
				tempN_NT -= init_nNT
			else:
				temp = NT* init_nNT
				trials += temp

			trials += targORprobe[i]

			if i in i_switch: #switch condition
				num_pre = randint(2,4)  
				#number of non task (1 or 2)before switching to the next block
				trials += NT * num_pre + ['F'] + ['Switch']
				tempN_NT -= num_pre
				# print trials[-10:]
			# print i+1, targORprobe[i], nNT, init_nNT

			if i == len(targORprobe)-1:
				trials += NT * Nend

		#debug
		cur_ntrials = len(trials) 
		if cur_ntrials != ntrials:
			tempN_NT = nNT - Nend
			trials = []
			print 'abandon this list as it doesnt meet the criteria %i'%(ntrials), cur_ntrials
		else: 
			print 'save this list', cur_ntrials
			trials +=End

	blocklst = np.array(trials)

	explen = time * 60 + 5 * 22 #length of the experiment (estimation)
	tempDis = np.zeros(len(blocklst))
	blocklen = np.sum(tempDis)
	while blocklen != explen:
		for i in range(0, len(blocklst)):
			if blocklst[i] == 'F':
				cur_len = np.arange(1.3,1.75,0.05)[randint(0,9)]   #length of fixation cross display
			elif blocklst[i] =='NT':
				cur_len = np.arange(0.80,1.25,0.05)[randint(0,9)]  #time length of the trial
			elif blocklst[i] =='TT':
				cur_len = np.arange(2.1,2.55,0.05)[randint(0,9)] + extend_resp_time #the time length of target display
			elif blocklst[i] =='MWQ' or blocklst[i] =='END' :
			 	cur_len = 4.5  #the time length of target display
			elif blocklst[i] =='QF':
			 	cur_len = .5  #the time length of target display
			else: #switch
			 	cur_len = np.arange(1.8,3.25,0.05)[randint(0,9)]
			tempDis[i] = cur_len
		blocklen = round(np.sum(tempDis), 0)
		if blocklen != explen:
			tempDis = np.zeros(len(blocklst))
		else:
			print 'save list', blocklen
	times = tempDis.reshape(blocklst.shape[0]/2,2)
	keys = blocklst.reshape(blocklst.shape[0]/2,2)

	return keys, times

def setStim (STIMS_DIR, keys, times, selection):
	'''
	STIMS_DIR: the directory of the stimuli
	keys: the trial type keys you got from function BlockList
	selection: manually set the starting condition or not, 
		it takes three kinds of input-
			None	you want to randomly select to start with 0 back or 1 back
			[0,1]	you want to start with 0-back
			[1,0]	you want to start with 1-back

	'''
	def setcond(selection):
		if selection== '0-back':
		    cond = [0,1]
		elif selection== '1-back':
		    cond = [1,0]
		else:
		    cond = None
		return cond

	#get file names
	NT_0B_STIMS_DIR = STIMS_DIR  + '0B_N*.png' 
	TT_0B_STIMS_DIR = STIMS_DIR  + '0B_G*.png'

	NT_1B_STIMS_DIR = STIMS_DIR  + 'nB_N*.png'
	TT_1B_STIMS_DIR = STIMS_DIR  + 'nB_G*.png'

	NT0Bpicfn = glob.glob(NT_0B_STIMS_DIR)
	NT0B_names = [pic.split(os.sep)[-2] + os.sep + pic.split(os.sep)[-1]  for pic in NT0Bpicfn]
	TT0Bpicfn = glob.glob(TT_0B_STIMS_DIR)
	TT0B_names = [pic.split(os.sep)[-2] + os.sep + pic.split(os.sep)[-1]  for pic in TT0Bpicfn]
	NT1Bpicfn = glob.glob(NT_1B_STIMS_DIR)
	NT1B_names = [pic.split(os.sep)[-2] + os.sep + pic.split(os.sep)[-1]  for pic in NT1Bpicfn]
	TT1Bpicfn = glob.glob(TT_1B_STIMS_DIR)
	TT1B_names = [pic.split(os.sep)[-2] + os.sep + pic.split(os.sep)[-1]  for pic in TT1Bpicfn]

	#get the index of the switch screen
	switch_ind = np.where(keys == 'Switch')[0] + 1   
	# print switch_ind, keys.shape[0]
	conlst = np.zeros(keys.shape[0],dtype=int)

	# assign conditions
	if setcond(selection) == None:
		cond = [0,1]
		shuffle(cond)
	else:
		cond = setcond(selection)

	for n in range((len(switch_ind)+1)/2):
		if n ==0: #first easy-hard switch
			conlst[0:switch_ind[0]], conlst[switch_ind[0]:] = cond[0], cond[1]
		elif n*2 == (len(switch_ind)+1)/2: #last easy-hard switch
			conlst[switch_ind[n*2-1]:switch_ind[n*2]], conlst[switch_ind[n*2]:] = cond[0], cond[1]
		else: #any switch in between
			conlst[switch_ind[n*2-1]:switch_ind[n*2]], conlst[switch_ind[n*2]:switch_ind[n*2+1]] = cond[0], cond[1]


	pic = []
	mwType = []
	ans = []
	MWQ_ind = np.arange(0,12)
	MWQ_start = 0

	END_ind = np.arange(0,22)
	END_start = 0
	shuffle(END_ind)

	MWQ_DIR = STIMS_DIR + 'probe_loop.csv'
	Focus =   pd.read_csv(MWQ_DIR).values[0]
	MWQlst =  pd.read_csv(MWQ_DIR).values[1:]

	END_DIR = STIMS_DIR + 'end_loop.csv'
	ENDlst =  pd.read_csv(END_DIR).values


	for i in range(0, len(keys)):
		cur_stim = []
		cur_ans = []
		cur_target = []

		if (keys[i,1] == 'NT') and (conlst[i] == 0):
			pick = randint(0,len(NT0B_names))
			cur_stim = NT0B_names[pick]
			
			pic.append(cur_stim)
			mwType.append('NT')
			ans.append(None)

		elif (keys[i,1] == 'NT') and (conlst[i] == 1):
			pick = randint(0,len(NT1B_names))
			cur_stim = NT1B_names[pick]
			
			pic.append(cur_stim)
			mwType.append('NT')
			ans.append(None)

			pre_NT = cur_stim

		elif (keys[i,1] == 'TT') and (conlst[i] == 0):
			pick = randint(0,len(TT0B_names))
			cur_stim = TT0B_names[pick]
			temp_ans = TT0B_names[pick].split('_')[2]
			if temp_ans =='L':
				cur_ans = 'left'
			elif temp_ans =='R':
				cur_ans = 'right'
			else:
				cur_ans = 'error'
				print 'error when stripping the correct trial answer'
			
			pic.append(cur_stim)
			mwType.append('TT')
			ans.append(cur_ans)

		elif (keys[i,1] == 'TT') and (conlst[i] == 1):

			pre_stim = pre_NT.split('.')[0].split('_')[2:4]
			pick = pre_stim[randint(0,2)]

			if pick == pre_stim[0]:
				cur_ans = 'left'
			elif pick == pre_stim[1]:
				cur_ans = 'right'
			else:
				pass
			
			find_stim = [TT1B_names[0].find(pick.upper()), 
			TT1B_names[1].find(pick.upper()), 
			TT1B_names[2].find(pick.upper())]
			
			f = [i for i,x in enumerate(find_stim)  if x >0]
			cur_stim = TT1B_names[f[0]]
			
			pic.append(cur_stim)
			mwType.append('TT')
			ans.append(cur_ans)

		elif keys[i,1] == 'Switch':
			pic.append('Switch')
			mwType.append('NT')
			ans.append(None)

		elif keys[i,1] == 'MWQ':
			
			if times[i,0] != 0.5:
				MWQ_start = i+1
				pic.append(str(Focus[0]))
				mwType.append(str(Focus[1]))
				ans.append(str(Focus[2]))
				MWQ_ind = np.arange(0,12)
				shuffle(MWQ_ind)
			else:
				temp = i-MWQ_start
				cur_MWQ_ind = MWQ_ind[temp]

				pic.append(str(MWQlst[cur_MWQ_ind,0]))
				mwType.append(str(MWQlst[cur_MWQ_ind,1]))
				ans.append(str(MWQlst[cur_MWQ_ind,2]))
		elif keys[i,1] == 'END':
			if times[i,0] != 0.5:
				END_start = i
			temp = i - END_start 
			cur_END_ind = END_ind[temp]
			pic.append(str(ENDlst[cur_END_ind,0]))
			mwType.append(str(ENDlst[cur_END_ind,1]))
			ans.append(str(ENDlst[cur_END_ind,2]))
                
	return pic, mwType, ans, conlst


def getStim (STIMS_DIR, selection, nSwitch, nTT, nProbe, nMWQ, time, filename):
	keys, times = BlockList(nSwitch, nTT, nProbe, nMWQ, time)
	stim, mwT, ans, cond = setStim(STIMS_DIR, keys, times, selection)
	stim = np.array(stim)
	mwT = np.array(mwT)
	ans = np.array(ans)
	triallst = np.zeros(keys.shape[0], 
	dtype=[('TrialIndex', int), ('nBack', int), ('stimType', 'S6'), ('fixT', float), ('stimT', float), 
		('stimPic', 'S82'), ('mwType', 'S10'), ('Ans', 'S63')])
	triallst['TrialIndex'] = range(1,keys.shape[0]+1)
	triallst['nBack'] = cond
	triallst['stimType'] = keys[:,1]
	triallst['fixT'] = times[:,0]
	triallst['stimT'] = times[:,1]
	triallst['stimPic'] = stim
	triallst['mwType'] = mwT
	triallst['Ans'] = ans
	#debug
	with open(filename, 'wb') as f:
		f.write(b'TrialIndex,nBack,stimType,fixT,stimT,stimPic,mwType,Ans\n')
		#f.write(bytes("SP,"+lists+"\n","UTF-8"))
		#Used this line for a variable list of numbers
		np.savetxt(f, triallst,delimiter=',', fmt='%i,%i,%s,%10.3f,%10.3f,%s,%s,%s')
		f.close()
	return triallst
	
def getTrials(expInfo, datafn, switch=3):
    trials = getStim(STIMS_DIR='Stimuli' + os.sep, selection=expInfo['conditions'], 
        nSwitch=switch, nTT=9*(switch+1)/2,nProbe=6*(switch+1)/2, nMWQ=13, time=9.5*(switch+1)/2, 
        filename=datafn + '_trials.csv')
    return trials

def getPractice(expInfo, datafn, switch=1):
    trials = getStim(STIMS_DIR='Stimuli' + os.sep, selection=expInfo['conditions'], 
        nSwitch=switch, nTT=10*(switch+1)/2, nProbe=1 , nMWQ=13, time=3.5, 
        filename=datafn +'_practice.csv')
    np.save(datafn + 'practice_trials',trials[:-14,])
    return trials
