from pandas import read_pickle
from numpy import isnan
from jb.jbprep import sql2pandas
from old_but_needed import jbload

################################
#  PREPROCESSING DATA
################################

def load_sql(DB_URL, TABLE_NAME):
    df = sql2pandas(DB_URL, TABLE_NAME)
    return df


def load_pickled(fname):
    assert (fname[-4:] == '.pkl' or fname[-7:] =='.pickle'), 'fname must be a pickle file'
    df = read_pickle(fname)
    return df

def load_legacy(db_url, expname):
    if expname=='noChoice_exp0':
        FINISHED_STATUSES = [3,4,5,7]
        # trials that do not return true for all functions in criterion will not be used
        CRITERION = [lambda df: 'round' in df,
                    lambda df: df['round'] > 0 and df['round'] <= 200,
                    lambda df: df['status'] in FINISHED_STATUSES]
        df = jbload.noChoice_exp0(db_url, CRITERION)
        return df

def filter_df(df, critfcns):
    """take only rows that return True for all functions in critfcns"""
    for critfcn in critfcns:
        crit = critfcn(df)
        df = df[crit]
    return df


def prep(df, expname):
    if expname == 'bayesOpt':
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

        df = filter_df(df, critfcns)

    elif expname == 'noChoice_exp0':
        #FIXME: need to make so doesn't have to have these names; not correct to call a drill an active observation
        df.rename(columns={'obsX': 'xPassiveObs',
                        'obsY': 'yPassiveObs',
                        'drillX': 'xActiveObs',  
                        'drillY': 'yActiveObs',
                        'round': 'itrial'},
                inplace=True)

        tmp = df.xPassiveObs
        tmp = tmp.map(lambda x: x.tolist())
        df['xPassiveObs'] = tmp

        tmp = df.yPassiveObs
        tmp = tmp.map(lambda x: x.tolist())
        df['yPassiveObs'] = tmp

        tmp = df.xActiveObs
        tmp = tmp.map(lambda x: [x])
        df['xActiveObs'] = tmp

        tmp = df.yActiveObs
        tmp = tmp.map(lambda x: [x])
        df['yActiveObs'] = tmp

        return df
