'''
v 2.02
'''

expName = 'mindwandering_practice' 
#collect participant info, create logfile
pptInfo = {
    'subject': '001', 
    'session': '999', 
    } #a pop up window will show up to collect these information

from psychopy import core

from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)

from MindWandering_TrialDisplay import*
from MindWandering_StimList import*

trials = np.load('Stimuli\\practice_trials.npy')
instruction()
myClock = core.Clock()
expTrial(myClock, trials, datafn, expInfo, feedback=True)

