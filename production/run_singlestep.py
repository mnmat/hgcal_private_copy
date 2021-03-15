import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Run step3 or 4 on several samples')
parser.add_argument('--sample', help="Data sample", choices=['singlepi', 'singlephoton', 'singleel', 'singleKaonL', 'all'], type=str, nargs='+')
parser.add_argument('--energies', help="Energies for each sample", choices=['10', '20', '50', '100', '200', '300', 'all'], type=str, nargs='+')
parser.add_argument('--step', help="Steps to run", choices=['step1', 'step2', 'step3', 'step4'], type=str)
parser.add_argument('--tag', help="Tag used in output folder", type=str, default='tag')
parser.add_argument('--test', help='Print out the command only', action='store_true')
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
args = parser.parse_args()

VERBOSE = args.verbose
if VERBOSE : print(args)

TEST = args.test

samples = args.sample
if args.sample == ['all']:
  samples = ['singlepi', 'singlephoton', 'singleel', 'singleKaonL']

energies = args.energies
if args.energies == ['all']:
  energies = ['10', '20', '50', '100', '200', '300']

genProducer = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy"}
folder = '/data2/user/ebrondol/HGCal/production/'+args.tag+'/CMSSW_11_3_0_pre4/'

if args.step == 'step1':
  if VERBOSE : print('running step1')
  for sample in samples:
    outputFolder = "{}/{}_{}_hgcalCenter/".format(folder, sample, genProducer[sample])
    for en in energies:
      command = "cmsRun step1_%s.py %s %s %s >& log_%s_%s_%sGeV.log &"%(genProducer[sample], en, sample, outputFolder, args.step, sample, en)
      print(command)
      if not TEST:
        os.system(command)

if args.step == 'step2':
  if VERBOSE : print('running step2')
  for sample in samples:
    outputFolder = "{}/{}_{}_hgcalCenter/".format(folder, sample, genProducer[sample])
    for en in energies:
      command = "cmsRun step2.py %s %s %s >& log_%s_%s_%sGeV.log &"%(en, sample, outputFolder, args.step, sample, en)
      print(command)
      if not TEST:
        os.system(command)

if args.step == 'step3':
  if VERBOSE : print('running step3')
  for sample in samples:
    outputFolder = "{}/{}_{}_hgcalCenter/".format(folder, sample, genProducer[sample])
    for en in energies:
      command = "cmsRun step3.py %s %s %s >& log_%s_%s_%sGeV.log &"%(en, sample, outputFolder, args.step, sample, en)
      print(command)
      if not TEST:
        os.system(command)

if args.step == 'step4':
  if VERBOSE : print('running step4')
  for sample in samples:
    outputFolder = "{}/{}_{}_hgcalCenter/".format(folder, sample, genProducer[sample])
    for en in energies:
      command = "cmsRun step4.py %s %s %s >& log_%s_%s_%sGeV.log &"%(en, sample, outputFolder, args.step, sample, en)
      print(command)
      if not TEST:
        os.system(command)

