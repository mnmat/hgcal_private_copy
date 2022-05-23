import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Run step1, 2, 3 or 4 on several samples')
parser.add_argument('--folderin', type=str, help='Name of input folder (if any)')
parser.add_argument('--folderout', type=str, help='Name of output folder (if none is given, the input one is used)', default=None)
parser.add_argument('--sample', help="Data sample", choices=['singlepi', 'singlephoton', 'singleel', 'singleKaonL', 'singlemuon', 'all'], type=str, nargs='+')
parser.add_argument('--energies', help="Energies for each sample", choices=['10', '20', '50', '100', '200', '300', 'all'], type=str, nargs='+')
parser.add_argument('--step', help="Steps to run", choices=['step1', 'step2', 'step3', 'step4'], type=str)
parser.add_argument('--tag', help="Tag used in output folder", type=str, default='tag')
parser.add_argument('--clue3d', help='Run config with clue3d modifier', action='store_true')
parser.add_argument('--test', help='Print out the command only', action='store_true')
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
args = parser.parse_args()

VERBOSE = args.verbose
TEST = args.test
CLUE3D = args.clue3d
if TEST : VERBOSE = True
if VERBOSE : print(args)

TAG  = args.tag

samples = args.sample
if args.sample == ['all']:
  samples = ['singlepi', 'singlephoton', 'singleel', 'singleKaonL', 'singlemuon']

energies = args.energies
if args.energies == ['all']:
  energies = ['10', '20', '50', '100', '200', '300']

genProducer = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy", 'singlemuon': "flatEGun"}

if args.step == 'step1':
  if VERBOSE : print('running step1')
  for sample in samples:
    outFolder = "{}/{}_{}_hgcalCenter/".format(args.folderout, sample, genProducer[sample])
    for en in energies:
      log = 'log/'+TAG+'_'+args.step+'_'+sample+'_'+en+'GeV.log'
      command = "cmsRun step1_%s.py %s %s %s >& %s &"%(genProducer[sample], en, sample, outFolder, log)
      print(command)
      if not TEST:
        os.system(command)
else:
  if VERBOSE : print('running %s'%args.step)
  for sample in samples:
    inFolder = "{}/{}_{}_hgcalCenter/".format(args.folderin, sample, genProducer[sample])
    if args.folderout is None:
      outFolder = inFolder
    else:
      outFolder = "{}/{}_{}_hgcalCenter/".format(args.folderout, sample, genProducer[sample])
    for en in energies:
      log = 'log/'+TAG+'_'+args.step+'_'+sample+'_'+en+'GeV.log'
      config_name = args.step
      if CLUE3D :
        config_name = args.step + "_clue3d"
      command = "cmsRun %s.py %s %s %s %s >& %s &"%(config_name, en, sample, inFolder, outFolder, log)
      print(command)
      if not TEST:
        os.system(command)

