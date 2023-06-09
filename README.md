# HGCAL_private

Collect of private plots for HGCal Software Reconstruction

## Production

You can produce 500 events of the following single particle samples:
- single photon 
- single neutral kaons
- single electrons
- single pions
The first two are produced using `CloseByParticleGunProducer` at the entrance of HGCal. The other two are produced using the `FlatRandomEGunProducer` module.

Check how to run the production of each single step (1,2,3 and 4) with:
```
cd production/
python run_singlestep.py -h
```

## Plotting

`python3` is necessary: `which root` and then `source PATH/TO/FOLDER/bin/thisroot.sh`

Check how to run the plotting of each performance (eff and energy) with:
```
python3 produce_plots_plotting_eff.py -h
```
Scrip[ts to run on multiple samples and energies in `run_*.py`

## HTCONDOR

To use run_singlestep.py on htcondor, one can use the scripts found in the scripts/ folder. Note that the .sub files require a textfile called tmp_step*.txt with the input arguments `eta`, `energy`, `number of events`, and `PATH/TO/FILE` to run. Those files can be created with `write_step_args.sh`. To send jobs to the worker nodes do the following:
```
cmsenv
cd scripts
condor_submit condor_step1.sub
```
To check the status of your job and remove jobs use
```
condor_q
condor_rm
```
