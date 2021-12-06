# Last update with 12_0_1_pre4
# Command example
# 

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, TFile, TCanvas, TGraph, TGraphErrors, TH1F, TLegend, gPad, TLatex, TLine
import json, array, math, os
import argparse
import lib_plotting

# From https://twiki.cern.ch/twiki/pub/CMS/Internal/FigGuidelines/myMacro.py.txt
import CMS_lumi, tdrstyle

onlyPhotons = False

#set the tdr style
tdrstyle.setTDRStyle() # this changes too many things

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Phase-II Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 50
if (iPos == 0): CMS_lumi.relPosX = 0.12
CMS_lumi.relPosY = 0.05

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

def plotEffAndPurity(metric):
#  ROOT.gStyle.SetOptStat(0)
#  gROOT.SetBatch(False);
  c = TCanvas("c2","c2",50,50,W,H)

  if not onlyPhotons:
    p2 = ROOT.TPad("p2","p3",0.,bottomOffset,1.,bottomSize); 
    p2.Draw();
#    p2.SetTopMargin(0.001);
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

  #photons, TICL
  energy = [   10,   20,   50,   100,   200,   300]
  photon_values_TICL = []
  photon_errors_TICL = []  
  photon_values_CLUE3D = []
  photon_errors_CLUE3D = []

  if metric == "Efficiency":
    photon_values_TICL = [0.899598, 0.997996, 1.000000, 1.000000, 1.000000, 1.000000]
    photon_errors_TICL = [0.013467, 0.002002, 0.000000, 0.000000, 0.000000, 0.000000]
    photon_values_CLUE3D = [0.353414+0.640562 , 0.997996, 1.000000, 1.000000, 1.000000, 1.000000]
    photon_errors_CLUE3D = [0.03035119841, 0.002002, 0.000000, 0.000000, 0.000000, 0.000000]
  elif metric == "Purity":
    photon_values_TICL = [0.863454, 0.993988, 0.997996, 1.000000, 1.000000, 1.000000]
    photon_errors_TICL = [0.015387, 0.003461, 0.002002, 0.000000, 0.000000, 0.000000]
    photon_values_CLUE3D = [0.353414+0.634538, 0.995992, 0.995992, 0.995992, 1.000000, 1.000000, 0.997996]
    photon_errors_CLUE3D = [0.030405, 0.002828, 0.002828, 0.000000, 0.000000, 0.002002]
  else :
    print("Metric %s does not exist!"%metric)
    return

  g_photon_TICL = lib_plotting.fillPlotError(energy, photon_values_TICL, photon_errors_TICL)
  g_photon_TICL.GetYaxis().SetTitle("Tracksters "+metric)
  g_photon_TICL.GetYaxis().SetLabelSize( 0.04 / topSize )
  g_photon_TICL.GetYaxis().SetNdivisions(505);
  g_photon_TICL.SetMinimum(0.0)
  g_photon_TICL.SetMaximum(1.4)
  if onlyPhotons:
    g_photon_TICL.SetMinimum(0.7)
    g_photon_TICL.SetMaximum(1.2)
    g_photon_TICL.GetXaxis().SetTitle("E_{GEN} [GeV]")
    g_photon_TICL.GetXaxis().SetTitleOffset( 1.0)
  g_photon_TICL.SetMarkerSize(1.3)
  g_photon_TICL.SetMarkerColor(ROOT.kOrange+2) 
  g_photon_TICL.SetLineColor(ROOT.kOrange+2) 
  g_photon_TICL.SetLineWidth(2) 
  g_photon_TICL.SetMarkerStyle(22)
  #Draw only axis is needed to draw line under the markers
  g_photon_TICL.GetHistogram().Draw("AXIS")

  if onlyPhotons:
    c.Update()
    line = ROOT.TLine(c.GetUxmin(), 1., c.GetUxmax(), 1.)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kGray+1)
    line.Draw("same")
  else:
    c.Update()
    line = ROOT.TLine(p1.GetUxmin(), 1., p1.GetUxmax(), 1.)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kGray+1)
    line.Draw("same")

  g_photon_TICL.Draw("PL")

  #photons, CLUE3D clusterised
  g_photon_CLUE3D = lib_plotting.fillPlotError(energy, photon_values_CLUE3D, photon_errors_CLUE3D)
  g_photon_CLUE3D.SetMarkerSize(1.5)
  g_photon_CLUE3D.SetMarkerStyle(26)
  g_photon_CLUE3D.SetMarkerColor(ROOT.kOrange+4)
  g_photon_CLUE3D.SetLineColor(ROOT.kOrange+4) 
  if onlyPhotons:
    g_photon_CLUE3D.SetMarkerColor(ROOT.kRed+2)
    g_photon_CLUE3D.SetLineColor(ROOT.kRed+2) 
  g_photon_CLUE3D.SetLineStyle(2) 
  g_photon_CLUE3D.Draw("PL")

  #electrons, TICL
  electron_values_TICL = []
  electron_errors_TICL = []  
  electron_values_CLUE3D = []
  electron_errors_CLUE3D = []

  if metric == "Efficiency":
    electron_values_TICL = [0.472000, 0.586000, 0.816000, 0.932000, 0.980000, 0.988000]
    electron_errors_TICL = [0.022326, 0.022027, 0.017329, 0.011258, 0.006261, 0.004870]
    electron_values_CLUE3D = [0.024000+0.518000, 0.638000+0.052000, 0.856000, 0.948000, 0.994000, 1.000000]
    electron_errors_CLUE3D = [0.02337, 0.02367, 0.015701, 0.009929, 0.003454, 0.000000]
  elif metric == "Purity":
    electron_values_TICL = [0.306000, 0.438000, 0.702000, 0.890000, 0.972000, 0.986000]
    electron_errors_TICL = [0.020609, 0.022188, 0.020455, 0.013993, 0.007378, 0.005254]
    electron_values_CLUE3D = [0.024000+0.358000, 0.506000+0.004000, 0.726000, 0.876000, 0.980000, 1.000000]
    electron_errors_CLUE3D = [0.02250, 0.02253, 0.019946, 0.014739, 0.006261, 0.000000]
  else :
    print("Metric %s does not exist!"%metric)
    return

  g_electron_TICL = lib_plotting.fillPlotError(energy, electron_values_TICL, electron_errors_TICL)
  g_electron_TICL.SetMarkerSize(1.5)
  g_electron_TICL.SetMarkerStyle(20)
  g_electron_TICL.SetMarkerColor(ROOT.kMagenta+1)
  g_electron_TICL.SetLineColor(ROOT.kMagenta+1)
  g_electron_TICL.SetLineWidth(2) 
  if not onlyPhotons:
    g_electron_TICL.Draw("PL")

  #electron, CLUE3D clusterised
  g_electron_CLUE3D = lib_plotting.fillPlotError(energy, electron_values_CLUE3D, electron_errors_CLUE3D)
  g_electron_CLUE3D.SetMarkerSize(1.5)
  g_electron_CLUE3D.SetMarkerStyle(24)
  g_electron_CLUE3D.SetMarkerColor(ROOT.kMagenta+2)
  g_electron_CLUE3D.SetLineColor(ROOT.kMagenta+2)
  g_electron_CLUE3D.SetLineStyle(2)
  if not onlyPhotons:
    g_electron_CLUE3D.Draw("PL")

  if onlyPhotons:
    leg = TLegend(0.50,0.25,0.8,0.50)
    leg.SetTextSize(0.03 / topSize)
    leg.SetHeader("Single-#gamma, PU = 0")
    leg.AddEntry(g_photon_TICL, "TICL - CA (default)", "PL")
    leg.AddEntry(g_photon_CLUE3D, "TICL - CLUE3D", "PL")
    leg.Draw("same")
  else:
    leg = TLegend(0.30,0.15,0.9,0.40)
    leg.SetTextSize(0.03 / topSize)
    leg.SetNColumns(2)
    leg.SetHeader("PU = 0")
    leg.AddEntry(g_photon_TICL, "Single-#gamma, TICL - CA", "PL")
    leg.AddEntry(g_electron_TICL, "Single-e^{+/-}, TICL - CA", "PL")
    leg.AddEntry(g_photon_CLUE3D, "Single-#gamma, TICL - CLUE3D", "PL")
    leg.AddEntry(g_electron_CLUE3D, "Single-e^{+/-}, TICL - CLUE3D", "PL")
    leg.Draw("same")

  if not onlyPhotons:
    p2.cd();
    photon_ratio = lib_plotting.fillPlotRatio(energy, photon_values_TICL, photon_values_CLUE3D, photon_errors_TICL, photon_errors_CLUE3D) 
    photon_ratio.SetMinimum(0.8)
    photon_ratio.SetMaximum(1.2)
    photon_ratio.GetYaxis().SetTitle("Ratio")
    photon_ratio.GetXaxis().SetTitle("E_{GEN} [GeV]")
    photon_ratio.GetXaxis().SetTitleSize( 0.04 / bottomSize )
    photon_ratio.GetYaxis().SetTitleSize( 0.04 / bottomSize )
    photon_ratio.GetXaxis().SetLabelSize( 0.04 / bottomSize); photon_ratio.GetXaxis().SetNdivisions(510);
    photon_ratio.GetYaxis().SetLabelSize( 0.04 / bottomSize); photon_ratio.GetYaxis().SetNdivisions(205);
    photon_ratio.GetYaxis().SetTitleOffset( 0.5 )
    photon_ratio.GetYaxis().CenterTitle()
    photon_ratio.SetMarkerSize(1.5)
    photon_ratio.SetMarkerStyle(26)
    photon_ratio.SetMarkerColor(ROOT.kOrange+2)
    photon_ratio.SetLineColor(ROOT.kOrange+2)
    photon_ratio.SetLineWidth(2)
    #Draw only axis is needed to draw line under the markers
    photon_ratio.GetHistogram().Draw("AXIS")

    c.Update()
    lineRatio = ROOT.TLine(p2.GetUxmin(), 1., p2.GetUxmax(), 1.)
    lineRatio.SetLineStyle(2)
    lineRatio.SetLineColor(ROOT.kGray+1)
    lineRatio.Draw("same")

    photon_ratio.Draw("P");

    electron_ratio = lib_plotting.fillPlotRatio(energy, electron_values_TICL, electron_values_CLUE3D, electron_errors_TICL, electron_errors_CLUE3D) 
    electron_ratio.SetMarkerSize(1.5)
    electron_ratio.SetMarkerStyle(24)
    electron_ratio.SetMarkerColor(ROOT.kMagenta+2)
    electron_ratio.SetLineColor(ROOT.kMagenta+2)
    electron_ratio.SetLineWidth(2)
    electron_ratio.Draw("P");

  CMS_lumi.CMS_lumi(c, iPeriod, iPos)

  c.Draw()
  name = "ACAT2021/plot" + metric
  if onlyPhotons:
    name = "ACAT2021/plot" + metric + "_onlyPhotons"
  lib_plotting.savePlot(c, name)
  return

if __name__ == "__main__":
  plotEffAndPurity("Efficiency")
  plotEffAndPurity("Purity")
