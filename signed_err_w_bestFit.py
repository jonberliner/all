from jb.jbutil import merge_first
from pandas import DataFrame, read_pickle
from fit_to_EI import ei_subject
import ggplot as gg
import pdb

OUTFOLDER = '/Users/jsb/Documents/drilling/analyses/bayesOpt_a/output/'
RAWFOLDER = '/Users/jsb/Documents/drilling/analyses/bayesOpt_a/raw/'

DF_NAME = 'df_bayesOpt_e_062515.pkl'
# name of pickled df with lenscales that best fit EI prediction of sub data
DF_FIT_NAME = 'df_lsfit_062615.pkl'

df = read_pickle(RAWFOLDER + DF_NAME)
df_lsfits = read_pickle(OUTFOLDER + DF_FIT_NAME)  # load
df = merge_first(df, df_lsfits, 'fit_ls', 'workerid')  # add fit_ls to exp data
df.rename(columns={'LENSCALE': 'exp_ls'}, inplace=True)
df_xDiff_wrt_fitls = df.groupby('workerid')\
            .apply(lambda dfs: ei_subject(dfs, dfs.fit_ls.iat[0]))\
            .reset_index(drop=True)\

df_xDiff_wrt_fitls.to_pickle(OUTFOLDER + 'df_xDiff_wrt_fitls_062615.pkl')

df_xDiff_wrt_fitls.groupby('workerid').std()
