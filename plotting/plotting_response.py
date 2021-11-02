# Last update with 12_0_1_pre4
# Command example
# 

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, TFile, TCanvas, TGraph, TGraphErrors, TH1F, TLegend, gPad, TLatex, TLine
import json, array
import argparse

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

def fillPlotError(x, y, err):

  graph = TGraphErrors()
  NPOINTS = 0
  for (ix, iy, iey) in zip(x, y, err):            
    graph.SetPoint(NPOINTS, ix, iy)
    graph.SetPointError(NPOINTS, 0, iey)
    NPOINTS = NPOINTS + 1

  return graph

def fillPlotRatio(x, y1, y2):

  graph = TGraph()
  NPOINTS = 0
  for (ix, iy1, iy2) in zip(x, y1, y2): 
    graph.SetPoint(NPOINTS, ix, iy1/iy2)
    NPOINTS = NPOINTS + 1

  return graph

def plotResponse():
  ROOT.gStyle.SetOptStat(0)
  gROOT.SetBatch(False);
  c = TCanvas("c2","c2",50,50,W,H)

  p2 = ROOT.TPad("p2","p3",0.,0.,1.,0.3); 
  p2.Draw();
  p2.SetTopMargin(0.001);
  p2.SetBottomMargin(0.3);

  p1 = ROOT.TPad("p1","p1",0.,0.3,1.,1.);  
  p1.Draw();
  p1.SetBottomMargin(0.001);
  p1.cd();

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

  leg = TLegend(0.50,0.30,0.95,0.50)
  leg.SetNColumns(2)
  leg.SetTextSize(0.03)

  #pions, reconstructable
  energy = [   10,   20,   50,   100,   200,   300]
  pion_values_recable = [  0.8132535, 0.8555554, 0.8960099, 0.9148156,   0.928956,   0.9368102]
  pion_errors_recable = [  0.01006934,  0.009053703,  0.006288085,  0.004593517,  0.004124433,  0.003325533]

  g_pion_recable = fillPlotError(energy, pion_values_recable, pion_errors_recable)
  g_pion_recable.GetYaxis().SetTitle("E_{RECO}/E_{GEN}")
  g_pion_recable.SetMinimum(0)
  g_pion_recable.SetMaximum(1.3)
  g_pion_recable.SetMarkerColor(ROOT.kAzure+2) 
  g_pion_recable.SetMarkerStyle(22)
  g_pion_recable.SetLineColor(2) 
  g_pion_recable.Draw("AP")

  #pions, CLUE clusterised
  pion_values_CLUE = [  0.7654207,   0.8209429,   0.8707107,   0.8952595,   0.9159519,   0.9277338]
  pion_errors_CLUE = [  0.01006934,   0.009053703,   0.006288085,   0.004593517,   0.004124433,   0.003325533]
  g_pion_CLUE = fillPlotError(energy, pion_values_CLUE, pion_errors_CLUE)
  g_pion_CLUE.SetMarkerStyle(26)
  g_pion_CLUE.SetMarkerColor(ROOT.kAzure+2)
  g_pion_CLUE.Draw("P")

  #photons, recable
  photon_values_recable = [  1.018485,
   1.016395,
   1.009366,
   1.010924,
   1.011171,
   1.025517]
  photon_errors_recable = [  0.004093275,
   0.003571733,
   0.01023423,
   0.007243054,
   0.004588783,
   0.000648609]
  g_photon_recable = fillPlotError(energy, photon_values_recable, photon_errors_recable)
  g_photon_recable.SetMarkerStyle(20)
  g_photon_recable.SetMarkerColor(ROOT.kOrange+1)
  g_photon_recable.Draw("P")

  #photons, CLUE
  photon_values_CLUE = [  1.007119,
   1.008034,
   1.001513,
   1.006748,
   1.00913,
   1.016827]
  photon_errors_CLUE = [  0.003938965,
   0.003548968,
   0.005989669,
   0.009316756,
   0.00670014,
   0.001893525]
  g_photon_CLUE = fillPlotError(energy, photon_values_CLUE, photon_errors_CLUE)
  g_photon_CLUE.SetMarkerStyle(24)
  g_photon_CLUE.SetMarkerColor(ROOT.kOrange+1)
  g_photon_CLUE.Draw("P")

  leg.AddEntry(g_photon_recable, "Single-#gamma, Rec/able", "P")
  leg.AddEntry(g_photon_CLUE, "Single-#gamma, Clustered", "P")
  leg.AddEntry(g_pion_recable, "Single-#pi^{+/-}, Rec/able", "P")
  leg.AddEntry(g_pion_CLUE, "Single-#pi^{+/-}, Clustered", "P")
  leg.Draw("same")

  CMS_lumi.CMS_lumi(c, iPeriod, iPos)

  p2.cd();
  pion_ratio = fillPlotRatio(energy, pion_values_recable, pion_values_CLUE) 
  pion_ratio.SetMinimum(0.8)
  pion_ratio.SetMaximum(1.2)
  pion_ratio.GetYaxis().SetTitle("Ratio")
  pion_ratio.GetXaxis().SetTitle("EN_{GEN}")
  pion_ratio.GetXaxis().SetLabelSize(0.075);
  pion_ratio.GetYaxis().SetLabelSize(0.075);
  pion_ratio.SetMarkerStyle(22)
  pion_ratio.SetMarkerColor(ROOT.kAzure+1)
  pion_ratio.Draw("AP");

  photon_ratio = fillPlotRatio(energy, photon_values_recable, photon_values_CLUE) 
  photon_ratio.SetMarkerStyle(20)
  photon_ratio.SetMarkerColor(ROOT.kOrange+1)
  photon_ratio.Draw("P");

  c.Draw()
  c.SaveAs("plot.png", "png")
  return

if __name__ == "__main__":
  plotResponse()
