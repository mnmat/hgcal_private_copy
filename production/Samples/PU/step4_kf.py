# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step4 --conditions auto:phase2_realistic_T15 -s HARVESTING:@phase2Validation+@phase2+@miniAODValidation+@miniAODDQM --scenario pp --filetype DQM --geometry Extended2026D49 --era Phase2C9 --mc -n 100 --no_exec --filein file:step3_inDQM.root --fileout file:step4.root
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
outfolder = sys.argv[8]
nthreads = int(sys.argv[9])
idx = str(sys.argv[10])

# Define input and output files
if idx != "none":
    infile_  = "file:{}/step3/step3_{}_e{}GeV_eta{}_z{}_events{}_nopu_{}.root".format(infolder, nameprefix, en_str, eta_str,caps,nevents,idx)
else:
    infile_  = "file:{}/step3/step3_{}_e{}GeV_eta{}_z{}_events{}_nopu.root".format(infolder, nameprefix, en_str, eta_str,caps,nevents)

outfolder = outfolder + '/step4/'

if not os.path.exists(outfolder):
   try:
      os.makedirs(outfolder)
   except OSError as e:
      if e.errno != errno.EEXIST:
         raise
   #os.makedirs(outfolder, exist_ok=True) # only in Python 3
if idx != "none":
    outfile_  = "file:{}/step4_{}_e{}GeV_eta{}_z{}_events{}_nopu_{}.root".format(outfolder, nameprefix, en_str, eta_str,caps,nevents,idx)
else:
    outfile_  = "file:{}/step4_{}_e{}GeV_eta{}_z{}_events{}_nopu.root".format(outfolder, nameprefix, en_str, eta_str,caps,nevents)


outfileDQM_ = outfile_.replace(".root","_inDQM.root")

from Configuration.Eras.Era_Phase2C17I13M9_cff import Phase2C17I13M9

process = cms.Process('HARVESTING',Phase2C17I13M9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D98Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.DQMSaverAtRunEnd_cff')
process.load('Configuration.StandardSequences.Harvesting_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.dqmSaver.dirName = outfolder
process.dqmSaver.workflow = cms.untracked.string('/step4_{}/e{}GeV/nopu'.format(nameprefix, en_str))

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)
process.MessageLogger.cerr.FwkReport.reportEvery = 100

# Input source
process.source = cms.Source("DQMRootSource",
    fileNames = cms.untracked.vstring(infile_)
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring('ProductNotFound'),
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
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step4 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
process.mix.input.nbPileupEvents.averageNumber = cms.double(200.000000)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-3)
process.mix.maxBunch = cms.int32(3)
process.mix.input.fileNames = cms.untracked.vstring(['/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/019a855c-d70e-42f6-b953-550e83ded2c9.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/1e6ae6fd-8ac7-4eca-b727-3252ae4ff52f.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/313dfade-529e-4ae1-9f42-4813b8c83862.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/7d4ca041-1a5d-4580-b5fd-fedeb7c61e88.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/c04e329b-d890-4f57-8aeb-f9a671ae0312.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/d1e561ab-33b8-48d6-b721-f1651d821732.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/d83dc109-bd09-4049-a9ac-49c2f2d922b7.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/f20bedd8-3db8-4d04-a2ab-0360e175f3ad.root', '/store/relval/CMSSW_13_2_0_pre1/RelValMinBias_14TeV/GEN-SIM/131X_mcRun4_realistic_v5_2026D98noPU-v1/2590000/f2ac7802-1364-45b1-b21d-f5f32f3bd20d.root'])
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T25', '')

# Path and EndPath definitions
process.alcaHarvesting = cms.Path()
process.dqmHarvesting = cms.Path(process.DQMOffline_SecondStep+process.DQMOffline_Certification)
process.dqmHarvestingExpress = cms.Path(process.DQMOffline_SecondStep_Express)
process.dqmHarvestingExtraHLT = cms.Path(process.DQMOffline_SecondStep_ExtraHLT+process.DQMOffline_Certification)
process.dqmHarvestingFakeHLT = cms.Path(process.DQMOffline_SecondStep_FakeHLT+process.DQMOffline_Certification)
process.dqmHarvestingPOGMC = cms.Path(process.DQMOffline_SecondStep_PrePOGMC)
process.genHarvesting = cms.Path(process.postValidation_gen)
process.validationHarvestingFS = cms.Path(process.recoMuonPostProcessors+process.postValidationTracking+process.MuIsoValPostProcessor+process.calotowersPostProcessor+process.hcalSimHitsPostProcessor+process.hcaldigisPostProcessor+process.hcalrechitsPostProcessor+process.electronPostValidationSequence+process.photonPostProcessor+process.pfJetClient+process.pfMETClient+process.pfJetResClient+process.pfElectronClient+process.rpcRecHitPostValidation_step+process.makeBetterPlots+process.bTagCollectorSequenceMCbcl+process.METPostProcessor+process.L1GenPostProcessor+process.bdHadronTrackPostProcessor+process.MuonCSCDigisPostProcessors+process.MuonGEMHitsPostProcessors+process.MuonGEMDigisPostProcessors+process.MuonGEMRecHitsPostProcessors+process.hgcalPostProcessor+process.trackerphase2ValidationHarvesting+process.postValidation_gen)
process.validationHarvestingHI = cms.Path(process.postValidationHI)
process.validationHarvestingNoHLT = cms.Path(process.postValidation+process.postValidation_gen)
process.validationHarvestingPhase2 = cms.Path(process.hltpostvalidation)
process.validationpreprodHarvesting = cms.Path(process.postValidation_preprod+process.hltpostvalidation_preprod+process.postValidation_gen)
process.validationpreprodHarvestingNoHLT = cms.Path(process.postValidation_preprod+process.postValidation_gen)
process.validationprodHarvesting = cms.Path(process.hltpostvalidation_prod+process.postValidation_gen)
process.postValidation_common_step = cms.Path(process.postValidation_common)
process.postValidationTracking_step = cms.Path(process.postValidationTracking)
process.postValidation_muons_step = cms.Path(process.postValidation_muons)
process.postValidation_JetMET_step = cms.Path(process.postValidation_JetMET)
process.electronPostValidationSequence_step = cms.Path(process.electronPostValidationSequence)
process.photonPostProcessor_step = cms.Path(process.photonPostProcessor)
process.bTagCollectorSequenceMCbcl_step = cms.Path(process.bTagCollectorSequenceMCbcl)
process.runTauEff_step = cms.Path(process.runTauEff)
process.postValidation_HCAL_step = cms.Path(process.postValidation_HCAL)
process.hgcalValidatorPostProcessor_step = cms.Path(process.hgcalValidatorPostProcessor)
process.mtdValidationPostProcessor_step = cms.Path(process.mtdValidationPostProcessor)
process.postValidationOuterTracker_step = cms.Path(process.postValidationOuterTracker)
process.trackerphase2ValidationHarvesting_step = cms.Path(process.trackerphase2ValidationHarvesting)
process.DQMHarvestTracking_step = cms.Path(process.DQMHarvestTracking)
process.DQMHarvestOuterTracker_step = cms.Path(process.DQMHarvestOuterTracker)
process.DQMHarvestTrackerPhase2_step = cms.Path(process.DQMHarvestTrackerPhase2)
process.DQMHarvestMuon_step = cms.Path(process.DQMHarvestMuon)
process.DQMCertMuon_step = cms.Path(process.DQMCertMuon)
process.DQMHarvestHcal_step = cms.Path(process.DQMHarvestHcal)
process.DQMHarvestHcal2_step = cms.Path(process.DQMHarvestHcal2)
process.DQMHarvestEGamma_step = cms.Path(process.DQMHarvestEGamma)
process.DQMCertEGamma_step = cms.Path(process.DQMCertEGamma)
process.DQMHarvestL1TPhase2_step = cms.Path(process.DQMHarvestL1TPhase2)
process.DQMHarvestMiniAOD_step = cms.Path(process.DQMHarvestMiniAOD)
process.dqmsave_step = cms.Path(process.DQMSaver)

# Schedule definition
process.schedule = cms.Schedule(process.postValidation_common_step,process.postValidationTracking_step,process.postValidation_muons_step,process.postValidation_JetMET_step,process.electronPostValidationSequence_step,process.photonPostProcessor_step,process.bTagCollectorSequenceMCbcl_step,process.runTauEff_step,process.postValidation_HCAL_step,process.hgcalValidatorPostProcessor_step,process.mtdValidationPostProcessor_step,process.postValidationOuterTracker_step,process.trackerphase2ValidationHarvesting_step,process.validationHarvesting,process.DQMHarvestTracking_step,process.DQMHarvestOuterTracker_step,process.DQMHarvestTrackerPhase2_step,process.DQMHarvestMuon_step,process.DQMCertMuon_step,process.DQMHarvestHcal_step,process.DQMHarvestHcal2_step,process.DQMHarvestEGamma_step,process.DQMCertEGamma_step,process.DQMHarvestL1TPhase2_step,process.validationHarvestingMiniAOD,process.DQMHarvestMiniAOD_step,process.dqmsave_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
