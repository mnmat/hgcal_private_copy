#! /bin/bash


#folderin='/eos/home-m/mmatthew/Data/debug_samples/LocalError'
#folderin='/afs/cern.ch/user/m/mmatthew/CMSSW_12_3_0_pre5/src/hgcal_private/production/test_htcondor/'
#folderin='/eos/user/m/mmatthew/Data/samples/'
#folderout='/eos/home-m/mmatthew/Data/KF/MaterialBudget/RadXi/1_75'
folderin='/eos/home-m/mmatthew/Data/KF/CMSSW_13_1_0_pre1/samples'
folderout='/eos/home-m/mmatthew/Data/KF/CMSSW_13_1_0_pre1/samples'
#folderout='/eos/home-m/mmatthew/Data/KF/CMSSW_13_1_0_pre1/materialbudget/massweighted'
#folderout='/eos/home-m/mmatthew/Data/KF/CMSSW_13_1_0_pre1/materialbudget/zero'
#folderout='/eos/user/m/mmatthew/Data/KF/CMSSW_13_1_0_pre1/Analyzer/UpdatorStudies'
#folderout='/eos/user/m/mmatthew/Data/debug_samples/ReduceSize/'

#folderout='/afs/cern.ch/user/m/mmatthew/CMSSW_12_3_0_pre5/src/hgcal_private/production/test_htcondor'
eta="$1"
en="$2"
nevents="$3"
idx="$4"
step="$5"
nthreads="1"
if [ "$step" == "step3" ]
then
    python run_singlestep.py --folderin $folderin --folderout $folderout --sample singlemuon --energies $en --etas $eta --nevents $nevents --caps pos --nthreads $nthreads --idx $idx --step $step --mode kf
else
    python run_singlestep.py --folderin $folderin --folderout $folderout --sample singlemuon --energies $en --etas $eta --nevents $nevents --caps pos --nthreads $nthreads --idx $idx --step $step
fi
