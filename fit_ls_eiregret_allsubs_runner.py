from fit_to_EI_regret import fit_subject_ls_wrt_eiregret
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

# make into function that can pass to minimize_scalar
get_dfs = lambda df, wid: df[df.workerid==wid]
fit_sub = lambda df, wid: fit_subject_ls_wrt_eiregret(get_dfs(df, wid))

def fit_ls_to_EIregret_sub(df, wid, subseries_fname, savefolder, force_run_all=False):
    try:
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
    except:
        print Warning(wid + ' failed')
    sys.stdout.flush()


if __name__ == '__main__':
    iwid = int(sys.argv[1])

    EXPNAME = 'noChoice_exp0'
    EXPDATE = '072415'  # date that the raw data was pulled from database

    BASEFOLDER = './'
    # FIXME: not actually raw; processed by prep_bayesOpt.load_*
    RAWFOLDER = BASEFOLDER + 'raw/'  # where data pulled from database is.
    OUTFOLDER = BASEFOLDER + 'output/'  # where results will be saved
    SUBSERIES_FNAME = '_'.join(['series_lsfit_regret', EXPNAME, EXPDATE])  # template for the name of the output of the analysis
    OUT_DF_NAME = '_'.join(['df_lsfit_regret', EXPNAME, EXPDATE])

    # ### uncomment to source from pkl
    PICKLED_RAWDF_NAME = '_'.join(['df', EXPNAME, EXPDATE]) + '.pkl'  #JBEDIT: is EXPDATE helpful?  or should throw away?

    df = load_and_prep.load_pickled(RAWFOLDER + PICKLED_RAWDF_NAME)
    df = load_and_prep.prep(df, 'noChoice_exp0')

    # get this subject's id
    wids = df.workerid.unique()
    print wids.shape
    wid = wids[iwid]

    # get fits
    fit_ls_to_EIregret_sub(df, wid, SUBSERIES_FNAME, OUTFOLDER)
    # stitch into a df
    df_lsfits = stitch_sub_fits(SUBSERIES_FNAME, OUTFOLDER)
    # save to csv for analysis
    df_lsfits.to_csv(OUTFOLDER + OUT_DF_NAME + '.csv', index=False)
    df_lsfits.to_pickle(OUTFOLDER + OUT_DF_NAME + '.pkl')

