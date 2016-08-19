'''
v 2.02
'''

expName = 'mindwandering_MDES' 
#collect participant info, create logfile
pptInfo = {
    'subject': '001', 
    'session': '001', 
    'conditions' : ['random', '0-back', '1-back'],
    } #a pop up window will show up to collect these information
"""
conditions:
random: randomly start with 1-back block or 0-back block
0-back: start with 0-back block
1-back: start with 1-back block 
"""
from psychopy import core

from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)

from MindWandering_TrialDisplay import*
from MindWandering_StimList import*

trials = getTrials(expInfo, datafn, switch=3) #3 switiches = four blocks = around 20 minutes 
instruction()
myClock = core.Clock()
expTrial(myClock, trials, datafn, expInfo, feedback=False)