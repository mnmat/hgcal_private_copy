#! /bin/bash

folderin='/eos/home-m/mmatthew/Data/KF/CMSSW_13_1_0_pre1/samples'
folderout='/eos/home-m/mmatthew/Data/KF/CMSSW_13_1_0_pre1/debugging/BoundaryCondition'

eta="$1"
en="$2"
nevents=1
idx="none"
step="step3"
nthreads="1"
if [ "$step" == "step3" ]
then
    python run_singlestep.py --folderin $folderin --folderout $folderout --sample singlemuon --energies $en --etas $eta --nevents $nevents --caps pos --nthreads $nthreads --idx $idx --step $step --mode kf --test
else
    python run_singlestep.py --folderin $folderin --folderout $folderout --sample singlemuon --energies $en --etas $eta --nevents $nevents --caps pos --nthreads $nthreads --idx $idx --step $step
fi
