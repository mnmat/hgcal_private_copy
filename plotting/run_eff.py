import os

#SAMPLE_LABEL = ["\"Single photons\"", "\"Single pions\"", "\"Single electrons\""]
#SAMPLE_FILE = ["singlephoton", "singlepi", "singleel"]
#SAMPLE_LABEL = ["\"Single electrons\""]
#SAMPLE_FILE = ["singleel"]
SAMPLE_LABEL = ["\"Single kaons\""]
SAMPLE_FILE = ["singleKaonL"]

RELEASE_TAG = ["after_60c3c21"]#, "before"]

ITERS = ["\"Global:ticlMultiClustersFromTrackstersMerge\" \"TrkEM:ticlMultiClustersFromTrackstersTrkEM\" \"EM:ticlMultiClustersFromTrackstersEM\" \"TrkHAD:ticlMultiClustersFromTrackstersTrk\" \"HAD:ticlMultiClustersFromTrackstersHAD\"",
         "\"Global:ticlMultiClustersFromTrackstersMerge\" \"Trk:ticlMultiClustersFromTrackstersTrk\" \"EM:ticlMultiClustersFromTrackstersEM\" \"HAD:ticlMultiClustersFromTrackstersHAD\""]

FEATURES = "\"E = 10 GeV:91:22\" \"E = 50 GeV:94:21\" \"E = 100 GeV:64:21\" \"E = 200 GeV:57:21\" \"E = 300 GeV:52:21\""

for tag,i_iter in zip(RELEASE_TAG,ITERS) :

  PATHFILESIN = "/home/ericabro/ericabro_cernbox/HGCal_Software/EMTrackSeeded/"+tag+"/"

  for i_label,i_samplefile in zip(SAMPLE_LABEL,SAMPLE_FILE):
    FILENAMES = ["DQM_V0001_R000000001__step4_"+i_samplefile+"__e10GeV__nopu.root", "DQM_V0001_R000000001__step4_"+i_samplefile+"__e50GeV__nopu.root", 
                 "DQM_V0001_R000000001__step4_"+i_samplefile+"__e100GeV__nopu.root", 
                 "DQM_V0001_R000000001__step4_"+i_samplefile+"__e200GeV__nopu.root", "DQM_V0001_R000000001__step4_"+i_samplefile+"__e300GeV__nopu.root"]

    listFilein = ""
    for filein in FILENAMES:
      listFilein = listFilein + PATHFILESIN + filein + " "

    PATHFILESOUT = tag+"/"+i_samplefile+"/"
    if not os.path.exists(PATHFILESOUT):
      os.makedirs(PATHFILESOUT)


    command_plot = "python produce_plots_plotting_eff.py --filesin %s --folderout %s --sample %s --features %s --iter %s -v"%(listFilein,PATHFILESOUT,i_label,FEATURES,i_iter)

    print(command_plot)
    os.system(command_plot)

