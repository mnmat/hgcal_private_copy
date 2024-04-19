# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --conditions auto:phase2_realistic_T15 -s DIGI:pdigi_valid,L1TrackTrigger,L1,DIGI2RAW,HLT:@fake2 --datatier GEN-SIM-DIGI-RAW -n 10 --geometry Extended2026D49 --era Phase2C9 --eventcontent FEVTDEBUGHLT --no_exec --filein file:step1.root --fileout file:step2.root
import FWCore.ParameterSet.Config as cms

import sys
import os, errno

# Get input variables
en_str = sys.argv[2]
eta_str = sys.argv[3].replace(".","")
nameprefix = sys.argv[4]
nevents = sys.argv[5]
caps = sys.argv[6]
infolder = sys.argv[7]
nthreads = int(sys.argv[9])
idx = str(sys.argv[10])

# Define input and output files
if idx != "none":
    infile_  = "file:{}/step1/step1_{}_e{}GeV_eta{}_z{}_events{}_nopu_{}.root".format(infolder, nameprefix, en_str, eta_str,caps,nevents,idx)
else:
    infile_  = "file:{}/step1/step1_{}_e{}GeV_eta{}_z{}_events{}_nopu.root".format(infolder, nameprefix, en_str, eta_str,caps,nevents)

outfolder = sys.argv[8]
print("Outfolder: ", outfolder)
outfolder = outfolder + '/step2/'

if not os.path.exists(outfolder):
   try:
      os.makedirs(outfolder)
   except OSError as e:
      if e.errno != errno.EEXIST:
         raise
   #os.makedirs(outfolder, exist_ok=True) # only in Python 3
if idx != "-1":
    outfile_  = "file:{}/step2_{}_e{}GeV_eta{}_z{}_events{}_nopu_{}.root".format(outfolder, nameprefix, en_str, eta_str,caps,nevents,idx)
else:
    outfile_  = "file:{}/step2_{}_e{}GeV_eta{}_z{}_events{}_nopu.root".format(outfolder, nameprefix, en_str, eta_str,caps,nevents)



from Configuration.Eras.Era_Phase2C17I13M9_cff import Phase2C17I13M9

process = cms.Process('HLT',Phase2C17I13M9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D98Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_75e33_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring(infile_),
    inputCommands = cms.untracked.vstring(
        'keep *', 
        'drop *_genParticles_*_*', 
        'drop *_genParticlesForJets_*_*', 
        'drop *_kt4GenJets_*_*', 
        'drop *_kt6GenJets_*_*', 
        'drop *_iterativeCone5GenJets_*_*', 
        'drop *_ak4GenJets_*_*', 
        'drop *_ak7GenJets_*_*', 
        'drop *_ak8GenJets_*_*', 
        'drop *_ak4GenJetsNoNu_*_*', 
        'drop *_ak8GenJetsNoNu_*_*', 
        'drop *_genCandidatesForMET_*_*', 
        'drop *_genParticlesForMETAllVisible_*_*', 
        'drop *_genMetCalo_*_*', 
        'drop *_genMetCaloAndNonPrompt_*_*', 
        'drop *_genMetTrue_*_*', 
        'drop *_genMetIC5GenJs_*_*'
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,    
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),    
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(nthreads),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(outfile_),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.mix.input.nbPileupEvents.averageNumber = cms.double(200.000000)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-3)
process.mix.maxBunch = cms.int32(3)
process.mix.input.fileNames = cms.untracked.vstring(['/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/019a855c-d70e-42f6-b953-550e83ded2c9.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/1e6ae6fd-8ac7-4eca-b727-3252ae4ff52f.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/313dfade-529e-4ae1-9f42-4813b8c83862.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/7d4ca041-1a5d-4580-b5fd-fedeb7c61e88.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/c04e329b-d890-4f57-8aeb-f9a671ae0312.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/d1e561ab-33b8-48d6-b721-f1651d821732.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/d83dc109-bd09-4049-a9ac-49c2f2d922b7.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/f20bedd8-3db8-4d04-a2ab-0360e175f3ad.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/f2ac7802-1364-45b1-b21d-f5f32f3bd20d.root'])
process.mix.digitizers = cms.PSet(process.theDigitizersValid)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T25', '')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.L1T_DoubleNNTau52 = cms.Path(process.HLTL1Sequence+process.hltL1DoubleNNTau52)
process.L1T_SingleNNTau150 = cms.Path(process.HLTL1Sequence+process.hltL1SingleNNTau150)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
# process.schedule imported from cff in HLTrigger.Configuration
process.schedule.insert(0, process.digitisation_step)
process.schedule.insert(1, process.L1TrackTrigger_step)
process.schedule.insert(2, process.L1simulation_step)
process.schedule.insert(3, process.digi2raw_step)

process.schedule.extend([process.endjob_step,process.FEVTDEBUGHLToutput_step])
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
