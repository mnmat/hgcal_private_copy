# Last update with 12_0_1_pre4
# Command example
# 

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, TFile, TCanvas, TGraph, TGraphErrors, TH1F, TLegend, gPad, TLatex, TLine
import json, array, math
import argparse

# From https://twiki.cern.ch/twiki/pub/CMS/Internal/FigGuidelines/myMacro.py.txt
import CMS_lumi, tdrstyle

#set the tdr style
tdrstyle.setTDRStyle() # this changes too many things

#If False, the sigma is used as error
errMean = False

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
L = 0.15*W_ref
R = 0.04*W_ref

topSize = 0.7
bottomSize = 0.3
bottomOffset = 0.

def fillPlotError(x, y, err):

  graph = TGraphErrors()
  NPOINTS = 0
  for (ix, iy, iey) in zip(x, y, err):            
    graph.SetPoint(NPOINTS, ix, iy)
    graph.SetPointError(NPOINTS, 0, iey)
    NPOINTS = NPOINTS + 1

  return graph

def fillPlotRatio(x, y1, y2, err1, err2):

  graph = TGraphErrors()
  NPOINTS = 0
  for (ix, iy1, iy2, ierr1, ierr2) in zip(x, y1, y2, err1, err2): 
    graph.SetPoint(NPOINTS, ix, iy1/iy2)
    ierr = math.sqrt(ierr1*ierr1 + ierr2*ierr2)
    graph.SetPointError(NPOINTS, 0, ierr*iy1/iy2)
    NPOINTS = NPOINTS + 1

  return graph

def plotResponse():
#  ROOT.gStyle.SetOptStat(0)
#  gROOT.SetBatch(False);
  c = TCanvas("c2","c2",50,50,W,H)

  p2 = ROOT.TPad("p2","p3",0.,bottomOffset,1.,bottomSize); 
  p2.Draw();
  p2.SetTopMargin(0.001);
  p2.SetBottomMargin(0.3);

  p1 = ROOT.TPad("p1","p1",0.,1 - topSize,1.,0.95);  
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

  leg = TLegend(0.30,0.10,0.9,0.3)
  leg.SetNColumns(2)
  leg.SetTextSize(0.03 / topSize)

  #pions, reconstructable
  energy = [   10,   20,   50,   100,   200,   300]
  pion_values_recable = [     0.809746,
   0.8550566,
   0.9012686,
   0.916591,
   0.9241791,
   0.9355128]
  #Sigma from the fit
  pion_errors_recable = [  0.1918199,
   0.1558144,
   0.1192124,
   0.08586224,
   0.06906588,
   0.06069801]
   #Error on the mean
  if errMean : 
     pion_errors_recable = [  0.01006934,  0.009053703,  0.006288085,  0.004593517,  0.004124433,  0.003325533]

  g_pion_recable = fillPlotError(energy, pion_values_recable, pion_errors_recable)
  g_pion_recable.GetYaxis().SetTitle("E_{RECO}/E_{GEN}")
  g_pion_recable.GetYaxis().SetLabelSize( 0.04 / topSize )
  g_pion_recable.GetYaxis().SetNdivisions(505);
  g_pion_recable.SetMinimum(0.4)
  g_pion_recable.SetMaximum(1.3)
  g_pion_recable.SetMarkerSize(1.5)
  g_pion_recable.SetMarkerColor(ROOT.kBlue+2) 
  g_pion_recable.SetLineColor(ROOT.kBlue+2) 
  g_pion_recable.SetLineWidth(2) 
  g_pion_recable.SetMarkerStyle(22)
  g_pion_recable.Draw("AP")

  #pions, CLUE clusterised
  pion_values_CLUE = [  0.7651331,
   0.8165129,
   0.874612,
   0.8990833,
   0.9137521,
   0.9264494]
  #Sigma from the fit
  pion_errors_CLUE = [0.2053781,
   0.1611473,
   0.118186,
   0.08667604,
   0.07258907,
   0.06198718]
  #Error on the mean
  if errMean : 
    pion_errors_CLUE = [  0.01006934,   0.009053703,   0.006288085,   0.004593517,   0.004124433,   0.003325533]
  g_pion_CLUE = fillPlotError(energy, pion_values_CLUE, pion_errors_CLUE)
  g_pion_CLUE.SetMarkerSize(1.5)
  g_pion_CLUE.SetMarkerStyle(26)
  g_pion_CLUE.SetMarkerColor(ROOT.kAzure+2)
  g_pion_CLUE.SetLineColor(ROOT.kAzure+2) 
  g_pion_CLUE.Draw("P")

  #photons, recable
  photon_values_recable = [  1.018914,
   1.012946,
   1.015002,
   1.014852,
   1.017496,
   1.019326]
  #Sigma from the fit
  photon_errors_recable = [ 0.07151062,
   0.05525297,
   0.03728509,
   0.02709585,
   0.02242512,
   0.0188195 ]
  #Error on the mean
  if errMean : 
    photon_errors_recable = [  0.004093275,
     0.003571733,
     0.01023423,
     0.007243054,
     0.004588783,
     0.000648609]
  g_photon_recable = fillPlotError(energy, photon_values_recable, photon_errors_recable)
  g_photon_recable.SetMarkerSize(1.5)
  g_photon_recable.SetMarkerStyle(20)
  g_photon_recable.SetMarkerColor(ROOT.kOrange+1)
  g_photon_recable.SetLineColor(ROOT.kOrange+1)
  g_photon_recable.SetLineWidth(2) 
  g_photon_recable.Draw("P")

  #photons, CLUE
  photon_values_CLUE = [  1.007362,
   1.006438,
   1.009577,
   1.011091,
   1.014405,
   1.016899]
  #Sigma from the fit
  photon_errors_CLUE = [  0.07420741,
   0.05478463,
   0.034986,
   0.02696595,
   0.02130994,
   0.01867162 ]
  #Error on the mean
  if errMean : 
    photon_errors_CLUE = [  0.003938965,
     0.003548968,
     0.005989669,
     0.009316756,
     0.00670014,
     0.001893525]
  g_photon_CLUE = fillPlotError(energy, photon_values_CLUE, photon_errors_CLUE)
  g_photon_CLUE.SetMarkerSize(1.5)
  g_photon_CLUE.SetMarkerStyle(24)
  g_photon_CLUE.SetMarkerColor(ROOT.kOrange+2)
  g_photon_CLUE.SetLineColor(ROOT.kOrange+2)
  g_photon_CLUE.Draw("P")

  # ERICA: Title to columns?
  leg.AddEntry(g_photon_recable, "Single-#gamma, Rec/able", "P")
  leg.AddEntry(g_photon_CLUE, "Single-#gamma, Clustered", "P")
  leg.AddEntry(g_pion_recable, "Single-#pi^{+/-}, Rec/able", "P")
  leg.AddEntry(g_pion_CLUE, "Single-#pi^{+/-}, Clustered", "P")
  leg.Draw("same")

  p2.cd();
  pion_ratio = fillPlotRatio(energy, pion_values_recable, pion_values_CLUE, pion_errors_recable, pion_errors_CLUE) 
  if errMean : 
    pion_ratio.SetMinimum(0.8)
    pion_ratio.SetMaximum(1.2)
  pion_ratio.GetYaxis().SetTitle("Ratio")
  pion_ratio.GetXaxis().SetTitle("E_{GEN} [GeV]")
  pion_ratio.GetXaxis().SetTitleSize( 0.04 / bottomSize )
  pion_ratio.GetYaxis().SetTitleSize( 0.04 / bottomSize )
  pion_ratio.GetXaxis().SetLabelSize( 0.04 / bottomSize); pion_ratio.GetXaxis().SetNdivisions(510);
  pion_ratio.GetYaxis().SetLabelSize( 0.04 / bottomSize); pion_ratio.GetYaxis().SetNdivisions(205);
  pion_ratio.GetYaxis().SetTitleOffset( 0.5 )
  pion_ratio.GetYaxis().CenterTitle()
  pion_ratio.SetMarkerSize(1.5)
  pion_ratio.SetMarkerStyle(26)
  pion_ratio.SetMarkerColor(ROOT.kBlue+2)
  pion_ratio.SetLineColor(ROOT.kBlue+1)
  pion_ratio.SetLineWidth(2)
  pion_ratio.Draw("AP");

  photon_ratio = fillPlotRatio(energy, photon_values_recable, photon_values_CLUE, photon_errors_recable, photon_errors_CLUE) 
  photon_ratio.SetMarkerSize(1.5)
  photon_ratio.SetMarkerStyle(24)
  photon_ratio.SetMarkerColor(ROOT.kOrange+2)
  photon_ratio.SetLineColor(ROOT.kOrange+2)
  photon_ratio.SetLineWidth(2)
  photon_ratio.Draw("P");

  c.Update()
  line = ROOT.TLine(p2.GetUxmin(), 1., p2.GetUxmax(), 1.)
  line.Draw("same")

  CMS_lumi.CMS_lumi(c, iPeriod, iPos)

  c.Draw()
  # ERICA: why the png looks so bad??
  c.SaveAs("plotResponse.png", "png")
  c.SaveAs("plotResponse.eps", "eps")
  c.SaveAs("plotResponse.C", "C")
  return

if __name__ == "__main__":
  plotResponse()
