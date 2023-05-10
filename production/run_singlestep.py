import sys
import os
import argparse
from subprocess import PIPE, CalledProcessError, Popen, check_call, check_output
import time

start = time.time()

parser = argparse.ArgumentParser(description='Run step1, 2, 3 or 4 on several samples')
parser.add_argument('--folderin', type=str, help='Name of input folder (if any)')
parser.add_argument('--folderout', type=str, help='Name of output folder (if none is given, the input one is used)', default=None)
parser.add_argument('--sample', help="Data sample", choices=['singlepi', 'singlephoton', 'singleel', 'singleKaonL', 'singlemuon', 'all'], type=str, nargs='+')
parser.add_argument('--energies', help="Energies for each sample", choices=['10', '20', '50', '100','all'], type=str, nargs='+')
parser.add_argument('--etas', help = "Eta for each sample", choices = ['1.6', '1.7','2.1','2.5', '2.9', '1.7_2.7', 'all'], type=str, nargs='+')
parser.add_argument('--nevents', help = "Number of events", choices = ['1', '500', '1000', '10000', 'all'], type=str, nargs='+')
parser.add_argument('--caps', help = "Position of endcap", choices = ['pos', 'neg', 'all'], type=str, nargs='+')
parser.add_argument('--step', help="Steps to run", choices=['step1', 'step2', 'step3', 'step4'], type=str)
parser.add_argument('--skip_existing', help="Skip command if file already exists", action='store_true')
parser.add_argument('--nthreads',help="Set number of threads", type=str, default="1")
parser.add_argument('--idx',help="Set file index",type=str,default="1")
parser.add_argument('--tag', help="Tag used in output folder", type=str, default='tag')
parser.add_argument('--mode', help='Run config with modifier', choices=['', 'clue3d', 'kf'], type=str, default='')
parser.add_argument('--test', help='Print out the command only', action='store_true')
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
args = parser.parse_args()

VERBOSE = args.verbose
TEST = args.test
if TEST : VERBOSE = True
if VERBOSE : print(args)

TAG  = args.tag


samples = args.sample
if args.sample == ['all']:
  samples = ['singlepi', 'singlephoton', 'singleel', 'singleKaonL', 'singlemuon']

energies = args.energies
if args.energies == ['all']:
    energies = ['10', '20', '50', '100']

etas = args.etas
if args.etas == ['all']:
  etas = ['1.6', '1.7','2.1','2.5', '2.9']

nevents = args.nevents
if args.nevents == ['all']:
  nevents = ['1','500']

caps = args.caps
if args.caps == ['all']:
  caps = ['pos','neg']

print(args.nthreads)
nthreads = int(float(args.nthreads))
idx = args.idx


genProducer = {'singlephoton':"closeBy", 'singlepi':"flatEGun", 'singleel':"flatEGun", 'singleKaonL':"closeBy", 'singlemuon': "flatEGun"}
if not os.path.isdir(args.folderout):
  os.makedirs(args.folderout)
#errfile = open(args.folderout+'/'+'errors.txt','w')

if args.step == 'step1':
  if VERBOSE : print('running step1')
  for sample in samples:
    for eta in etas:
      for nevent in nevents:
        for cap in caps:
          outFolder = "{}/z{}/n{}/Eta_{}/{}_{}_hgcalCenter/".format(args.folderout, cap, nevent,eta.replace('.',''), sample, genProducer[sample])
          
          for en in energies:
            if idx != "none":
              outfile  = "{}/{}_{}_e{}GeV_eta{}_z{}_events{}_nopu_{}.root".format(args.step,args.step,sample, en, eta.replace('.',''),cap,nevent,idx)
            else:
              outfile  = "{}/{}_{}_e{}GeV_eta{}_z{}_events{}_nopu.root".format(args.step,args.step,sample, en, eta.replace('.',''),cap,nevent)

            if (args.skip_existing) and (os.path.exists(outFolder+outfile)):
              print("Skipped creating already existing ", outfile)
              continue
            log = 'log/'+TAG+'_'+args.step+'_'+sample+'_'+en+'GeV' + '_'+eta+'eta'+'_'+'z'+cap+'_'+'n'+nevent+'.log'
            #command = "cmsRun step1_%s.py %s %s %s %s %s %s >& %s &"%(genProducer[sample], en, eta, sample, nevent, cap, outFolder, log)
            command = "cmsRun step1_%s.py %s %s %s %s %s %s %i %s"%(genProducer[sample], en, eta, sample, nevent, cap, outFolder, nthreads,idx)

            print(command)
            if not TEST:
              try:
                #os.system(command)
                p = check_output(command, shell=True)
                #p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                #output, err = p.communicate()
              except CalledProcessError as e:
                # errfile.write(command)
                # errfile.write("\n")
                print(e.output)
else:
  if VERBOSE : print('running %s'%args.step)
  for sample in samples:
      for eta in etas:
        for nevent in nevents:
          for cap in caps:
            #inFolder = "{}/{}_{}_hgcalCenter/".format(args.folderin, sample, genProducer[sample])
            inFolder = "{}/z{}/n{}/Eta_{}/{}_{}_hgcalCenter/".format(args.folderin,cap,nevent,eta.replace('.',''),sample,genProducer[sample])
            if args.folderout is None:
              outFolder = inFolder
            else:
              outFolder = "{}/z{}/n{}/Eta_{}/{}_{}_hgcalCenter/".format(args.folderout,cap,nevent,eta.replace('.',''),sample,genProducer[sample])

            for en in energies:
              if idx != "none":
                outfile  = "/{}_{}_e{}GeV_eta{}_z{}_events{}_nopu_{}.root".format(args.step,sample, en, eta.replace('.',''),caps,nevents,idx)
              else:
                outfile  = "/{}_{}_e{}GeV_eta{}_z{}_events{}_nopu.root".format(args.step,sample, en, eta.replace('.',''),caps,nevents)

              if (args.skip_existing) and (os.path.exists(os.path.join(outFolder, outfile))):
                print("Skipped creating already existing ", outfile)
              log = 'log/'+TAG+'_'+args.step+'_'+sample+'_'+en+'GeV' + '_'+eta+'eta'+'_'+'z'+cap+'_'+'n'+nevent+'.log'
              config_name = args.step
              if args.mode =='clue3d':
                config_name = args.step + "_clue3d"
              if args.mode == 'kf':
                config_name = args.step + "_kf"
              #command = "cmsRun %s.py %s %s %s %s %s %s %s >& %s &"%(config_name, en, eta, sample, nevent, sample, inFolder, outFolder, log)
              command = "cmsRun %s.py %s %s %s %s %s %s %s %i %s"%(config_name, en, eta, sample, nevent, cap, inFolder, outFolder,nthreads,idx)

              if not TEST:
                try:
                  #os.system(command)
                  p = check_output(command, shell=True)
                  #p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                  #output, err = p.communicate()
                except CalledProcessError as e:
                  # errfile.write(command)
                  # errfile.write("\n")
                  print(e.output)
              else:
                print(command)


print("Done in ", time.time()-start)