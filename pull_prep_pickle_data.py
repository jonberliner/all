import load_and_prep

# FREE PARAMS
EXPNAME = 'bayesOpt_e'  # should be the name of the table in the db, which, by convention, is also the psiturk experiment folder name
EXPDATE = '072815'  # should be today

# REST OF SCRIPT
# pull from db
DB_URL = 'mysql://jsb4:PASSWORD@mydb.c4dh2hic3vxp.us-east-1.rds.amazonaws.com:3306/myexp'
if EXPNAME == 'bayesOpt_e':
    df = load_and_prep.load_sql(DB_URL, EXPNAME)
elif EXPNAME == 'myopic_exp0':
    df = load_and_prep.load_legacy(DB_URL, 'myopic_exp0')
elif EXPNAME == 'noChoice_exp0':
    df = load_and_prep.load_legacy(DB_URL, 'noChoice_exp0')
else: raise ValueError('invalid experiment name')
df.to_pickle('./raw/' + 'df_' + EXPNAME + '_' + EXPDATE + '.pkl')

# prep
df = load_and_prep.prep(df, EXPNAME)
df.to_pickle('./prepped/' + 'df_' + EXPNAME + '_' + EXPDATE + '.pkl')
