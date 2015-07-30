from fit_ls_eiregret_sub_runner import fit_ls_to_EIregret_sub
from jbutil import stitch_pickled
import prep_bayesOpt
# from prep_bayesOpt import load_pickled, load_sql
from numpy.random import RandomState
rng = RandomState()
import pdb
from time import time
from os import environ, getcwd
from os.path import isfile
from glob import glob
from pandas import Series, DataFrame, concat, merge, read_pickle
from jb.jbutil import merge_first
from time import time
import sys

if __name__ == '__main__':
    EXPNAME = 'myopic_exp0'
    EXPDATE = '072715'  # date that the raw data was pulled from database
    BASEFOLDER = './'
    # FIXME: not actually raw; processed by prep_bayesOpt.load_*
    RAWFOLDER = BASEFOLDER + 'raw/'  # where data pulled from database is.
    PREPPEDFOLDER = BASEFOLDER + 'prepped/'  # where data is after being scrubbed after pulled from db
    OUTFOLDER = BASEFOLDER + 'output/'  # where results will be saved
    OUT_DF_NAME = '_'.join(['df_lsfit_regret', EXPNAME, EXPDATE])
    SUBSERIES_FNAME = '_'.join(['series_lsfit_regret', EXPNAME, EXPDATE])  # template for the name of the output of the analysis

    # ### uncomment to source from pkl
    PICKLED_DF_NAME = '_'.join(['df', EXPNAME, EXPDATE]) + '.pkl'
    # df = prep_bayesOpt.load_pickled(PREPPEDFOLDER + PICKLED_DF_NAME)  #FIXME: commented out bc not working yet
    #FIXME: line below uses a hacked prepped dataset prepped in ipython
    df = unpickle(PREPPEDFOLDER + PICKLED_DF_NAME)
    # ### uncomment to source from AWS
    # AWS_DB_URL = 'mysql://jsb4:PASSWORD@mydb.c4dh2hic3vxp.us-east-1.rds.amazonaws.com:3306/myexp'
    # SQL_TABLE_NAME = 'bayesOpt_e'
    # df = prep_bayesOpt.load_sql(AWS_DB_URL, SQL_TABLE_NAME)

    # get this subject's id
    wids = df.workerid.unique()
    # get fits
    [fit_ls_to_EIregret_sub(df, wid, SUBSERIES_FNAME, OUTFOLDER) for wid in wids]

    # stitch into a df
    df_lsfits = stitch_pickled(OUTFOLDER+SUBSERIES_FNAME+'*.pkl')
    # unpickle raw
    dfprepped = unpickle(PREPPEDFOLDER + PICKLED_DF_NAME)
    # merge experiment condition
    merge_first(df_lsfits, dfprepped, 'LENSCALE', 'workerid')
    merge_first(df_lsfits, dfprepped, 'counterbalance', 'workerid')
    df_lsfits.rename(columns={'LENSCALE': 'exp_ls'}, inplace=True)

    # save to csv for analysis in r
    df_lsfits.to_csv(OUTFOLDER+OUT_DF_NAME+'.csv', index=False)
    df_lsfits.to_pickle(OUTFOLDER+OUT_DF_NAME+'.pkl')

