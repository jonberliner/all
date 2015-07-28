from fit_to_EI_regret import fit_subject_ls_wrt_eiregret
from jb.jbutil import stitch_pickled
from jb.jbpickle import unpickle
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

# make into function that can pass to minimize_scalar
get_dfs = lambda df, wid: df[df.workerid==wid]
fit_sub = lambda df, wid: fit_subject_ls_wrt_eiregret(get_dfs(df, wid))

def fit_ls_to_EIregret_sub(df, wid, subseries_fname, savefolder, force_run_all=False):
    # try:
    tic = time()
    print 'begin ' + wid
    sys.stdout.flush()
    subfname = savefolder + subseries_fname + wid + '.pkl'
    if (not isfile(subfname)) or force_run_all:
        print str(wid) + ' fitting now...'
        # fit subject length-scale
        subfit = fit_sub(df, wid)
        # format into series
        print 'converting to series...'
        s_subfit = Series(subfit)
        # make names more sensible
        s_subfit.rename({'fun': 'sse', #FIXME: no longer sse; should be cumulative regret
                            'x': 'fit_ls'},
                            inplace=True)
        s_subfit['workerid'] = wid
        # pickle
        print 'saving...'
        s_subfit.to_pickle(subfname)
        toc = time()
        print wid + ' saved successfully in ' + str(toc-tic) + ' seconds'
    else:
        print wid + 'already run (pass force_run_all=True to force rerun)'
    # except:
    #     print Warning(wid + ' failed')
    sys.stdout.flush()


if __name__ == '__main__':
    iwid = int(sys.argv[1])

    EXPNAME = 'myopic_exp0'
    EXPDATE = '072715'  # date that the raw data was pulled from database
    BASEFOLDER = './'
    # FIXME: not actually raw; processed by prep_bayesOpt.load_*
    RAWFOLDER = BASEFOLDER + 'raw/'  # where data pulled from database is.
    PREPPEDFOLDER = BASEFOLDER + 'prepped/'  # where data is after being scrubbed after pulled from db
    OUTFOLDER = BASEFOLDER + 'output/'  # where results will be saved
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
    print wids.shape
    wid = wids[iwid]

    # get fits
    fit_ls_to_EIregret_sub(df, wid, SUBSERIES_FNAME, OUTFOLDER)
