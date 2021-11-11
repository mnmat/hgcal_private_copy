# CMS DN/2021-005
# 

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, TFile, TCanvas, TGraph, TGraphErrors, TH1F, TLegend, gPad, TLatex, TLine
import json, array, math
import argparse

# From https://twiki.cern.ch/twiki/pub/CMS/Internal/FigGuidelines/myMacro.py.txt
import CMS_lumi, tdrstyle

difference = True
ratio = False

#set the tdr style
tdrstyle.setTDRStyle() # this changes too many things

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "HGCal Testbeam Preliminary"
CMS_lumi.lumi_sqrtS = "" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 50
if (iPos == 0): CMS_lumi.relPosX = 0.12
CMS_lumi.relPosX = 0.50

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

def fillPlotDifference(x, y1, y2, err1, err2):

  graph = TGraphErrors()
  NPOINTS = 0
  for (ix, iy1, iy2, ierr1, ierr2) in zip(x, y1, y2, err1, err2): 
    graph.SetPoint(NPOINTS, ix, iy1-iy2)
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
#  p2.SetTopMargin(0.001);
  p2.SetBottomMargin(bottomSize);

  p1 = ROOT.TPad("p1","p1",0.,1 - topSize,1.,0.95);  
  p1.Draw();
  p1.SetBottomMargin(1);
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

  leg = TLegend(0.60,0.45,0.9,0.70)
  leg.SetTextSize(0.03 / topSize)

  #data, reconstructable
  energy = [   
  19.640062597809063,
  29.65571205007825,
  50,
  79.73395931142407,
  99.76525821596242,
  119.79655712050076,
  149.6870109546166,
  198.04381846635363,
  244.36619718309856,
  288.18466353677616]
  data_values_recable = [
  -0.030923295454545446,
  -0.02907386363636364,
  -0.016585227272727276,
  -0.009863636363636363,
  -0.006482954545454546,
  -0.003678977272727273,
  -0.0027840909090909105,
  -0.0018892045454545455,
  -0.0034999999999999996,
  -0.003142045454545454 ]
  #Fill empty
  data_errors_recable = [  0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0]

  g_data_recable = fillPlotError(energy, data_values_recable, data_errors_recable)
  g_data_recable.GetYaxis().SetTitle("(E_{RECO}/E_{TRUE} - 1)")
  g_data_recable.GetYaxis().SetLabelSize( 0.04 / topSize )
  g_data_recable.GetYaxis().SetNdivisions(505);
  g_data_recable.SetMinimum(-0.04)
  g_data_recable.SetMaximum(0.)
  g_data_recable.SetMarkerSize(1.5)
  g_data_recable.SetMarkerColor(ROOT.kGreen+2) 
  g_data_recable.SetLineColor(ROOT.kGreen+2)
  g_data_recable.SetLineWidth(2) 
  g_data_recable.SetMarkerStyle(21)
  g_data_recable.Draw("APL")

  #data, CLUE clusterised
  data_values_CLUE = [  
  -0.03808238636363637,
  -0.034025568181818185,
  -0.01992613636363636,
  -0.012210227272727272,
  -0.008431818181818183,
  -0.005329545454545454,
  -0.004136363636363636,
  -0.0029431818181818187,
  -0.004215909090909091,
  -0.003738636363636364 ]
  #Fill empty
  data_errors_CLUE = [  0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0]
  g_data_CLUE = fillPlotError(energy, data_values_CLUE, data_errors_CLUE)
  g_data_CLUE.SetMarkerSize(1.5)
  g_data_CLUE.SetMarkerStyle(22)
  g_data_CLUE.SetLineWidth(2)
  g_data_CLUE.SetMarkerColor(ROOT.kOrange-4)
  g_data_CLUE.SetLineColor(ROOT.kOrange-4) 
  g_data_CLUE.Draw("PL")

  leg.AddEntry(g_data_recable, "Reconstructable", "P")
  leg.AddEntry(g_data_CLUE, "Clusterized Hits", "P")
  leg.Draw("same")

  p2.cd();
  if difference : 
    data_difference = fillPlotDifference(energy, data_values_recable, data_values_CLUE, data_errors_recable, data_errors_CLUE) 
    data_difference.GetYaxis().SetTitle("Difference")
    data_difference.GetXaxis().SetTitle("Beam Energy [GeV]")
    data_difference.SetMinimum(-0.01)
    data_difference.SetMaximum(0.01)
    data_difference.GetXaxis().SetTitleSize( 0.04 / bottomSize )
    data_difference.GetYaxis().SetTitleSize( 0.04 / bottomSize )
    data_difference.GetXaxis().SetLabelSize( 0.04 / bottomSize); data_difference.GetXaxis().SetNdivisions(510);
    data_difference.GetYaxis().SetLabelSize( 0.04 / bottomSize); data_difference.GetYaxis().SetNdivisions(205);
    data_difference.GetYaxis().SetTitleOffset( 0.5 )
    data_difference.GetYaxis().CenterTitle()
    data_difference.SetMarkerSize(1.2)
    data_difference.SetMarkerStyle(20)
    data_difference.SetMarkerColor(ROOT.kBlack)
    data_difference.SetLineColor(ROOT.kBlack)
    data_difference.SetLineWidth(2)
    data_difference.Draw("AP");
    c.Update()
    line = ROOT.TLine(p2.GetUxmin(), 0., p2.GetUxmax(), 0.)
    line.SetLineColor(ROOT.kGray+2)
    line.Draw("same")
  if ratio : 
    data_ratio = fillPlotRatio(energy, data_values_recable, data_values_CLUE, data_errors_recable, data_errors_CLUE) 
    data_ratio.GetYaxis().SetTitle("Ratio")
    data_ratio.GetXaxis().SetTitle("Beam Energy [GeV]")
    data_ratio.SetMinimum(0.5)
    data_ratio.SetMaximum(1.5)
    data_ratio.GetXaxis().SetTitleSize( 0.04 / bottomSize )
    data_ratio.GetYaxis().SetTitleSize( 0.04 / bottomSize )
    data_ratio.GetXaxis().SetLabelSize( 0.04 / bottomSize); data_ratio.GetXaxis().SetNdivisions(510);
    data_ratio.GetYaxis().SetLabelSize( 0.04 / bottomSize); data_ratio.GetYaxis().SetNdivisions(205);
    data_ratio.GetYaxis().SetTitleOffset( 0.5 )
    data_ratio.GetYaxis().CenterTitle()
    data_ratio.SetMarkerSize(1.2)
    data_ratio.SetMarkerStyle(20)
    data_ratio.SetMarkerColor(ROOT.kBlack)
    data_ratio.SetLineColor(ROOT.kBlack)
    data_ratio.SetLineWidth(2)
    data_difference.Draw("AP");
    c.Update()
    line = ROOT.TLine(p2.GetUxmin(), 1., p2.GetUxmax(), 1.)
    line.SetLineColor(ROOT.kGray+2)
    line.Draw("same")

  CMS_lumi.CMS_lumi(c, iPeriod, iPos)

  c.Update()
  c.Draw()
  # ERICA: why the png looks so bad??
  c.SaveAs("plotTestBeam.png", "png")
  c.SaveAs("plotTestBeam.eps", "eps")
  c.SaveAs("plotTestBeam.C", "C")
  return

if __name__ == "__main__":
  plotResponse()
