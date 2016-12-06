'''
Before running this file, please check:
1) all the participant and session information on the FILENAMES are correct.
2) all the participant and session information in the file are stroed under correct columns.
3) logs with wrong data are not in the data directory if you want to run in batch
4) this file can handle single data log
'''

# raw data directory
# i.e. DATA_DIR = 'R:\LabData\CohortData\TaskSwitch\*_taskswitching*.csv'
DATA_DIR = 'R:\\Cohort_2016-2017\\MindWanderingTask_psychopy\\data_mindwandering_CS201617\\5*_mindwandering_CS201617*_data.csv'

# results 
# i.e. RESULT_DIR = 'U:\Projects\CS_Analysis\Results'
RESULT_DIR = 'U:\\Projects\\CS3_Analysis\\Results'

# task name. use in the result output file
EXPNAME = 'MindWandering'

# Are you only analysing a sub set?
subset = True

# A list of participant number
# this only applies when you wish to analyse a subset
# This must match the IDs on the csv filename
PPT_ID = [500, 501, 502, 503]
################################################ Advanced settings. #################################################
'''
These variables have already been set for the analysis. No cofiguration required. 
'''

# the list of lable name(s) for independent varable(s) you care in your files
# i.e. multiple variables: Label_IV = ['dimension', 'CSI', 'type']
# i.e. only one variables: Label_IV = ['dimension']
Label_IV = ['nBack', 'stimType', 'mwType'] 

# the list of lable name(s) for dependent varable(s) you care in your files
# i.e. multiple variables: Label_DV = ['resp.rt', 'resp.corr']
# i.e. only one variables: Label_DV = ['resp.rt']
Label_DV = ['keyResp', 'respRT', 'respCORR']

# the lable name for indexing the data, such as participant id or session number in a file
# i.e. Lable_id = ['participant']
# if there are more than one variable, please keep participant number as the first one
Lable_idx = ['IDNO', 'Session']
################################################ Do not change things below this line. ################################################ 

################################################ Load ExpAnalysis.py ################################################ 
import pandas as pd 
import numpy as np 
import glob, os, sys, errno
import itertools

def get_DIRs(DATA_DIR, subset, PPT_ID):
	'''
	DATA_DIR: string; 
	raw data directory with filename patten; 
	i.e. DATA_DIR = 'R:\LabData\CohortData\TaskSwitch\*_taskswitching*.csv'

	subset: True or False; 
	True if you are only analysing some participants

	PPT_ID: list
	A list of participant number; This must match the IDs on the csv filename

	'''
	DATA_DIR = sorted(glob.glob(DATA_DIR))
	if subset:
		check_id = []
		for d in DATA_DIR:
			check_id.append(int(d.split(os.sep)[-1].split('_')[0]))
		check_id = sorted(check_id)

		if set(PPT_ID).issubset(check_id)==False:
			sys.exit('The participant ID list and the log files doesn\'t match. Please check your data under %s and variable PPT_ID.' %DATA_DIR)

		DIRs = []
		for d in DATA_DIR:
			cur_id = int(d.split(os.sep)[-1].split('_')[0])
			if cur_id in PPT_ID:
				DIRs.append(d)

	else:
		DIRs = DATA_DIR

	return DIRs


def concat_data_csvs(DIRs, Lable_idx, Label_IV, Label_DV):
	'''
	The IDs on the csv filename must be correct.
	The filename should be: [PPT_ID]_[SESSION]_[otherStuff].csv

	DIRs: list;
	a list of file paths

	Lable_idx: list
	the lable name for indexing the data, such as participant id or session number in a file
	i.e. Lable_id=['participant']
	if there are more than one variable, please keep participant number as the first one	
	the list of lable name(s) for independent varable(s) you care in your files

	Label_IV: list
	i.e. multiple variables: Label_IV=['dimension', 'CSI', 'type']
	i.e. only one variables: Label_IV=['dimension']
	
	Label_DV: list
	the list of lable name(s) for dependent varable(s) you care in your files
	i.e. multiple variables: Label_DV=['resp.rt', 'resp.corr']
	i.e. only one variables: Label_DV=['resp.rt']

	'''
	def label_check(DIRs, Label_var):

		#load a dummy file to check the informations
		tmp_dat = pd.read_csv(DIRs[0], sep=',', header=0)
		tmp_keys = tmp_dat.keys().values.tolist()
		if set(Label_var).issubset(tmp_keys):
			pass
		else:
			sys.exit('Some label(s) do not exist in file %s. Are you sure all the variables are correctly spelt?' %DIRs[0])

	Label_var = Label_IV + Label_DV + Lable_idx

	label_check(DIRs, Label_var)

	# create a empty entry for storing data frames
	df_collect = dict()
	for p in DIRs:

		# get rt, acc, condition information
		df_cur = pd.read_csv(p, sep=',', header=0)
		if set(Label_var).issubset(df_cur.keys().values.tolist()):
			df_cur_dat = df_cur[Label_var]
		else: 
			for v in Label_var:
				if set(v).issubset(df_cur.keys().values.tolist()):
					pass
				else:
					df_cur_dat[v] = None # create empty varaible for missing variables

		# get id
		# use the id on the file name as the acutal id
		cur_id = int(p.split(os.sep)[-1].split('_')[0])
		if len(Lable_idx) > 0:
			df_cur_dat[Lable_idx[0]] = list(itertools.repeat(cur_id, df_cur_dat.shape[0]))
		else:
			df_cur_dat['IDNO'] = list(itertools.repeat(cur_id, df_cur_dat.shape[0]))

		# save the participant's data to a dictionary
		df_collect[p.split(os.sep)[-1]] = df_cur_dat
		
	return pd.concat(df_collect, axis=0) # concatenate all the dataframes into long form

def save_csv(df, RESULT_DIR, EXPNAME, FILENAME): 
	'''
	save a panda dataframe as a csv file
	'''
	# check if there's a result directory
	try:
	    os.makedirs(RESULT_DIR)
	except OSError as exception:
	    if exception.errno != errno.EEXIST:
	        raise    
	#dump to disc
	df.to_csv(RESULT_DIR + os.sep + EXPNAME + '_' + FILENAME + '.csv', index=True)

#####################################################CONCATENATE FILES#######################################################
# concatenate files
DIRs = get_DIRs(DATA_DIR, subset, PPT_ID)
df_long = concat_data_csvs(DIRs, Lable_idx, Label_IV, Label_DV)
# Debug
# save_csv(df_long, RESULT_DIR, EXPNAME, FILENAME='long')

#####################################################RUN ANALYSIS#######################################################

# summary wide data

# behavioural
df_taskperformance = pd.pivot_table(df_long.query('stimType == "TT"'), values=['respRT', 'respCORR'], index=Lable_idx,
		columns=['nBack'], aggfunc=np.mean)
new_col = []
for col in df_taskperformance.columns.values:
	dv_type = col[0]
	if dv_type=='respRT':
		dv_type = 'RT'
	else:
		dv_type = 'ACC'
	cond = '%iBACK' %int(col[1])
	try:
		cur_var = '_'.join([cond, dv_type])
	except TypeError:
		cur_var = '_'.join([cond, dv_type])
	new_col.append(cur_var)

df_taskperformance.columns = new_col


if len(DIRs)==1:
	ppt = (df_long.participant.values[0])
	FILENAME = 'behaviour_summary_' + str(ppt)
	save_csv(df_taskperformance, RESULT_DIR, EXPNAME, FILENAME)
else: 
	FILENAME = 'behaviour_summary' 
	save_csv(df_taskperformance, RESULT_DIR, EXPNAME, FILENAME)

# Mind-wandering
MWQ_inc = ['MWQ', 'END']
df_MWQ = df_long.query('stimType in @MWQ_inc')
df_MWQ.keyResp = list(map(int, df_MWQ.keyResp.values))

MWQ_idx = []
prev_IDNO = 0
for index, row in df_MWQ.iterrows():
	cur_IDNO = row.IDNO
	cur_sess = row.Session
	if row.mwType == 'Focus':
		if prev_IDNO != cur_IDNO or prev_sess != cur_sess: 
			i = 1
		else: 
			i += 1

		MWQ_idx.append(i)
	elif row.stimType == 'MWQ' :
		MWQ_idx.append(i)
	else:
		MWQ_idx.append(99)
	prev_IDNO = row.IDNO
	prev_sess = row.Session

df_MWQ['MWQ_idx'] = MWQ_idx
Lable_idx.append('MWQ_idx')
Lable_idx.append('nBack')

df_MWQ = pd.pivot_table(df_MWQ, values=['keyResp', 'respRT'], index=Lable_idx,
	columns=['mwType'])

new_col = []
for col in df_MWQ.columns.values:
	dv_type = col[0]
	cond = col[1]
	if dv_type=='respRT':
		dv_type = 'RT'
		cur_var = '_'.join(['MWQ', cond, dv_type])
	else:
		cur_var = '_'.join(['MWQ', cond])
	
	new_col.append(cur_var)

df_MWQ.columns = new_col

if len(DIRs)==1:
	ppt = (df_long.participant.values[0])
	FILENAME = 'MWQ_RAW_' + str(ppt)
	save_csv(df_MWQ, RESULT_DIR, EXPNAME, FILENAME)
else: 
	FILENAME = 'MWQ_RAW' 
	save_csv(df_MWQ, RESULT_DIR, EXPNAME, FILENAME)
