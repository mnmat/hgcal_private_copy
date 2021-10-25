# Last update with 12_0_1_pre4
# Command example
# python3 plotting_energy.py --filesin /data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e50GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e100GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e200GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e300GeV__nopu.root  --folderout vanilla/singlephoton_EM/ --histoprefix "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/ticlTrackstersEM/" --histonames "trackster_energy" --varAxes ";Regressed Energy;#Tracksters" --sample "Single #gamma, EM iter only" --features "E = 50 GeV:94:21" "E = 100 GeV:64:21" "E = 200 GeV:57:21" "E = 300 GeV:52:21" -v 

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
parser.add_argument('--histoprefix', help='Folders of histo in the ROOT file')
parser.add_argument('--histonames', nargs='+', help='Name of histos to plot (ex. eff_vs_theta eff_vs_phi)')
parser.add_argument('--varAxes', nargs='+', help='Name of axes in histos (ex. ";#theta [#circ];Tracking efficiency" ";#phi [#circ];Tracking efficiency")')
#parser.add_argument('--logXaxis', nargs='+', help='Bool to set log of X axes in histos')
#parser.add_argument('--logYaxis', nargs='+', help='Bool to set log of Y axes in histos')
#parser.add_argument('--rangeYaxis', nargs='+', help='Range Y axis (ex. =\"min:max\")', type=list_with_negatives, action='store')
#parser.add_argument('--rangeXaxis', nargs='+', help='Range X axis (ex. =\"min:max\")', type=list_with_negatives, action='store')
parser.add_argument('--sample', help="Data sample", type=str)
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

SAMPLE = args.sample
#HISTOPREFIX = 'DQMData/Run 1/HGCAL/Run summary/HGCalValidator/'
HISTOPREFIX = args.histoprefix
HISTONAMES = args.histonames
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

GRAPHS = []
def main():
  for i_histo in range(0,len(HISTONAMES)) :
    if VERBOSE : 
      print(("> Plotting %s histogram:"%HISTONAMES[i_histo]))
      print(("  Axis titles = %s"%(AXISTITLE[i_histo])))
#      print("  X axis: min = %.2f, max = %.2f, isLog = %s"%(MINXAXIS[i_histo],MAXXAXIS[i_histo],AXISXLOG[i_histo]))
#      print("  Y axis: min = %.2f, max = %.2f, isLog = %s"%(MINYAXIS[i_histo],MAXYAXIS[i_histo],AXISYLOG[i_histo]))
    c = TCanvas("c","c")
#    gROOT.SetBatch(True);
#
#    c.SetGrid()
#    if json.loads(AXISXLOG[i_histo].lower()):
#      c.SetLogx()
#    if json.loads(AXISYLOG[i_histo].lower()):
#      c.SetLogy()
#
    leg = TLegend(0.53,0.65,0.75,0.85)
    leg.SetTextSize(0.03)
    leg.SetHeader(SAMPLE)

#    # Why this does not work??
#    for i_gr in range(0, len(INPUTFILES)):
#      if VERBOSE: print(("  %s"%(INPUTFILES[i_gr])))
#      inputTFile = TFile(INPUTFILES[i_gr], "r")
#      if inputTFile.IsZombie(): continue
#      graph = inputTFile.Get(HISTOPREFIX+HISTONAMES[i_histo])
#      print(graph)
#   
#      GRAPHS.append(graph)
# 
#      graph.SetMarkerStyle(MARKERS[i_gr])
#      graph.SetMarkerColor(COLORS[i_gr])
#      graph.SetLineColor(COLORS[i_gr])
#      graph.SetMarkerSize(1.3)
#      graph.SetLineWidth(2)
#      graph.Draw("histsame")

#      if i_gr == 0 :
#        graph.SetTitle(AXISTITLE[i_histo])
#        graph.SetMinimum(0)
#        graph.SetMaximum(200)
#        graph.GetXaxis().SetRangeUser(0.,700.);
#        graph.Draw("hist")
#      else :
#        graph.Draw("histsame")
#      leg.AddEntry(graph, LABELS[i_gr], "L")

    if VERBOSE : print("  Input files used:")
    if VERBOSE : print(("  %s"%(INPUTFILES[0])))
    inputTFile = TFile(INPUTFILES[0])
    graph = inputTFile.Get(HISTOPREFIX+HISTONAMES[i_histo])
    graph.SetTitle(AXISTITLE[i_histo])
    graph.SetMarkerStyle(MARKERS[0])
    graph.SetMarkerSize(1.3)
    graph.SetMarkerColor(COLORS[0])
    graph.SetLineColor(COLORS[0])
    graph.SetLineWidth(2)
    graph.SetMinimum(0)
    graph.SetMaximum(200)
    graph.GetXaxis().SetRangeUser(0.,700.);

    graph.Draw("")

    if VERBOSE : print(("  %s"%(INPUTFILES[1])))
    inputTFile2 = TFile(INPUTFILES[1])
    graph2 = inputTFile2.Get(HISTOPREFIX+HISTONAMES[i_histo])
    graph2.SetTitle(AXISTITLE[i_histo])
    graph2.SetMarkerStyle(MARKERS[1])
    graph2.SetMarkerSize(1.3)
    graph2.SetMarkerColor(COLORS[1])
    graph2.SetLineColor(COLORS[1])
    graph2.SetLineWidth(2)

    graph2.Draw("same")

    if VERBOSE : print(("  %s"%(INPUTFILES[2])))
    inputTFile3 = TFile(INPUTFILES[2])
    graph3 = inputTFile3.Get(HISTOPREFIX+HISTONAMES[i_histo])
    graph3.SetTitle(AXISTITLE[i_histo])
    graph3.SetMarkerStyle(MARKERS[2])
    graph3.SetMarkerSize(1.3)
    graph3.SetMarkerColor(COLORS[2])
    graph3.SetLineColor(COLORS[2])
    graph3.SetLineWidth(2)

    graph3.Draw("same")

    if VERBOSE : print(("  %s"%(INPUTFILES[3])))
    inputTFile4 = TFile(INPUTFILES[3])
    graph4 = inputTFile4.Get(HISTOPREFIX+HISTONAMES[i_histo])
    graph4.SetTitle(AXISTITLE[i_histo])
    graph4.SetMarkerStyle(MARKERS[3])
    graph4.SetMarkerSize(1.3)
    graph4.SetMarkerColor(COLORS[3])
    graph4.SetLineColor(COLORS[3])
    graph4.SetLineWidth(2)

    graph4.Draw("same")

#    if VERBOSE : print(("  %s"%(INPUTFILES[4])))
#    inputTFile5 = TFile(INPUTFILES[4])
#    graph5 = inputTFile5.Get(HISTOPREFIX+HISTONAMES[i_histo])
#    graph5.SetTitle(AXISTITLE[i_histo])
#    graph5.SetMarkerStyle(MARKERS[4])
#    graph5.SetMarkerSize(1.3)
#    graph5.SetMarkerColor(COLORS[4])
#    graph5.SetLineColor(COLORS[4])
#    graph5.SetLineWidth(2)
#
#    graph5.Draw("same")

    leg.AddEntry(graph, LABELS[0], "L")
    leg.AddEntry(graph2, LABELS[1], "L")
    leg.AddEntry(graph3, LABELS[2], "L")
    leg.AddEntry(graph4, LABELS[3], "L")
#    leg.AddEntry(graph5, LABELS[4], "L")
    gPad.Update()
    leg.Draw("same")

    c.Draw()
    nameOutputPlot = OUTPUTFOLDER+HISTONAMES[i_histo]
    c.SaveAs(nameOutputPlot+".eps","eps")
    c.SaveAs(nameOutputPlot+".png","png")


  return

if __name__ == "__main__":
    main()
