import os

SAMPLE_LABEL = ["\"Single photons, 1 Sim Clu\"", "\"Single pions, 1 Sim Clu\"", "\"Single electrons, 1 Sim Clu\"", "\"Single kaons, 1 Sim Clu\""]
SAMPLES = ["singlephoton", "singlepi", "singleel", "singleKaonL"]
#SAMPLE_LABEL = ["\"Single pions, 1 Sim Clu\""]
#SAMPLES = ["singlepi"]
GENPRODUCER = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy"}

RELEASE_TAG = ["vanilla"]

ITERS = ["\"Dummy:ticlMultiClustersFromTrackstersDummy\" \"Merged:ticlMultiClustersFromTrackstersMerge\" \"TrkEM:ticlMultiClustersFromTrackstersTrkEM\" \"EM:ticlMultiClustersFromTrackstersEM\" \"TrkHAD:ticlMultiClustersFromTrackstersTrk\" \"HAD:ticlMultiClustersFromTrackstersHAD\""]

FEATURES = "\"E = 10 GeV:91:22\" \"E = 50 GeV:94:21\" \"E = 100 GeV:64:21\" \"E = 200 GeV:57:21\" \"E = 300 GeV:52:21\""
PATHFILESIN = "/data2/user/ebrondol/HGCal/HGCDoublet_validation/CMSSW_11_2_0_pre10/TICLv3_11_2_X_pre10/production/"

for tag,i_iter in zip(RELEASE_TAG,ITERS) :

  for i_label,i_sample in zip(SAMPLE_LABEL,SAMPLES):
    inputFolder = "{}/{}_{}_hgcalCenter/step4/".format(PATHFILESIN, i_sample, GENPRODUCER[i_sample])
    FILENAMES = ["DQM_V0001_R000000001__step4_"+i_sample+"__e10GeV__nopu.root", "DQM_V0001_R000000001__step4_"+i_sample+"__e50GeV__nopu.root", 
                 "DQM_V0001_R000000001__step4_"+i_sample+"__e100GeV__nopu.root", 
                 "DQM_V0001_R000000001__step4_"+i_sample+"__e200GeV__nopu.root", "DQM_V0001_R000000001__step4_"+i_sample+"__e300GeV__nopu.root"]

    listFilein = ""
    for filein in FILENAMES:
      listFilein = listFilein + inputFolder + filein + " "

    PATHFILESOUT = tag+"/"+i_sample+"/"
    if not os.path.exists(PATHFILESOUT):
      os.makedirs(PATHFILESOUT)


    command_plot = "python produce_plots_plotting_eff.py --filesin %s --folderout %s --sample %s --features %s --iter %s -v"%(listFilein,PATHFILESOUT,i_label,FEATURES,i_iter)

    print(command_plot)
    os.system(command_plot)

