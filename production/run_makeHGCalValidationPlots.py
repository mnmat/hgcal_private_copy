import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Produce root files with tracking analysis plots')
parser.add_argument('--folderin', type=str, help='Name of input folder')
parser.add_argument('--folderout', type=str, help='Name of output folder', default="~/www_eos/HGCal/HGCDoublet_validation/20201012_EMTrackSeeded/png/newFolder")
parser.add_argument('--sample', help="Data sample", type=str, choices=["pions", "kaons", "electrons", "photons", "all"])
parser.add_argument('--label',type=str, help='Label used in output log file and sub-folder')
parser.add_argument('--test', help='Print out the command only', action='store_true')
parser.add_argument('--separate', help='Produce separate plots', action='store_true')
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
args = parser.parse_args()

LABEL = args.label

pions = False
electrons = False
photons = False
print(args.sample)

PATHIN = args.folderin+'/'
TEST = args.test

#singleKaonL_closeBy_hgcalCenter/ singleel_flatEGun_hgcalCenter/    singlephoton_closeBy_hgcalCenter/ singlepi_flatEGun_hgcalCenter/    

def create_command(filesin, folderout, sample, label):
  final_folder = folderout + "/" + sample
  log = label+"_"+sample+'.log'
  #command = 'makeHGCalValidationPlots.py '+filesin+' -o '+final_folder+' --png --collection all'
  command = 'makeHGCalValidationPlots.py '+filesin+' -o '+final_folder+' --png --collection allTiclMultiClusters'
  if args.separate : 
    command += ' --separate '
  command += ' >& '+log+' &'
  return command

energies = ['10','20','50','100','200','300']

# kaons
if (args.sample == "kaons") or (args.sample == "all") :
  SAMPLES = ['singleKaonL__e'+en+'GeV__nopu' for en in energies]
  FILESIN = ""
  for SAMPLE in SAMPLES : 
    FILESIN += PATHIN+'/singleKaonL_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_'+SAMPLE+'.root '
  command = create_command(FILESIN, args.folderout, "singleKaonL", args.label)
  print(command)
  if not TEST:
    os.system(command)

# photons
if (args.sample == "photons") or (args.sample == "all") :
  SAMPLES = ['singlephoton__e'+en+'GeV__nopu' for en in energies]
  FILESIN = ""
  for SAMPLE in SAMPLES : 
    FILESIN += PATHIN+'/singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_'+SAMPLE+'.root '
  command = create_command(FILESIN, args.folderout, "singlephoton", args.label)
  print(command)
  if not TEST:
    os.system(command)

# pions
if (args.sample == "pions") or (args.sample == "all") :
  SAMPLES = ['singlepi__e'+en+'GeV__nopu' for en in energies]
  FILESIN = ""
  for SAMPLE in SAMPLES : 
    FILESIN += PATHIN+'/singlepi_flatEGun_hgcalCenter/step4/DQM_V0001_R000000001__step4_'+SAMPLE+'.root '
  command = create_command(FILESIN, args.folderout, "singlepi", args.label)
  print(command)
  if not TEST:
    os.system(command)

# electrons
if (args.sample == "electrons") or (args.sample == "all") :
  SAMPLES = ['singleel__e'+en+'GeV__nopu' for en in energies]
  FILESIN = ""
  for SAMPLE in SAMPLES : 
    FILESIN += PATHIN+'/singleel_flatEGun_hgcalCenter/step4/DQM_V0001_R000000001__step4_'+SAMPLE+'.root '
  command = create_command(FILESIN, args.folderout, "singleel", args.label)
  print(command)
  if not TEST:
    os.system(command)
