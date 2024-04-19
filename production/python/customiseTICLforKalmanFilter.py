# Validation
from Analyzers.EfficiencyAnalyzerDemo.EfficiencyAnalyzerDemo_cfi import *
from Analyzers.Ntuplizer.Ntuplizer_cfi import *

def customiseTICLForKalmanFilterMetricAnalyzer(process):
    
    # Validation Metrics
    process.kfAnalyzer = efficiencyAnalyzerDemo.clone()
    process.TFileService = cms.Service("TFileService",
                                       fileName=cms.string("histo.root")
                                       )    
    process.FEVTDEBUGHLToutput_step = cms.EndPath(
        process.FEVTDEBUGHLToutput + process.kfAnalyzer)
    return process

def customiseTICLForKalmanFilterNtuplizer(process):
    
    process.kfNtuplizer = ntuplizer.clone()
    process.FEVTDEBUGHLToutput_step = cms.EndPath(
        process.FEVTDEBUGHLToutput + process.kfNtuplizer)

    return process

