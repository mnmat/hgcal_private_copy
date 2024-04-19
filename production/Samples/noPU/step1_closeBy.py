# Last update with 12_0_1_pre4
# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: CloseByParticle_Photon_ERZRanges_cfi --conditions auto:phase2_realistic_T15 -n 10 --era Phase2C9 --eventcontent FEVTDEBUG --relval 9000,100 -s GEN,SIM --datatier GEN-SIM --beamspot HLLHC --geometry Extended2026D49 --no_exec --fileout file:step1.root
import FWCore.ParameterSet.Config as cms

import sys, os, errno

nevents = sys.argv[5]
caps = sys.argv[6]

en_str = sys.argv[2]
en = float(en_str)
en_min = float(en-0.01)
en_max = float(en+0.01)
nameprefix = sys.argv[4]

eta_str = sys.argv[3]
eta = float(eta_str)

if caps =="neg": eta = -eta 
elif caps!="pos":
    raise Exception('%s is an invalid keyword argument for the z position. Should be either "pos" or "neg".'%caps)

eta_min = eta - 0.00001
eta_max = eta + 0.00001
eta_str = eta_str.replace(".","")

if "pho" in nameprefix :
  part_id = 22
elif "Kaon" in nameprefix :
  part_id = 130
else:
  print('no part id valid')
  sys.exit() 

print ("partId=", part_id, "en=", en, " nameprefix=", nameprefix)

folder = sys.argv[7]
outfolder = folder + '/step1/'
if not os.path.exists(outfolder):
   try:
      os.makedirs(outfolder)
   except OSError as e:
      if e.errno != errno.EEXIST:
         raise
   #os.makedirs(outfolder, exist_ok=True) # only in Python 3
outfile_  = "file:{}/step1_{}_e{}GeV_eta{}_z{}_events{}_nopu.root".format(outfolder, nameprefix, en_str, eta_str,caps,nevents)

from Configuration.Eras.Era_Phase2C9_cff import Phase2C9

process = cms.Process('SIM',Phase2C9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedHGCALCloseBy_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(nevents),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
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
    annotation = cms.untracked.string('CloseByParticle_Photon_ERZRanges_cfi nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(outfile_),
    outputCommands = process.FEVTDEBUGEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T15', '')

process.generator = cms.EDProducer("CloseByParticleGunProducer",
    AddAntiParticle = cms.bool(False),
    PGunParameters = cms.PSet(
        Delta = cms.double(10),
        EnMax = cms.double(en_max),
        EnMin = cms.double(en_min),
        MaxEta = cms.double(eta_max),
        MaxPhi = cms.double(3.14159265359),
        MinEta = cms.double(eta_min),
        MinPhi = cms.double(-3.14159265359),
        NParticles = cms.int32(1),
        Overlapping = cms.bool(False),
        PartID = cms.vint32(int(part_id)),
        Pointing = cms.bool(True),
        RMax = cms.double(120), #HGC min = 60.
        RMin = cms.double(60), #HGC max = 120
        RandomShoot = cms.bool(False),
        ZMax = cms.double(321), #HGC max = 650
        ZMin = cms.double(320) #HGC min = 320
    ),
    Verbosity = cms.untracked.int32(0),
    firstRun = cms.untracked.uint32(1),
    psethack = cms.string('random particles in phi and r windows')
)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGoutput_step = cms.EndPath(process.FEVTDEBUGoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.endjob_step,process.FEVTDEBUGoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path).insert(0, process.generator)



# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
