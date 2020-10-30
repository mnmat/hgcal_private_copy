import os

SAMPLE = "\"Single kaons, HAD iter only\""

#fixedPt
PATHFILESIN = "/home/ericabro/ericabro_cernbox/HGCal_Software/EMTrackSeeded/after_60c3c21/"
PATHFILESOUT = "after_60c3c21/plots_kaons_HAD/"

if not os.path.exists(PATHFILESOUT):
    os.makedirs(PATHFILESOUT)

FILENAMES = ["DQM_V0001_R000000001__step4_singleKaonL__e10GeV__nopu.root", "DQM_V0001_R000000001__step4_singleKaonL__e50GeV__nopu.root", "DQM_V0001_R000000001__step4_singleKaonL__e100GeV__nopu.root", 
             "DQM_V0001_R000000001__step4_singleKaonL__e200GeV__nopu.root", "DQM_V0001_R000000001__step4_singleKaonL__e300GeV__nopu.root"]
FEATURES = "\"E = 10 GeV:91:22\" \"E = 50 GeV:94:21\" \"E = 100 GeV:64:21\" \"E = 200 GeV:57:21\" \"E = 300 GeV:52:21\""

#HISTOPREFIX = "\"DQMData/Run 1/HGCAL/Run summary/TICLTracksters/ticlTrackstersEM/\""
#HISTONAMES = "\"Regressed Energy\""
#AXISTITLES = "\";Regressed Energy;#Tracksters\""
HISTOPREFIX = "\"DQMData/Run 1/HGCAL/Run summary/HGCalValidator/ticlMultiClustersFromTrackstersHAD/\""
HISTONAMES = "multicluster_energy"
AXISTITLES = "\";Raw Energy;#Tracksters\""

listFilein = ""
for filein in FILENAMES:
  listFilein = listFilein + PATHFILESIN + filein + " "

command_plot = "python produce_plots_plotting_energy.py --filesin %s --folderout %s --histoprefix %s --histonames %s --varAxes %s --sample %s --features %s -v"%(listFilein,PATHFILESOUT,HISTOPREFIX,HISTONAMES,AXISTITLES,SAMPLE,FEATURES)

print(command_plot)
os.system(command_plot)

