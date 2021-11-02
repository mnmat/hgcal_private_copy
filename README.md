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
