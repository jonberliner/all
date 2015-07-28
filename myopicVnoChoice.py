from jb.jbdrill import jbload, jbstats, jbsac
from pandas import concat
from matplotlib import pyplot as plt

NTRIAL = 200

# ## LOCAL DB (used if dbs recently synced with sync_mysql_aws2local.sh)
# DB_URL = 'mysql://root:PASSWORD@127.0.0.1/myexp'
## AWS DB
print 'did you remember to go on AWS and change security to allow access from your IP?'
DB_URL = 'mysql://jsb4:PASSWORD@mydb.c4dh2hic3vxp.us-east-1.rds.amazonaws.com:3306/myexp'

FINISHED_STATUSES = [3,4,5,7]   # psiturk markers for a completed experiment
# trials that do not return true for all functions in criterion will not be used
CRITERION = [lambda df: 'round' in df,  # gets rid of non-my-exp trials (e.g. psiturk gunk)
            lambda df: df['round'] > 0 and df['round'] <= NTRIAL,  # same as above
            lambda df: df['status'] in FINISHED_STATUSES]  # taking complete exps only

# get experiments data
dfm = jbload.myopic_exp0(DB_URL, CRITERION)  #load myopic experiment
dfn = jbload.noChoice_exp0(DB_URL, CRITERION)  #load noChoice experiment
#TODO: move rngseed conversion to jbload
dfm['rngseed'] = dfm['rngseed'].astype(str)
dfn['rngseed'] = dfn['rngseed'].astype(str)
df = concat([dfm, dfn])  # combine both experiments into same df
df.reset_index(inplace=True, drop=True)
df.rename(columns={'round': 'itrial'}, inplace=True)  # better names

# verify that our yolking worked out correctly
for itrial in range(NTRIAL):
    dft = df[df.itrial==itrial]  # get this trial
    # get number of samples in this trial for everyone in this yolk set
    tmp = dft.groupby('rngseed').apply(lambda df0: df0.nObs.unique())
    # assert everyone in this counterbalance had same stream of number of obs
    for rr in tmp:
        assert(len(rr)==1)

# get average distance between myopic and noChoice
m_mu_sam2obs = jbsac.sac(dfm, 
        lambda df0: jbstats.dBetween(df0, 'samX', 'obsX'),  # apply this fcn...
        'workerid',  # split up by this field...
        ['condition', 'experiment', 'rngseed'],  # while keeping these labels for the returned df...
        'mu_d')  # ...and labeling that result this

n_mu_drill2obs = jbsac.sac(dfn, lambda df0:
        jbstats.dBetween(df0, 'drillX', 'obsX'), 'workerid',
        ['condition', 'experiment', 'rngseed'], 'mu_d')

d2obs = concat([m_mu_sam2obs, n_mu_drill2obs])
d2obs.reset_index(drop=True, inplace=True)

d2obs.to_csv('d2obs_myopicVnoChoice.csv')

m_mu_sam2obs = jbstats.dBetween_analysis(dfm, 'samX', 'obsX')['worker_mu_d']
n_mu_drill2obs = jbstats.dBetween_analysis(dfn, 'drillX', 'obsX')['worker_mu_d']
worker_mu_d2obs = concat([m_mu_sam2obs, n_mu_drill2obs])
