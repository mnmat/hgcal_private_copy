import os
from collections import OrderedDict

#SAMPLE_LABEL = ["Single-#gamma", "Single-#pi^{#pm}", "Single-e^{#pm}", "Single-K^{0}_{L}"]
#SAMPLES = ["singlephoton", "singlepi", "singleel", "singleKaonL"]
SAMPLE_LABEL = ["\"Single-#gamma, PU = 0\""]
SAMPLES = ["singlephoton"]
GENPRODUCER = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy"}

RELEASE_TAG = ["clue3D"]
#RELEASE_TAG = ["vanilla"]

PATHFILESIN = "/data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/clue3D/"
#PATHFILESIN = "/data2/user/ebrondol/HGCal/production/CMSSW_12_0_0_pre3/vanilla/"

energies_features = [[10,94,20], [20,51,5], [50,54,26], [100,64,22], [200,99,3], [300,57,23]]
EN_FEATURES = ' '.join("\""+str(key[0])+" GeV:"+str(key[1])+":"+str(key[2])+"\"" for key in energies_features)

iter_features = [["Merge","Merge",94,20], ["CLUE3DHigh","CLUE3DHigh",51,5], ["CLUE3DLow","CLUE3DLow",54,26], ["TrkEM","TrkEM",64,22], ["EM","EM",99,3], ["TrkHAD","Trk",57,23], ["HAD","HAD", 30,4]]
ITER_FEATURES = ' '.join("\""+str(key[0])+":ticlTracksters"+str(key[1])+":"+str(key[2])+":"+str(key[3])+"\"" for key in iter_features)

print(EN_FEATURES)
print(ITER_FEATURES)
for tag in RELEASE_TAG :

  for i_label,i_sample in zip(SAMPLE_LABEL,SAMPLES):
    inputFolder = "{}/{}_{}_hgcalCenter/step4/".format(PATHFILESIN, i_sample, GENPRODUCER[i_sample])
    FILENAMES = ["DQM_V0001_R000000001__step4_"+i_sample+"__e"+str(key[0])+"GeV__nopu.root" for key in energies_features]

    listFilein = ""
    for filein in FILENAMES:
      listFilein = listFilein + inputFolder + filein + " "

    PATHFILESOUT = tag+"/"+i_sample+"/"
    if not os.path.exists(PATHFILESOUT):
      os.makedirs(PATHFILESOUT)

    command_plot = "python3 plotting_eff.py --filesin %s --folderout %s --sample %s --features %s --iter %s -v"%(listFilein, PATHFILESOUT, i_label, EN_FEATURES, ITER_FEATURES)

    print(command_plot)
    os.system(command_plot)

