#!/usr/bin/env python

from psychopy import visual, core, event
from numpy.random import randint, shuffle
import numpy as np
from baseDef import*
win = set_window(fullscr=True, gui=False, color=0)
sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana'] #use the first font found on this list
fixation = visual.ImageStim(win, name='fixation', image = None, size = (800, 600))#set pix pos
postResp = visual.Circle(win, name='postRespT', lineColor='black', fillColor='black', radius=2, edges=32, )
im = visual.ImageStim(win, name='stimPic', image = None, size = (800, 600), )
question = visual.TextStim(win, name='QuestionMWQ',
   text='default text', font= sans,
   pos=[0, 100], height=60, wrapWidth=1300,
   color='black')
#not using the rating scale module
descr = visual.TextStim(win, name='Descriptions',
   text='default text', font= sans,
   pos=[0, -60], height=50, wrapWidth=1300,
   color='black')
scale = visual.TextStim(win, name='RatingScale',
   text='1     2     3     4', font= sans,
   pos=[0, -120], height=45, wrapWidth=1300,
   color='black', )
msgTxt = visual.TextStim(win,text='default text', font= sans, name='mesage',
    height=34, wrapWidth=1100,
    color='black', 
    )
instrTxt = visual.TextStim(win,text='default text', font= sans, name='instruction',
    pos=[-50,0], height=30, wrapWidth=1100,
    color='black',
    ) #object to display instructions
fb = visual.TextStim(win,text='default text', font= sans, name='feedback',
    height=50, wrapWidth=1100,
    color='black', 
    )


import codecs

def feedback_screen(keyResp, CORR):
    feedbacks_txt = codecs.open('Instructions'+ os.sep+ 'feedbacks.txt', 'r', encoding='utf-8').read().split('\n')
    fb_msg = feedbacks_txt[0]
    if keyResp:
        if CORR == 0:
            fb_msg = feedbacks_txt[1]
        elif CORR == 1:
            fb_msg = feedbacks_txt[2]
    else:
        fb_msg = feedbacks_txt[0]
    fb.setText(fb_msg)
    fb.draw()
    win.flip()
    core.wait(1)
    
def show_questions():
    question.draw()
    descr.draw()
    scale.draw()
    win.flip()

def show_stim():
    im.draw()
    win.flip()

def reset_output():
    keyResp = None
    thisRT = np.nan
    respRT = np.nan
    CORR = np.nan
    return keyResp, thisRT, respRT, CORR

def getResp(stimType, startT, stimT, myClock, thisTrial):
    keyResp, thisRT, respRT, CORR = reset_output()
    
    if stimType == 'MWQ' or stimType == 'END':
    	while keyResp==None:
            show_questions()
            keyResp, thisRT = get_keyboard(myClock,win, respkeylist=['1', '2', '3', '4']) #set response keys, any numbers you want
            if not np.isnan(thisRT):
                respRT = thisRT - startT
            else:
                pass

    elif stimType=='TT' or stimType=='NT':
    	while keyResp==None and (myClock.getTime() - startT <=stimT):
            show_stim()
            keyResp, thisRT = get_keyboard(myClock,win, respkeylist=['left', 'right']) 
            if not np.isnan(thisRT):
                respRT = thisRT - startT
            else:
                pass
        if thisTrial['Ans'] == keyResp:
            CORR = 1
        elif keyResp == None and thisTrial['Ans'] == 'None':
        	CORR = 1
        else:
            CORR = 0
    return keyResp, respRT, CORR

def saveResp(f, i, thisTrial, expInfo, keyResp, respRT, CORR, startT, fixStart):
    write_datalog(f, data='%i,%i,%i,%s,%f,%f,%f,%f,%s,%s,%s,%s,%f,%f,%s,%s\n'
        %(i, thisTrial['TrialIndex'], thisTrial['nBack'], thisTrial['stimType'], 
            fixStart, thisTrial['fixT'], startT, thisTrial['stimT'], 
            thisTrial['stimPic'], thisTrial['mwType'], thisTrial['Ans'],
            keyResp,CORR,respRT,expInfo['subject'],expInfo['session']))
    event.clearEvents()


def instruction():
    Instruction = codecs.open('Instructions'+ os.sep+ 'exp_instr.txt', 'r', encoding='utf-8').read().split('#\n')
    Ready = codecs.open('Instructions'+ os.sep+ 'wait_trigger.txt', 'r', encoding='utf-8').read()
    #instructions screen 
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        if i==0:
        	core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])
        else:
        	event.waitKeys(keyList=['return'])

        if event.getKeys(keyList = ['escape']):
            quitEXP(True)

    instrTxt.setText(Ready)
    instrTxt.draw()
    win.flip()
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    #need to update a scanner trigger version
    core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])
    

def fixation_screen(myClock, thisTrial):
    if thisTrial['stimType'] == 'MWQ' or thisTrial['stimType'] == 'END':
        if thisTrial['mwType']=='Focus':
            fixation = visual.ImageStim(win, name='fixation', image = None, size = (800, 600))#set pix pos
            if thisTrial['nBack'] == 0:
                fixation.setImage('Stimuli'+ os.sep+ '0B_fix.png')
            elif thisTrial['nBack'] ==1:
                fixation.setImage('Stimuli'+ os.sep+ 'nB_fix.png')
            fixation.draw()
        else:
            fixation = visual.TextStim(win, name='fixation', text='+', color='black', height=62,)#set pix pos
            fixation.draw()
    else:
        fixation = visual.ImageStim(win, name='fixation', image = None, size = (800, 600))#set pix pos
        if thisTrial['nBack'] == 0:
            fixation.setImage('Stimuli'+ os.sep+ '0B_fix.png')
        elif thisTrial['nBack'] ==1:
            fixation.setImage('Stimuli'+ os.sep+ 'nB_fix.png')
        fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='fixation cross on screen') #new log haoting
    win.flip()
    fixStart = myClock.getTime() #fixation cross onset
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    core.wait(thisTrial['fixT'])
    return fixStart

def MWQ_screen(myClock, i, thisTrial, expInfo, f):
    fixStart = fixation_screen(myClock, thisTrial)
    question.setText(thisTrial['stimPic'])
    descr.setText(thisTrial['Ans'])
    show_questions()
    win.logOnFlip(level=logging.EXP, msg='MWQ on screen') #new log haoting
    startT = myClock.getTime()
    keyResp, respRT, CORR = getResp(thisTrial['stimType'], startT, 300, myClock, thisTrial)
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    saveResp(f, i, thisTrial, expInfo, keyResp, respRT, CORR, startT, fixStart)


def NoGo_screen(myClock, i, thisTrial, expInfo, f, feedback=True):
    fixStart = fixation_screen(myClock, thisTrial)
    im.setImage(thisTrial['stimPic'])
    show_stim()
    win.logOnFlip(level=logging.EXP, msg='Stimulus on screen') #new log haoting
    startT = myClock.getTime()
    keyResp, respRT, CORR = getResp(thisTrial['stimType'], startT, thisTrial['stimT'], myClock, thisTrial)
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    core.wait(thisTrial['stimT'])
    if feedback==True and thisTrial['stimType'] == 'TT':
        feedback_screen(keyResp, CORR)
    saveResp(f, i, thisTrial, expInfo, keyResp, respRT, CORR, startT, fixStart)


def switch_screen(myClock, i, thisTrial, expInfo, f):
    fixStart = fixation_screen(myClock, thisTrial)
    msgTxt.setText(thisTrial['stimPic'])
    msgTxt.draw()
    win.flip()
    win.logOnFlip(level=logging.EXP, msg='Switch text on screen') #new log haoting
    startT = myClock.getTime() #stimulus on set
    keyResp, thisRT, respRT, CORR = reset_output()
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    core.wait(thisTrial['stimT'])
    saveResp(f, i, thisTrial, expInfo, keyResp, respRT, CORR, startT, fixStart)
    
def freetxt(datafn):
	# this whole function can run on itself for gathering free text responses.
	CapturedResponseString = visual.TextStim(win,text='', font= sans, name='FreeTextMW',
		height=34, wrapWidth=1100, 
		pos=[-600,100], alignHoriz ='left', alignVert='top', 
		color='black', 
		)
	freetxt_instr = codecs.open('Instructions'+ os.sep+ 'FreeText_respinstr.txt', 'r', encoding='utf-8').read()
	ResponseInstruction = visual.TextStim(win,text=freetxt_instr, font= sans, name='FreeTextInstruction',
		pos=[0,300], height=34, wrapWidth=1100,
		color='black',
		) #object to display instructions

	def updateTheResponse(captured_string):
		CapturedResponseString.setText(captured_string)
		CapturedResponseString.draw()
		ResponseInstruction.setText(freetxt_instr)
		ResponseInstruction.draw()
		win.flip()

	def saveThisTxt(datafn, captured_string):
		outfile = datafn + '_text.txt'
		f = codecs.open(outfile, 'a', encoding='utf-8') #open our results file in append mode so we don't overwrite anything
		f.write(captured_string) #write the string they typed
		f.write('; typed at %s' %time.asctime()) #write a timestamp (very course)
		f.write('\n') # write a line ending
		f.close() #close and "save" the output file

	captured_string = ''
	CaptureResp = True
	shift_flag = False
	BeforeTyping = codecs.open('Instructions'+ os.sep+ 'FreeText_instr.txt', 'r', encoding='utf-8').read()
	msgTxt.setText(BeforeTyping)
	msgTxt.draw()
	win.flip()
	event.waitKeys('space')
	updateTheResponse(captured_string + '|')
	while CaptureResp:
	    # now we will keep tracking what's happening on the keyboard
	    # until the participant hits the return key
	     # only changes when they hit return
	    
	    #check for Esc key / return key presses each frame
		for key in event.getKeys():
	        #quit at any point
			if event.getKeys(keyList = ['escape']):
				quitEXP(True)
	        #allow the participant to do deletions too , using the 
	        # delete key, and show the change they made
			elif key in ['return']:
				saveThisTxt(datafn, captured_string)
				CaptureResp = False
				break
			elif key in ['delete','backspace']:
				captured_string = captured_string[:-1] #delete last character
				updateTheResponse(captured_string)
	        #handle spaces
			elif key in ['space']:
				captured_string += ' '
				updateTheResponse(captured_string)
			elif key in ['period']:
				captured_string += '.'
				updateTheResponse(captured_string)
			elif key in ['comma']:
				captured_string += ','
				updateTheResponse(captured_string)
			elif key in ['lshift','rshift']:
				shift_flag = True
			elif key in ['lctrl', 'rctrl', 'lwindows', 'capslock', 'right', 'left']:	
				pass #do nothing when some keys are pressed
			else: 
				if shift_flag:
					captured_string += chr(ord(key) - ord(' '))
					shift_flag = False
				else:
					captured_string = captured_string + key
				#show it
			updateTheResponse(captured_string + '|') 

def endExp():
    endtxt = codecs.open('Instructions'+ os.sep+ 'end_instr.txt', 'r', encoding='utf-8').read().split('#\n')[0]
    msgTxt.setText(endtxt)
    msgTxt.draw()
    win.flip()
    event.waitKeys(maxWait = 20)
    logging.flush()
    # f.close()
    win.close()
    core.quit()


def expTrial(myClock, trials, datafn, expInfo, feedback=True, MW_description=False): 
    keyResp, thisRT, respRT, CORR = reset_output()
    nEndStart = trials.shape[0] - 22 
    headers = 'TrialIndex,StimIndex,nBack,stimType,fixStart,fixT,stimStart,stimT,stimPic,mwType,Ans,keyResp,respCORR,respRT,IDNO,Session\n'
    f = open_datalog(datafn, dataformat='_data.csv', headers=headers)
    for i, thisTrial in enumerate(trials):
        # if i ==0:
        #     headers = 'TrialIndex,StimIndex,nBack,stimType,fixStart,fixT,stimStart,stimT,stimPic,mwType,Ans,keyResp,respCORR,respRT,IDNO,Session\n'
        #     f = open_datalog(datafn, dataformat='_data.csv', headers=headers)
        # else:
        #     pass   
        if thisTrial['stimType'] == 'Switch':
            switch_screen(myClock, i, thisTrial, expInfo, f)
        elif thisTrial['stimType'] == 'MWQ':
            MWQ_screen(myClock, i, thisTrial, expInfo, f)
        elif thisTrial['stimType'] == 'END':
        	if i == nEndStart:
        		endlooptxt = codecs.open('Instructions'+ os.sep+ 'endloop_instr.txt', 'r', encoding='utf-8').read().split('#\n')[0]
        		msgTxt.setText(endlooptxt)
        		msgTxt.draw()
        		win.flip()
        		event.waitKeys('space')
        		MWQ_screen(myClock, i, thisTrial, expInfo, f)
        	else:
        		MWQ_screen(myClock, i, thisTrial, expInfo, f)
        else:
            NoGo_screen(myClock, i, thisTrial, expInfo, f, feedback)
    f.close()
    freetxt(datafn)
    endExp()

