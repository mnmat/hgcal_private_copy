#! bin/bash

# Set input variables

step="$1"
cap="zpos"
root="/eos/user/m/mmatthew/Data/KF/CMSSW_13_1_0_pre1/samples"
tevts=10000 # Number of total events
fevts=1000 # Number of events per file
end=$((tevts/fevts))

# Create txt file
f="tmp_"$step".txt"

rm $f
touch $f
txt=""

for eta in 1.6 1.7 2.1 2.5 2.9
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
                tmp=$root"/"$cap"/n"$fevts"/Eta_${eta:0:1}${eta:2:3}/singlemuon_flatEGun_hgcalCenter/step1/step1_singlemuon_e"$energy"GeV_eta"${eta:0:1}${eta:2:3}"_"$cap"_events"$fevts"_nopu_"$i".root"
                echo "$eta, $energy, $fevts, $i, $tmp" >>  $f 
            elif [ "$step" == "step3" ]
            then
                tmp=$root"/"$cap"/n"$fevts"/Eta_${eta:0:1}${eta:2:3}/singlemuon_flatEGun_hgcalCenter/step2/step2_singlemuon_e"$energy"GeV_eta"${eta:0:1}${eta:2:3}"_"$cap"_events"$fevts"_nopu_"$i".root"
                echo "$eta, $energy, $fevts, $i, $tmp" >>  $f 
            fi
        done
    done
done