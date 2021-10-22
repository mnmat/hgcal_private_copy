import os
from collections import OrderedDict


#SAMPLE_LABEL = ["Single photons", "Single pions", "Single electrons", "Single kaons"]
#SAMPLE_FILE = ["singlephoton", "singlepi", "singleel", "singleKaonL"]
SAMPLE_LABEL = ["Single pions"]
SAMPLE_FILE = ["singlepi"]
GENPRODUCER = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy"}

RELEASE_TAG = ["vanilla"]

ITERS = ["TrkEM", "EM", "Trk", "HAD"]

energies_features = OrderedDict([#("10",91), 
                                 ("50",94), ("100",64), ("200",57), ("300",52)])
FEATURES = ' '.join("\"E = "+key+" GeV:"+str(energies_features[key])+":21\"" for key in energies_features)

for tag in RELEASE_TAG :
  PATHFILESIN = "/data2/user/ebrondol/HGCal/production/CMSSW_12_0_0_pre3/"+tag+"/"
  for i_label,i_sample in zip(SAMPLE_LABEL,SAMPLE_FILE):
    inputFolder = "{}/{}_{}_hgcalCenter/step4/".format(PATHFILESIN, i_sample, GENPRODUCER[i_sample])
    FILENAMES = ["DQM_V0001_R000000001__step4_"+i_sample+"__e"+key+"GeV__nopu.root" for key in energies_features]

    listFilein = ""
    for filein in FILENAMES:
      listFilein = listFilein + inputFolder + filein + " "

    for i_iter in ITERS :
      PATHFILESOUT = tag+"/"+i_sample+"_"+i_iter+"/"
      if not os.path.exists(PATHFILESOUT):
        os.makedirs(PATHFILESOUT)
  
      HISTOPREFIX = "\"DQMData/Run 1/HGCAL/Run summary/HGCalValidator/ticlTracksters"+i_iter+"/\""
      HISTONAMES = "\"trackster_energy\""
      AXISTITLES = "\";Regressed Energy;#Tracksters\""
      #AXISTITLES = "\";Raw Energy;#Tracksters\""
 
      final_label = "\"" + i_label + ", " + i_iter + " iter only"  + "\""
      command_plot = "python3 produce_plots_plotting_energy.py --filesin %s --folderout %s --histoprefix %s --histonames %s --varAxes %s --sample %s --features %s -v"%(listFilein,PATHFILESOUT,HISTOPREFIX,HISTONAMES,AXISTITLES,final_label,FEATURES)
  
      print(command_plot)
      os.system(command_plot)

