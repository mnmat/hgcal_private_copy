import os
from collections import OrderedDict
import argparse

parser = argparse.ArgumentParser(description='Run step1, 2, 3 or 4 on several samples')
parser.add_argument('--test', help='Print out the command only', action='store_true')
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
args = parser.parse_args()

VERBOSE = args.verbose
TEST = args.test

SAMPLE_LABEL = ["\"Single-#gamma, PU = 0\"", "\"Single-#pi^{#pm}, PU = 0\"", "\"Single-e^{#pm}, PU = 0\"", "\"Single-K^{0}_{L}, PU = 0\""]
SAMPLES = ["singlephoton", "singlepi", "singleel", "singleKaonL"]
GENPRODUCER = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy"}

RELEASE_TAG = ["clue3D"]

energies_features = [[10,94,20], [20,51,5], [50,54,26], [100,64,22], [200,99,3], [300,57,23]]
EN_FEATURES = ' '.join("\""+str(key[0])+" GeV:"+str(key[1])+":"+str(key[2])+"\"" for key in energies_features)

iter_features = [["Merge","Merge",94,20], ["CLUE3DHigh","CLUE3DHigh",51,5], ["CLUE3DLow","CLUE3DLow",54,26], ["TrkEM","TrkEM",64,22], ["EM","EM",99,3], ["TrkHAD","Trk",57,23], ["HAD","HAD", 30,4]]
ITER_FEATURES = ' '.join("\""+str(key[0])+":ticlTracksters"+str(key[1])+":"+str(key[2])+":"+str(key[3])+"\"" for key in iter_features)

for tag in RELEASE_TAG :
  PATHFILESIN = "/data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/"+tag+"/"
  for i_label,i_sample in zip(SAMPLE_LABEL,SAMPLES):
    inputFolder = "{}/{}_{}_hgcalCenter/step4/".format(PATHFILESIN, i_sample, GENPRODUCER[i_sample])
    FILENAMES = ["DQM_V0001_R000000001__step4_"+i_sample+"__e"+str(key[0])+"GeV__nopu.root" for key in energies_features]

    listFilein = ""
    for filein in FILENAMES:
      listFilein = listFilein + inputFolder + filein + " "

    PATHFILESOUT = tag+"/"+i_sample+"/"
    if not os.path.exists(PATHFILESOUT):
      os.makedirs(PATHFILESOUT)
  
    HISTONAMES = "\"trackster_energy\""
    AXISTITLES = "\";Regressed Energy;#Tracksters\""
    #AXISTITLES = "\";Raw Energy;#Tracksters\""
 
    command_plot = "python3 plotting_energy.py --filesin %s --folderout %s --histonames %s --varAxes %s --sample %s --features %s --iter %s"%(listFilein,PATHFILESOUT,HISTONAMES,AXISTITLES,i_label,EN_FEATURES, ITER_FEATURES)
    if VERBOSE or TEST:
      command_plot = command_plot + " -v"
      print(command_plot)

    if not TEST:
        os.system(command_plot)

