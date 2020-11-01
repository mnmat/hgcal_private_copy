import os


SAMPLE_LABEL = ["Single photons", "Single pions", "Single electrons", "Single kaons"]
SAMPLE_FILE = ["singlephoton", "singlepi", "singleel", "singleKaonL"]

RELEASE_TAG = ["after_60c3c21_model197566b"]

ITERS = ["TrkEM", "EM", "Trk", "HAD"]

FEATURES = "\"E = 10 GeV:91:22\" \"E = 50 GeV:94:21\" \"E = 100 GeV:64:21\" \"E = 200 GeV:57:21\" \"E = 300 GeV:52:21\""

for tag in RELEASE_TAG :
  PATHFILESIN = "/home/ericabro/ericabro_cernbox/HGCal_Software/EMTrackSeeded/"+tag+"/"
  for i_label,i_samplefile in zip(SAMPLE_LABEL,SAMPLE_FILE):
    FILENAMES = ["DQM_V0001_R000000001__step4_"+i_samplefile+"__e10GeV__nopu.root", "DQM_V0001_R000000001__step4_"+i_samplefile+"__e50GeV__nopu.root", 
                 "DQM_V0001_R000000001__step4_"+i_samplefile+"__e100GeV__nopu.root", 
                 "DQM_V0001_R000000001__step4_"+i_samplefile+"__e200GeV__nopu.root", "DQM_V0001_R000000001__step4_"+i_samplefile+"__e300GeV__nopu.root"]

    listFilein = ""
    for filein in FILENAMES:
      listFilein = listFilein + PATHFILESIN + filein + " "

    for i_iter in ITERS :
      PATHFILESOUT = tag+"/"+i_samplefile+"_"+i_iter+"/"
      if not os.path.exists(PATHFILESOUT):
        os.makedirs(PATHFILESOUT)
  
      HISTOPREFIX = "\"DQMData/Run 1/HGCAL/Run summary/TICLTracksters/ticlTracksters"+i_iter+"/\""
      HISTONAMES = "\"Regressed Energy\""
      AXISTITLES = "\";Regressed Energy;#Tracksters\""
      #HISTOPREFIX = "\"DQMData/Run 1/HGCAL/Run summary/HGCalValidator/ticlMultiClustersFromTracksters"+i_iter+"/\""
      #HISTONAMES = "multicluster_energy"
      #AXISTITLES = "\";Raw Energy;#Tracksters\""
 
      final_label = "\"" + i_label + ", " + i_iter + " iter only"  + "\""
      command_plot = "python produce_plots_plotting_energy.py --filesin %s --folderout %s --histoprefix %s --histonames %s --varAxes %s --sample %s --features %s -v"%(listFilein,PATHFILESOUT,HISTOPREFIX,HISTONAMES,AXISTITLES,final_label,FEATURES)
  
      print(command_plot)
      os.system(command_plot)

