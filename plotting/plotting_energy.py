# Last update with 12_0_1_pre4
# Command example
# python3 plotting_energy.py --filesin /data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e50GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e100GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e200GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_1_0_pre4/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e300GeV__nopu.root  --folderout vanilla/singlephoton_EM/ --histoprefix "DQMData/Run 1/HGCAL/Run summary/HGCalValidator/ticlTrackstersEM/" --histonames "trackster_energy" --varAxes ";Regressed Energy;#Tracksters" --sample "Single #gamma, EM iter only" --features "E = 50 GeV:94:21" "E = 100 GeV:64:21" "E = 200 GeV:57:21" "E = 300 GeV:52:21" -v 

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, TFile, TCanvas, TGraph, TLegend, gPad, TLatex, TH1F
import json, array
import argparse

def list_with_negatives(value):
  values = value.split(" ")
  print(values)
  return values

gROOT.Macro("CLICdpStyle.C") 
parser = argparse.ArgumentParser(description='Produce root files with tracking analysis plots')
parser.add_argument('--filesin', nargs='+', help='List of root file used as input')
parser.add_argument('--features', nargs='+', help='List of features used for this input file as label:color:markerStyle (ex. "p_{T} = 1 GeV:1:20")')
parser.add_argument('--folderout', help='Name of output folder')
parser.add_argument('--histonames', nargs='+', help='Name of histos to plot (ex. eff_vs_theta eff_vs_phi)')
parser.add_argument('--varAxes', nargs='+', help='Name of axes in histos (ex. ";#theta [#circ];Tracking efficiency" ";#phi [#circ];Tracking efficiency")')
parser.add_argument('--iters', nargs='+', help='List of iterations label:fullName (ex. "EM:ticlMultiClustersFromTrackstersEM")')
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

LABELS_EN = []
COLORS_EN = []
MARKERS_EN = []
for feature in args.features:
  feat = feature.split(":")
  LABELS_EN.append(feat[0])
  COLORS_EN.append(int(feat[1]))
  MARKERS_EN.append(int(feat[2]))

if len(INPUTFILES) != len(LABELS_EN):
  print("Number of input files differs from number of energy features!")
  exit()

SAMPLE = args.sample
HISTOPREFIX = 'DQMData/Run 1/HGCAL/Run summary/HGCalValidator'
if 'non' in SAMPLE:
  HISTOPREFIX += '_1SimCl'

LABELS_ITERS = []
FULL_ITERS = []
COLORS_ITERS = []
MARKERS_ITERS = []
for i in args.iters:
  iter_name = i.split(":")
  LABELS_ITERS.append(iter_name[0])
  FULL_ITERS.append(iter_name[1])
  COLORS_ITERS.append(int(iter_name[2]))
  MARKERS_ITERS.append(int(iter_name[3]))

# From https://twiki.cern.ch/twiki/pub/CMS/Internal/FigGuidelines/myMacro.py.txt
import CMS_lumi, tdrstyle

#set the tdr style
tdrstyle.setTDRStyle() # this changes too many things

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "14 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 50
if (iPos == 0): CMS_lumi.relPosX = 0.12

H_ref = 600;
W_ref = 800;
W = W_ref
H = H_ref

iPeriod = 0

# references for T, B, L, R
T = 0.08*H_ref
B = 0.14*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

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

def main():
  for i_histo in range(0,len(HISTONAMES)) :
    if VERBOSE : 
      print(("> Plotting %s histogram:"%HISTONAMES[i_histo]))
      print(("  Axis titles = %s"%(AXISTITLE[i_histo])))
#      print("  X axis: min = %.2f, max = %.2f, isLog = %s"%(MINXAXIS[i_histo],MAXXAXIS[i_histo],AXISXLOG[i_histo]))
#      print("  Y axis: min = %.2f, max = %.2f, isLog = %s"%(MINYAXIS[i_histo],MAXYAXIS[i_histo],AXISYLOG[i_histo]))
    if not VERBOSE : gROOT.SetBatch(True);
    for i_iter in range(0, len(FULL_ITERS)) :
      c = TCanvas("c","c")
      c.SetFillColor(0)
      c.SetBorderMode(0)
      c.SetFrameFillStyle(0)
      c.SetFrameBorderMode(0)
      c.SetTickx(0)
      c.SetTicky(0)
#
#      c.SetGrid()
#      if json.loads(AXISXLOG[i_histo].lower()):
#        c.SetLogx()
#      if json.loads(AXISYLOG[i_histo].lower()):
#        c.SetLogy()
#
      leg = TLegend(0.53,0.65,0.75,0.85)
      leg.SetTextSize(0.03)
      final_label = SAMPLE + ", " + LABELS_ITERS[i_iter] + " iter only"
      leg.SetHeader(final_label)
      histofullname = HISTOPREFIX+'/'+FULL_ITERS[i_iter]+'/'+HISTONAMES[i_histo]
      if VERBOSE : print("  Histo path: %s"%(histofullname))

#      # Why this does not work??
#      GRAPHS = []
#      NPOINTS = []
#      for label_en in LABELS_EN :
#        graph_en = TH1F(label_en, label_en, 500, 0., 500.)
#        GRAPHS.append(graph_en)
#        NPOINTS.append(0)
#
#      if VERBOSE: print("  Input files:")
#      for i_en in range(0, len(LABELS_EN)):
#        if VERBOSE: print(("  %s"%(INPUTFILES[i_en])))
#        inputTFile = TFile(INPUTFILES[i_en], "r")
#        if inputTFile.IsZombie(): continue
#        graph = inputTFile.Get(histofullname)
#        print(graph)
#        new = TH1F(graph.Clone("new"+ROOT.TString(i_en)))
#
#      for i_gr in range(0, len(LABELS_EN)):
#        if i_gr == 0 :
#          GRAPHS[i_gr].Draw("PE0")
#        else :
#          GRAPHS[i_gr].Draw("PE0same")
#        leg.AddEntry(graph, LABELS[i_gr], "L")

      if VERBOSE : print("  Input files used:")
      if VERBOSE : print(("  %s"%(INPUTFILES[0])))
      inputTFile = TFile(INPUTFILES[0])
      graph = inputTFile.Get(histofullname)
      if VERBOSE : print(graph)
      graph.SetTitle(AXISTITLE[i_histo])
      graph.SetMarkerStyle(MARKERS_EN[0])
      graph.SetMarkerSize(1.3)
      graph.SetMarkerColor(COLORS_EN[0])
      graph.SetLineColor(COLORS_EN[0])
      graph.SetLineWidth(2)
      graph.SetMinimum(0)
      graph.SetMaximum(200)
      graph.GetXaxis().SetRangeUser(0.,700.);

      graph.Draw("")

      if VERBOSE : print(("  %s"%(INPUTFILES[1])))
      inputTFile2 = TFile(INPUTFILES[1])
      graph2 = inputTFile2.Get(histofullname)
      graph2.SetTitle(AXISTITLE[i_histo])
      graph2.SetMarkerStyle(MARKERS_EN[1])
      graph2.SetMarkerSize(1.3)
      graph2.SetMarkerColor(COLORS_EN[1])
      graph2.SetLineColor(COLORS_EN[1])
      graph2.SetLineWidth(2)

      graph2.Draw("same")

      if VERBOSE : print(("  %s"%(INPUTFILES[2])))
      inputTFile3 = TFile(INPUTFILES[2])
      graph3 = inputTFile3.Get(histofullname)
      graph3.SetTitle(AXISTITLE[i_histo])
      graph3.SetMarkerStyle(MARKERS_EN[2])
      graph3.SetMarkerSize(1.3)
      graph3.SetMarkerColor(COLORS_EN[2])
      graph3.SetLineColor(COLORS_EN[2])
      graph3.SetLineWidth(2)

      graph3.Draw("same")

      if VERBOSE : print(("  %s"%(INPUTFILES[3])))
      inputTFile4 = TFile(INPUTFILES[3])
      graph4 = inputTFile4.Get(histofullname)
      graph4.SetTitle(AXISTITLE[i_histo])
      graph4.SetMarkerStyle(MARKERS_EN[3])
      graph4.SetMarkerSize(1.3)
      graph4.SetMarkerColor(COLORS_EN[3])
      graph4.SetLineColor(COLORS_EN[3])
      graph4.SetLineWidth(2)

      graph4.Draw("same")

      if VERBOSE : print(("  %s"%(INPUTFILES[4])))
      inputTFile5 = TFile(INPUTFILES[4])
      graph5 = inputTFile5.Get(histofullname)
      graph5.SetTitle(AXISTITLE[i_histo])
      graph5.SetMarkerStyle(MARKERS_EN[4])
      graph5.SetMarkerSize(1.3)
      graph5.SetMarkerColor(COLORS_EN[4])
      graph5.SetLineColor(COLORS_EN[4])
      graph5.SetLineWidth(2)

      graph5.Draw("same")

      if VERBOSE : print(("  %s"%(INPUTFILES[5])))
      inputTFile6 = TFile(INPUTFILES[5])
      graph6 = inputTFile6.Get(histofullname)
      graph6.SetTitle(AXISTITLE[i_histo])
      graph6.SetMarkerStyle(MARKERS_EN[5])
      graph6.SetMarkerSize(1.3)
      graph6.SetMarkerColor(COLORS_EN[5])
      graph6.SetLineColor(COLORS_EN[5])
      graph6.SetLineWidth(2)

      graph6.Draw("same")

      leg.AddEntry(graph,  LABELS_EN[0], "L")
      leg.AddEntry(graph2, LABELS_EN[1], "L")
      leg.AddEntry(graph3, LABELS_EN[2], "L")
      leg.AddEntry(graph4, LABELS_EN[3], "L")
      leg.AddEntry(graph5, LABELS_EN[4], "L")
      leg.AddEntry(graph6, LABELS_EN[5], "L")
      gPad.Update()
      leg.Draw("same")
      CMS_lumi.CMS_lumi(c, iPeriod, iPos)

      c.Draw()
      nameOutputPlot = OUTPUTFOLDER+HISTONAMES[i_histo]+"_"+LABELS_ITERS[i_iter]
      c.SaveAs(nameOutputPlot+".eps","eps")
      c.SaveAs(nameOutputPlot+".png","png")

  return

if __name__ == "__main__":
    main()
