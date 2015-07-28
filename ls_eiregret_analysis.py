from jb.jbutil import stitch_pickled, merge_first
from jb.jbpickle import unpickle
import load_and_prep
# import prep_bayesOpt

# RUN fit_ls_eiregret_sub_runner.py FOR ALL SUBJECTS BEFORE RUNNING THIS SCRIPT!
print 'RUN fit_ls_eiregret_sub_runner.py FOR ALL SUBJECTS BEFORE RUNNING THIS SCRIPT!'

EXPNAME = 'noChoice_exp0'
EXPDATE = '072415'  # date that the raw data was pulled from database
BASEFOLDER = './'
# FIXME: not actually raw; processed by prep_bayesOpt.load_*
RAWFOLDER = BASEFOLDER + 'raw/'  # where data pulled from database is.
PREPPEDFOLDER = BASEFOLDER + 'prepped/'  # dfs prepped after extracting from db
OUTFOLDER = BASEFOLDER + 'output/'  # where results will be saved
SUBSERIES_FNAME = '_'.join(['series_lsfit_regret', EXPNAME, EXPDATE])  # template for the name of the output of the analysis
OUT_DF_NAME = '_'.join(['df_lsfit_regret', EXPNAME, EXPDATE])
PICKLED_DF_NAME = '_'.join(['df', EXPNAME, EXPDATE]) + '.pkl'

# stitch into a df
df_lsfits = stitch_pickled(OUTFOLDER+SUBSERIES_FNAME+'*.pkl')
# unpickle raw
dfraw = unpickle(RAWFOLDER + PICKLED_DF_NAME)
# merge experiment condition
merge_first(df_lsfits, dfraw, 'LENSCALE', 'workerid')
merge_first(df_lsfits, dfraw, 'counterbalance', 'workerid')
df_lsfits.rename(columns={'LENSCALE': 'exp_ls'}, inplace=True)

# save to csv for analysis in r
df_lsfits.to_csv(OUTFOLDER+OUT_DF_NAME+'.csv', index=False)
df_lsfits.to_pickle(OUTFOLDER+OUT_DF_NAME+'.pkl')

