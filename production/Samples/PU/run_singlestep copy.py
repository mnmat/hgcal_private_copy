import sys
import os
import argparse
from subprocess import PIPE, CalledProcessError, Popen, check_call, check_output
import time
import random

start = time.time()

parser = argparse.ArgumentParser(description='Run step1, 2, 3 or 4 on several samples')
parser.add_argument('--folderin', type=str, help='Name of input folder (if any)')
parser.add_argument('--folderout', type=str, help='Name of output folder (if none is given, the input one is used)', default=None)
parser.add_argument('--sample', help="Data sample", choices=['singlepi', 'singlephoton', 'singleel', 'singleKaonL', 'singlemuon', 'all'], type=str, nargs='+')
parser.add_argument('--energies', help="Energies for each sample", choices=['10', '20', '50', '100'], type=str, nargs='+')
parser.add_argument('--etas', help = "Eta for each sample", choices = ['1.6', '1.7','2.1','2.5', '2.9', '1.7_2.7'], type=str, nargs='+')
parser.add_argument('--nevents', help = "Number of events", choices = ['1', '10', '100','500', '1000', '10000'], type=str, nargs='+')
parser.add_argument('--caps', help = "Position of endcap", choices = ['pos', 'neg'], type=str, nargs='+')
parser.add_argument('--step', help="Steps to run", choices=['step1', 'step2', 'step3', 'step4'], type=str)
parser.add_argument('--skip_existing', help="Skip command if file already exists", action='store_true')
parser.add_argument('--idx',help="Set file index",type=str,default="1")
parser.add_argument('--tag', help="Tag used in output folder", type=str, default='tag')
parser.add_argument('--mode', help='Run config with modifier', choices=['', 'clue3d', 'kf'], type=str, default='')
args = parser.parse_args()

# Settings

initialSeed = random.randint(1, 99999999)
TAG  = args.tag
samples = args.sample
energies = args.energies
etas = args.etas
nevents = args.nevents
caps = args.caps
idx = args.idx
if args.step == "all":
  steps = ["step1", "step2", "step3"]
else:
  steps = [args.step]

genProducer = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy", 'singlemuon': "flatEGun"}

for step in steps:
  if args.step == 'step1':
    log = 'log/'+TAG+'_'+args.step+'_'+sample+'_'+en+'GeV' + '_'+eta+'eta'+'_'+'z'+cap+'_'+'n'+nevent+'.log'
    #command = "cmsRun step1_%s.py %s %s %s %s %s %s >& %s &"%(genProducer[sample], en, eta, sample, nevent, cap, outFolder, log)
    command = "cmsRun step1_%s.py %s %s %s %s %s %s %i %s %i"%(genProducer[sample], en, eta, sample, nevent, cap, ".", 1, idx, initialSeed)
    print(command)
    p = check_output(command, shell=True)
  else:
    log = 'log/'+TAG+'_'+args.step+'_'+sample+'_'+en+'GeV' + '_'+eta+'eta'+'_'+'z'+cap+'_'+'n'+nevent+'.log'
    config_name = args.step
    if args.mode =='clue3d':
      config_name = args.step + "_clue3d"
    if args.mode == 'kf':
      config_name = args.step + "_kf"
    #command = "cmsRun %s.py %s %s %s %s %s %s %s >& %s &"%(config_name, en, eta, sample, nevent, sample, inFolder, outFolder, log)
    command = "cmsRun %s.py %s %s %s %s %s %s %s %i %s"%(config_name, en, eta, sample, nevent, cap, "./", "./",nthreads,idx)
    p = check_output(command, shell=True)


outFolder = "{}/z{}/n{}/Eta_{}/{}_{}_hgcalCenter/".format(args.folderout, cap, nevent,eta.replace('.',''), sample, genProducer[sample])

#xrdcp step2.root root://eosuser.cern.ch//eos/user/m/mmatthew/TICLv4Sample/CMSSW_13_X/TEST//step2/step2_$1_$2.root
#xrdcp step3.root root://eosuser.cern.ch//eos/user/m/mmatthew/TICLv4Sample/CMSSW_13_X/TEST//step3/step3_$1_$2.root

outFolder = "{}/z{}/n{}/Eta_{}/{}_{}_hgcalCenter/".format(args.folderout, cap, nevent,eta.replace('.',''), sample, genProducer[sample])
if os.path.exists(outFolder):
  mk
for step in steps:  
  tmpFolder = os.path.join(outFolder,step)
  if not os.path.isdir(tmpFolder):
    os.makedirs(tmpFolder)
  outfile  = "{}/{}_{}_e{}GeV_eta{}_z{}_events{}_nopu_{}.root".format(step,sample, en, eta.replace('.',''),cap,nevent,idx)
  output = "root://eosuser.cern.ch/%s/%s" %(tmpFolder, outFile)
  command = "xrdcp %s.root %s"%(step, output)
  p = check_output(command, shell = True)

print("Done in ", time.time()-start)