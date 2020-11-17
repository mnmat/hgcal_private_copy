import os

SAMPLE_LABEL = ["\"Single photons, 1 Sim Clu\"", "\"Single pions, 1 Sim Clu\"", "\"Single electrons, 1 Sim Clu\"", "\"Single kaons, 1 Sim Clu\""]
SAMPLE_FILE = ["singlephoton", "singlepi", "singleel", "singleKaonL"]
#SAMPLE_LABEL = ["\"Single pions, 1 Sim Clu\""]
#SAMPLE_FILE = ["singlepi"]

RELEASE_TAG = ["92c59aa_model197566b"]#, "before"]

ITERS = ["\"Dummy:ticlMultiClustersFromTrackstersDummy\" \"Merged:ticlMultiClustersFromTrackstersMerge\" \"TrkEM:ticlMultiClustersFromTrackstersTrkEM\" \"EM:ticlMultiClustersFromTrackstersEM\" \"TrkHAD:ticlMultiClustersFromTrackstersTrk\" \"HAD:ticlMultiClustersFromTrackstersHAD\"",
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

