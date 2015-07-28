+ make sure have raw/, prepped/, output/, and figs/ subfolders in home folder
+ set EXPNAME and EXPDATE for what data to pull in pull_prep_pickle_data.py
+ python pull_prep_pickle_data.py
+ set EXPNAME and EXPDATE for what data to analyze in fit_ls_eireget_sub_runner.py
+ python fit_ls_eireget_sub_runner.py {{SUBJECT NUMBER}}
+ set EXPNAME and EXPDATE for what data to stitch into df in ls_eiregret_analysis.py
+ python ls_eiregret_analysis.py
+ set EXPNAME and EXPDATE in plot_ls_expVfit.R file
+ run that .R file to output fits figure
