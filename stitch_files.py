from glob import glob
from pandas import Series, DataFrame, concat, merge, read_pickle
from jb.jbutil import merge_first
import pdb


def stitch_pickled(critstring):
    assert (critsting[-4:] == '.pkl' or critsting[-7:] =='.pickle'), 'critsting must end in pickle extension'
    subpkls = glob(critstring)
    subfits = [read_pickle(subpkl) for subpkl in subpkls]
    stitched_df = DataFrame(subfits)
    return stitched_df


df_lsfit = merge_first(df_lsfit, df, 'LENSCALE', 'workerid')
df_lsfit.rename(columns={'LENSCALE': 'exp_ls'}, inplace=True)
