from pandas import read_pickle
from numpy import isnan
from jb.jbprep import sql2pandas

# crit fcns for bayesOpt_e
istrial = lambda df0: df0.itrial.map(lambda itrial: not isnan(itrial))
iscomplete = lambda df0: df0.status.map(lambda status: status in [3, 4, 5, 7])
nousernans = lambda df0: df0.yActiveObs.map(lambda yA: None not in yA)
def atleast_ntrials(df, n):
    goodwids = []
    for wid in df.workerid.unique():
        dfs = df[df.workerid==wid]
        if len(dfs.itrial.unique()) >= n:
            goodwids.append(wid)
    crit = df.workerid.map(lambda wid: wid in goodwids)
    return crit

atleast_120 = lambda df0: atleast_ntrials(df0, 120)
critfcns = [istrial, iscomplete, nousernans, atleast_120]
# critfcns = [istrial, iscomplete, nousernans]


def filter_df(df, critfcns):
    """take only rows that return True for all functions in critfcns"""
    for critfcn in critfcns:
        crit = critfcn(df)
        df = df[crit]
    return df


def load_pickled(fname):
    assert (fname[-4:] == '.pkl' or fname[-7:] =='.pickle'), 'fname must be a pickle file'
    df = read_pickle(fname)
    return filter_df(df, critfcns)


def load_sql(DB_URL, TABLE_NAME):
    df = sql2pandas(DB_URL, TABLE_NAME)
    return filter_df(df, critfcns)


