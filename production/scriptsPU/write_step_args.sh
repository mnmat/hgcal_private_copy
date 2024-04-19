#! bin/bash

# This script can be used to write .txt files containing arguments for the create_samples.sh executable for htcondor.
# It can also be used to split the total number of events into more manageable sizes to utilize parallelization.
# The arguments are eta, energy, number of events, and path to the input file

# Set input variables
step="$1"
cap="zpos"
root="/eos/cms/store/group/dpg_hgcal/comm_hgcal/mmatthew/PatternRecognitionByKalmanFilter/CMSSW_13_2_0_pre3/samples/200_PU"

#root="/eos/user/m/mmatthew/Data/KF/CMSSW_13_2_0_pre3/samplesPU"
particles="singlemuon"
producer="flatEGun"
position="hgcalCenter"
tevts=500 # Number of total events
fevts=100 # Number of events per file
end=$((tevts/fevts))

# Create txt file
f="tmp_"$step".txt"
rm $f
touch $f
txt=""

for eta in 1.6 1.7 2.1 2.3 2.5 2.7 2.9
do
    for energy in 10 20 50 100
    do
        for i in $(seq 1 $end)
        do
            if [ "$step" == "step1" ]
            then
                echo "$eta, $energy, $fevts, $i" >> $f
            elif [ "$step" == "step2" ]
            then
                tmp=$root"/"$cap"/n"$fevts"/Eta_"${eta:0:1}${eta:2:3}"/"$particles"_"$producer"_"$position"/step1/step1_"$particles"_e"$energy"GeV_eta"${eta:0:1}${eta:2:3}"_"$cap"_events"$fevts"_nopu_"$i".root"
                echo "$eta, $energy, $fevts, $i, $tmp" >>  $f 
            elif [ "$step" == "step3" ]
            then
                tmp=$root"/"$cap"/n"$fevts"/Eta_${eta:0:1}${eta:2:3}/singlemuon_flatEGun_hgcalCenter/step2/step2_singlemuon_e"$energy"GeV_eta"${eta:0:1}${eta:2:3}"_"$cap"_events"$fevts"_nopu_"$i".root"
                echo "$eta, $energy, $fevts, $i, $tmp" >>  $f 
            fi
        done
    done
done
