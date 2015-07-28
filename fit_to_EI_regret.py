import jb.jbgp_1d as gp
import jb.jbaqusitionFunctions as acq
import numpy as np
from numpy import array as npa
from numpy.random import RandomState
from scipy.optimize import minimize_scalar
from pandas import DataFrame, concat
import pdb

rngseed = None  # if want to replicate exactly
if rngseed: rng = RandomState(rngseed)
else: rng = RandomState()

# idf0 = rng.randint(NROW)
# trialSeries = df.iloc[idf0]


def fit_subject_ls_wrt_eiregret(dfs):
    fitfcn = lambda ls: (eiregret_subject(dfs, ls).regret).sum()
    res = minimize_scalar(fitfcn, bounds=(0.0001, 0.5), method='bounded')
    return res


def eiregret_experiment(df, ls=None):
    subjectdfs = []
    for iwid, wid in enumerate(df.workerid.unique()):
        try:
            print str(iwid) + ' of ' + str(len(df.workerid.unique()))
            dfs = df[df.workerid==wid]
            subjectdfs.append(eiregret_subject(dfs, ls))
        except:
            msg = ''.join([wid, ' failed'])
            print Warning(msg)
    return concat(subjectdfs)


def eiregret_subject(dfs, ls=None):
    assert len(dfs.workerid.unique())==1
    assert len(dfs.LENSCALE.unique())==1
    if not ls: ls=dfs.LENSCALE.iat[0]
    trialdfs = []
    for itrial in dfs.itrial.unique():
        dft = dfs[dfs.itrial==itrial]
        assert dft.shape[0] == 1
        trialSeries = dft.iloc[0]
        trialdfs.append(eiregret_trialSeries(trialSeries, ls))
    return concat(trialdfs)


def eiregret_trialSeries(trialSeries, ls=None, firstN=None):
    if not ls: ls=trialSeries.LENSCALE  # default use experiment lenscale
    wid = trialSeries.workerid
    itrial = trialSeries.itrial
    condition = trialSeries.condition
    counterbalance = trialSeries.counterbalance
    sigvar = trialSeries.SIGVAR
    noisevar2 = 1e-7
    DOMAIN = np.linspace(0, 1, 1028)
    KDOMAIN = gp.K_se(DOMAIN, DOMAIN, ls, sigvar)

    # trial by trial fits to expected improvement
    nPassiveObs = len(trialSeries.xPassiveObs)
    nActiveObs = len(trialSeries.xActiveObs)
    xActive = trialSeries.xActiveObs
    yActive = trialSeries.yActiveObs
    xPassive = trialSeries.xPassiveObs
    yPassive = trialSeries.yPassiveObs

    minidicts = []
    if firstN: nActiveObs = firstN
    for iActive in xrange(nActiveObs):  # run analysis for each active choice
        # get active obs to this point
        xAct = xActive[:iActive]
        yAct = yActive[:iActive]
        # combine all obs seen to this point
        xObs = npa(xAct + xPassive)
        yObs = npa(yAct + yPassive)
        xBest = xObs.max()
        yBest = yObs.max()
        # get posterior
        mu = gp.conditioned_mu(DOMAIN, xObs, yObs, ls, sigvar, noisevar2)
        cm = gp.conditioned_covmat(DOMAIN, KDOMAIN, xObs, ls, sigvar, noisevar2)
        sd = np.diag(cm)
        # get EI guess
        eiout = acq.EI(yBest, mu, sd, DOMAIN, return_whole_domain=True)
        xEI = eiout['xmax']
        yEI = eiout['fmax']
        domainEI = eiout['fall']
        iEI = np.where(DOMAIN>=xEI)[0][0]
        # get subject guess
        xSub = xActive[iActive]
        ySub = yActive[iActive]
        iSub = np.where(DOMAIN>=xSub)[0][0]
        # get regret
        evyEI = domainEI[iEI]
        evySub = domainEI[iSub]
        # compare
        regret = evyEI - evySub
        # store
        minidicts.append({'regret': regret,
                        'evyEI': evyEI,
                        'evySub': evySub,
                        'xEI': xEI,
                        'yEI': yEI,
                        'xSub': xSub,
                        'ySub': ySub,
                        'iActive': iActive,
                        'xPassive': xPassive,
                        'yPassive': yPassive,
                        'lenscale': ls,
                        'xAct': xAct,
                        'yAct': yAct,
                        'workerid': wid,
                        'itrial': itrial,
                        'condition': condition,
                        'counterbalance': counterbalance})
    return DataFrame(minidicts)
