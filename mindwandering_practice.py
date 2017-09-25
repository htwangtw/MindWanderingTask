#!/usr/bin/env python

'''
v 2.02
'''

expName = 'mindwandering_practice' 
#collect participant info, create logfile
pptInfo = {
    'subject': '001', 
    'session': ['999'], 
    'conditions':['random']
    } #a pop up window will show up to collect these information

from psychopy import core

from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)

from MindWandering_TrialDisplay import*
from MindWandering_StimList import*

trials = getPractice(expInfo, datafn, switch=1)
instruction()
myClock = core.Clock()
expTrial(myClock, trials, datafn, expInfo, feedback=True, MW_description=False)

