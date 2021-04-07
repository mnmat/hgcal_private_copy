# Command example
# python produce_plots_plotting_eff.py --filesin /home/ericabro/ericabro_cernbox/HGCal_Software/EMTrackSeeded/after_60c3c21/DQM_V0001_R000000001__step4_singlephoton__e10GeV__nopu.root /home/ericabro/ericabro_cernbox/HGCal_Software/EMTrackSeeded/after_60c3c21/DQM_V0001_R000000001__step4_singlephoton__e100GeV__nopu.root --folderout plots_photons/ -v --features "E = 10 GeV:91:22" "E = 100 GeV:64:21" --sample "Single photons" --iters "EM:ticlMultiClustersFromTrackstersEM" "Global:ticlMultiClustersFromTrackstersMerge"

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, TFile, TCanvas, TGraph, TLegend, gPad, TLatex, TLine
import json, array
import argparse

def list_with_negatives(value):
  values = value.split(" ")
  print(values)
  return values

gROOT.Macro("CLICdpStyle.C") 
parser = argparse.ArgumentParser(description='Produce root files with tracking analysis plots')
parser.add_argument('--filesin', nargs='+', help='List of root file used as input')
parser.add_argument('--features', nargs='+', help='List of features used for this input file as label:color:markerStyle (ex. "p_{T} = 1 GeV:1:20:False")')
parser.add_argument('--iters', nargs='+', help='List of iterations label:fullName (ex. "EM:ticlMultiClustersFromTrackstersEM")')
parser.add_argument('--folderout', help='Name of output folder')
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
HISTOPREFIX = 'DQMData/Run 1/HGCAL/Run summary/HGCalValidator'
if 'non' in SAMPLE:
  HISTOPREFIX += '_1SimCl'

HISTONAMES = ["globalEfficiencies"]

LABEL_ITERS = []
FULL_ITERS = []
for i in args.iters:
  iter_name = i.split(":")
  #print(iter_name)
  LABEL_ITERS.append(iter_name[0])
  FULL_ITERS.append(iter_name[1])

GRAPHS = []
x1 = []
y1 = []

# From https://twiki.cern.ch/twiki/pub/CMS/Internal/FigGuidelines/myMacro.py.txt
import CMS_lumi, tdrstyle
import array

#set the tdr style
#tdrstyle.setTDRStyle() # this changes too many things

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "14 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if (iPos == 0): CMS_lumi.relPosX = 0.12

H_ref = 600;
W_ref = 800;
W = W_ref
H = H_ref

iPeriod = 0

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

def main():

  for i_histo in range(0, len(HISTONAMES)) :
    if VERBOSE : 
      print("> Plotting %s histogram:"%HISTONAMES[i_histo])
    c = TCanvas("c","c")

# From https://twiki.cern.ch/twiki/pub/CMS/Internal/FigGuidelines/myMacro.py.txt
    c = TCanvas("c2","c2",50,50,W,H)
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )
    c.SetTickx(0)
    c.SetTicky(0)

    c.SetGrid()
#    gROOT.SetBatch(True);

    gPad.Update()
    leg = TLegend(0.53,0.60,0.75,0.90)
    leg.SetTextSize(0.03)
    leg.SetHeader(SAMPLE)

    if VERBOSE: print("  Input files:")
    for i_gr in range(0, len(INPUTFILES)):
      if VERBOSE: print("  %s"%(INPUTFILES[i_gr]))
      tot_graph = ROOT.TH1F(INPUTFILES[i_gr], INPUTFILES[i_gr], len(FULL_ITERS), 0., len(FULL_ITERS))
      GRAPHS.append(tot_graph)
      inputTFile = TFile(INPUTFILES[i_gr], "r")
      if inputTFile.IsZombie(): continue
      for i_iter in range(0, len(FULL_ITERS)) :
        histofullname = HISTOPREFIX+'/'+FULL_ITERS[i_iter]+'/'+HISTONAMES[i_histo]
        graph = inputTFile.Get(histofullname)
        #print(graph)
        if VERBOSE : print('    Looking at %s'%histofullname)
        #print(graph.GetBinContent(1))
        #print(graph.GetBinError(1))
        tot_graph.SetBinContent(i_iter+1, graph.GetBinContent(1))
        tot_graph.SetBinError(i_iter+1, graph.GetBinError(1))
        tot_graph.GetXaxis().SetBinLabel(i_iter+1,"%s" % LABEL_ITERS[i_iter] )

      inputTFile.Close()
      tot_graph.SetMarkerStyle(i_gr + 2)
      tot_graph.SetMarkerColor(COLORS[i_gr])
      tot_graph.SetLineColor(COLORS[i_gr])
      tot_graph.SetLineWidth(len(INPUTFILES)-i_gr)
      tot_graph.SetMarkerSize(1.3)
      if i_gr == 0 :
        tot_graph.SetMaximum(1.5)
        tot_graph.SetLabelSize(0.07)
        tot_graph.GetYaxis().SetTitle("Tracksters Efficiency ")
        tot_graph.GetYaxis().SetTitleOffset(0.8)
        tot_graph.Draw("P0")
      else :
        tot_graph.Draw("P0same")

      leg.AddEntry(tot_graph, LABELS[i_gr], "PL")

    gPad.Update()
    leg.Draw("same")

    if LABEL_ITERS[-1] == "Merge":
      vert = TLine(len(FULL_ITERS)-1, gPad.GetUymin(), len(FULL_ITERS)-1, gPad.GetUymax())
      vert.Draw()

    CMS_lumi.CMS_lumi(c, iPeriod, iPos)

    c.Draw()
    nameOutputPlot = OUTPUTFOLDER+HISTONAMES[i_histo]
    c.SaveAs(nameOutputPlot+".eps","eps")
    c.SaveAs(nameOutputPlot+".png","png")


  return

if __name__ == "__main__":
    main()
