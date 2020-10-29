# Command
# python produce_plots_plotting_layers.py --filesin /home/ericabro/ericabro_cernbox/HGCal_Software/EMTrackSeeded/after_60c3c21/DQM_V0001_R000000001__step4_singlepi__e100GeV__nopu.root /home/ericabro/ericabro_cernbox/HGCal_Software/EMTrackSeeded/after_60c3c21/DQM_V0001_R000000001__step4_singlephoton__e100GeV__nopu.root --folderout plots/ -v --varAxes ";First Layer Number;#Tracksters" --features "pions, E = 100 GeV:4:22" "photons, E = 100 GeV:2:21"

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, TFile, TCanvas, TGraph, TLegend, gPad, TLatex
import json
import argparse

def list_with_negatives(value):
  values = value.split(" ")
  print(values)
  return values

gROOT.Macro("CLICdpStyle.C") 
parser = argparse.ArgumentParser(description='Produce root files with tracking analysis plots')
parser.add_argument('--filesin', nargs='+', help='List of root file used as input')
parser.add_argument('--features', nargs='+', help='List of features used for this input file as label:color:markerStyle (ex. "p_{T} = 1 GeV:1:20:False")')
parser.add_argument('--folderout', help='Name of output folder')
#parser.add_argument('--histonames', nargs='+', help='Name of histos to plot (ex. eff_vs_theta eff_vs_phi)')
parser.add_argument('--varAxes', nargs='+', help='Name of axes in histos (ex. ";#theta [#circ];Tracking efficiency" ";#phi [#circ];Tracking efficiency")')
#parser.add_argument('--logXaxis', nargs='+', help='Bool to set log of X axes in histos')
#parser.add_argument('--logYaxis', nargs='+', help='Bool to set log of Y axes in histos')
#parser.add_argument('--rangeYaxis', nargs='+', help='Range Y axis (ex. =\"min:max\")', type=list_with_negatives, action='store')
#parser.add_argument('--rangeXaxis', nargs='+', help='Range X axis (ex. =\"min:max\")', type=list_with_negatives, action='store')
#parser.add_argument('--sample', help="Data sample", type=str, choices=["muon", "ele", "pion", "ttbar3TeV", "ttbar380GeV"])
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
args = parser.parse_args()

VERBOSE = args.verbose
if VERBOSE : print(args)

INPUTFILES = args.filesin
OUTPUTFOLDER = args.folderout

LABELS = []
COLORS = []
MARKERS = []
for feature in args.features:
  feat = feature.split(":")
  #print(feat)
  LABELS.append(feat[0])
  COLORS.append(int(feat[1]))
  MARKERS.append(int(feat[2]))

#SAMPLE = args.sample
HISTOPREFIX = 'DQMData/Run 1/HGCAL/Run summary/HGCalValidator/ticlMultiClustersFromTrackstersDummy/'
HISTONAMES = ['multicluster_firstlayer']
#HISTONAMES = ['multicluster_firstlayer','multicluster_layersnum']
#HISTONAMES = args.histonames
AXISTITLE = args.varAxes
#AXISXLOG  = args.logXaxis
#AXISYLOG  = args.logYaxis
#
#MINYAXIS = []
#MAXYAXIS = []
#for axisY in args.rangeYaxis :
#  for rangeY in axisY:
#    #print(rangeY)
#    if rangeY is not "":
#      axis = rangeY.split(":")
#      MINYAXIS.append(float(axis[0]))
#      MAXYAXIS.append(float(axis[1]))
#
#MINXAXIS = []
#MAXXAXIS = []
#for axisX in args.rangeXaxis :
#  for rangeX in axisX :
#    #print(axis)
#    if rangeX is not "":
#      axis = rangeX.split(":")
#      MINXAXIS.append(float(axis[0]))
#      MAXXAXIS.append(float(axis[1]))
#
def main():
  for i_histo in range(0,len(HISTONAMES)) :
    if VERBOSE : 
      print("> Plotting %s histogram:"%HISTONAMES[i_histo])
      print("  Axis titles = %s"%(AXISTITLE[i_histo]))
#      print("  X axis: min = %.2f, max = %.2f, isLog = %s"%(MINXAXIS[i_histo],MAXXAXIS[i_histo],AXISXLOG[i_histo]))
#      print("  Y axis: min = %.2f, max = %.2f, isLog = %s"%(MINYAXIS[i_histo],MAXYAXIS[i_histo],AXISYLOG[i_histo]))
    c = TCanvas("c","c")
    gROOT.SetBatch(True);
#
#    c.SetGrid()
#    if json.loads(AXISXLOG[i_histo].lower()):
#      c.SetLogx()
#    if json.loads(AXISYLOG[i_histo].lower()):
#      c.SetLogy()
#
    leg = TLegend(0.23,0.70,0.45,0.90)
    leg.SetTextSize(0.03)
#    if SAMPLE == "muon" :
#      if "fake" in HISTONAMES[i_histo] : leg = TLegend(0.63,0.60,0.85,0.75)
#      leg.SetHeader("Single #mu^{-}")
#    elif SAMPLE == "ele" :
#      leg.SetHeader("Single e^{-}")
#    elif SAMPLE == "pion" :
#      leg.SetHeader("Single #pi^{-}")
#    elif SAMPLE == "ttbar3TeV" :
#      leg = TLegend(0.23,0.20,0.85,0.35)
#      leg.SetHeader("t#bar{t}, E_{CM} = 3 TeV")
#    elif SAMPLE == "ttbar380GeV" :
#      leg.SetHeader("t#bar{t}, E_{CM} = 380 GeV")
#
    if VERBOSE : print("  Input files used:")
    if VERBOSE : print("  %s"%(INPUTFILES[0]))
    inputTFile = TFile(INPUTFILES[0])
    graph = inputTFile.Get(HISTOPREFIX+HISTONAMES[i_histo])
    graph.SetTitle(AXISTITLE[i_histo])
    graph.SetMarkerStyle(MARKERS[0])
    graph.SetMarkerSize(1.3)
    graph.SetMarkerColor(COLORS[0])
    graph.SetLineColor(COLORS[0])
    graph.SetLineWidth(2)

    graph.Draw("")
#        gPad.Update()
#        graph_copy = graph.GetPaintedGraph()
#        graph_copy.GetXaxis().SetTitleOffset(1.2)
#        graph_copy.SetMinimum(MINYAXIS[i_histo])
#        graph_copy.SetMaximum(MAXYAXIS[i_histo])
#        graph_copy.GetXaxis().SetRangeUser(MINXAXIS[i_histo],MAXXAXIS[i_histo]);
#      else : 
#        graph.Draw("same")

    if VERBOSE : print("  %s"%(INPUTFILES[1]))

    inputTFile2 = TFile(INPUTFILES[1])
    graph2 = inputTFile2.Get(HISTOPREFIX+HISTONAMES[i_histo])
    graph2.SetTitle(AXISTITLE[i_histo])
    graph2.SetMarkerStyle(MARKERS[1])
    graph2.SetMarkerSize(1.3)
    graph2.SetMarkerColor(COLORS[1])
    graph2.SetLineColor(COLORS[1])
    graph2.SetLineWidth(2)

    graph2.Draw("same")

    leg.AddEntry(graph, LABELS[0], "L")
    leg.AddEntry(graph2, LABELS[1], "L")
    leg.Draw("same")
    
#    gPad.Update()
    text = TLatex();
    text.SetTextSize(0.035);
    text.DrawTextNDC(0.175, 0.939349, "CMS HGCal Prelimiary");
    
    c.Draw()
    nameOutputPlot = OUTPUTFOLDER+HISTONAMES[i_histo]
    c.SaveAs(nameOutputPlot+".eps","eps")
    c.SaveAs(nameOutputPlot+".png","png")

  return

if __name__ == "__main__":
    main()
