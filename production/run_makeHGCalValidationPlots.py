import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Produce root files with tracking analysis plots')
parser.add_argument('--folderin', type=str, help='Name of input folder')
parser.add_argument('--folderout', type=str, help='Name of output folder', default="~/www_eos/HGCal/png/")
parser.add_argument('--sample', help="Data sample", choices=['singlepi', 'singlephoton', 'singleel', 'singleKaonL', 'all'], type=str, nargs='+')
parser.add_argument('--energies', help="Energies for each sample", choices=['10', '20', '50', '100', '200', '300', 'all'], type=str, nargs='+')
parser.add_argument('--tag',type=str, help='Tag used in output log file and sub-folder')
parser.add_argument('--test', help='Print out the command only', action='store_true')
parser.add_argument('--separate', help='Produce separate plots', action='store_true')
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
args = parser.parse_args()

SAMPLES = args.sample
if args.sample == ['all']:
  SAMPLES = ['singlepi', 'singlephoton', 'singleel', 'singleKaonL']

genProducer = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy"}

ENERGIES = args.energies
if args.energies == ['all']:
  ENERGIES = ['10', '20', '50', '100', '200', '300']

VERBOSE = args.verbose
TEST = args.test
if TEST : VERBOSE = True
if VERBOSE : print(args)

PATHIN  = args.folderin+'/'
PATHOUT = args.folderout+'/'
TAG  = args.tag

def create_command(folderin, folderout, sample, tag):
  final_folderin  = "{}/{}_{}_hgcalCenter/step4/".format(folderin, sample, genProducer[sample])
  final_folderout = folderout + "/" + sample
  log = 'log/'+tag+'_makeHGCalValidationPlots_'+sample+'.log'

  filesin = ""
  for en in ENERGIES : 
    filesin += final_folderin+'/DQM_V0001_R000000001__step4_'+sample+'__e'+en+'GeV__nopu.root '

  #command = 'makeHGCalValidationPlots.py '+filesin+' -o '+final_folder+' --png --collection all'
  command = 'makeHGCalValidationPlots.py '+filesin+' -o '+final_folderout+' --png --collection tracksters'
  if args.separate : 
    command += ' --separate '
  command += ' >& '+log+' &'

  if VERBOSE: print(command)

  return command

for sample in SAMPLES:
  command = create_command(PATHIN, PATHOUT, sample, TAG)
  if not TEST:
    os.system(command)

