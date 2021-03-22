import os
from collections import OrderedDict

SAMPLE_LABEL = ["\"Single #gamma, non-converted\"", "\"Single #pi^{#pm}, non-converted\"", "\"Single e^{#pm}, non-converted\"", "\"Single K^{0}_{L}, non-converted\""]
SAMPLES = ["singlephoton", "singlepi", "singleel", "singleKaonL"]
#SAMPLE_LABEL = ["\"Single pions, 1 Sim Clu\""]
#SAMPLES = ["singlepi"]
GENPRODUCER = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy"}

RELEASE_TAG = ["vanilla"]

iterLabel = OrderedDict([#("Dummy","Dummy"), 
			 ("TrkEM","TrkEM"), ("EM","EM"), ("Trk","TrkHAD"), ("HAD","HAD")
                         , ("Merge","Merge")
                        ])
ITERS = [' '.join("\""+iterLabel[ticlIter]+":ticlMultiClustersFromTracksters"+ticlIter+"\"" for ticlIter in iterLabel)]

#PATHFILESIN = "/data2/user/ebrondol/HGCal/HGCDoublet_validation/CMSSW_11_2_0_pre10/TICLv3_11_2_X_pre10/production/"
PATHFILESIN = "/data2/user/lecriste/HGCal/samples/TICLDebugger/EMTrackSeeded/92c59aa-pre10_model138329a/"

energies_features = OrderedDict([#("10",91), 
("50",94), ("100",64), ("200",57), ("300",52)])
FEATURES = ' '.join("\"E = "+key+" GeV:"+str(energies_features[key])+":21\"" for key in energies_features)
for tag,i_iter in zip(RELEASE_TAG,ITERS) :

  for i_label,i_sample in zip(SAMPLE_LABEL,SAMPLES):
    inputFolder = "{}/{}_{}_hgcalCenter/step4/".format(PATHFILESIN, i_sample, GENPRODUCER[i_sample])
    FILENAMES = ["DQM_V0001_R000000001__step4_"+i_sample+"__e"+key+"GeV__nopu.root" for key in energies_features]

    listFilein = ""
    for filein in FILENAMES:
      listFilein = listFilein + inputFolder + filein + " "

    PATHFILESOUT = tag+"/"+i_sample+"/"
    if not os.path.exists(PATHFILESOUT):
      os.makedirs(PATHFILESOUT)


    command_plot = "python produce_plots_plotting_eff.py --filesin %s --folderout %s --sample %s --features %s --iter %s -v"%(listFilein,PATHFILESOUT,i_label,FEATURES,i_iter)

    print(command_plot)
    os.system(command_plot)

