import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, TFile, TCanvas, TGraph, TGraphErrors, TH1F, TLegend, gPad, TLatex, TLine
import json, array, os
import argparse
import numpy as np
import lib_plotting

# From https://twiki.cern.ch/twiki/pub/CMS/Internal/FigGuidelines/myMacro.py.txt
import CMS_lumi, tdrstyle

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

def plotValues(energy, 
               photon_values_recable, photon_errors_recable, photon_values_CLUE, photon_errors_CLUE, 
               pion_values_recable, pion_errors_recable, pion_values_CLUE, pion_errors_CLUE, 
               variable = "Resolution", plotRatio = False):
  ROOT.gStyle.SetOptStat(0)
  gROOT.SetBatch(False);
  c = TCanvas("c2","c2",50,50,W,H)

  if plotRatio :
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

  leg = TLegend(0.18,0.55,0.8,0.80)
  if plotRatio:
    leg = TLegend(0.30,0.35,0.9,0.60)
  if variable == "Response":
    leg = TLegend(0.30,0.15,0.9,0.40)
  leg.SetNColumns(2)
  leg.SetTextSize(0.025 / topSize)
  if plotRatio:
    leg.SetTextSize(0.03 / topSize)

  g_pion_recable = lib_plotting.fillPlotError(energy, pion_values_recable, pion_errors_recable)
  g_pion_recable.GetYaxis().SetTitle("#sigma_{E}/E")
  if variable == "Response":
    g_pion_recable.GetYaxis().SetTitle("E_{ALL HITS}/E_{GEN}")
  if not plotRatio:
    g_pion_recable.GetXaxis().SetTitle("E_{GEN} [GeV]")
  g_pion_recable.GetXaxis().SetTitleOffset( 1.0 )
  g_pion_recable.GetYaxis().SetLabelSize( 0.04 / topSize )
  g_pion_recable.GetYaxis().SetNdivisions(505);
  g_pion_recable.SetMinimum(0.0)
  g_pion_recable.SetMaximum(0.5)
  if variable == "Response":
    g_pion_recable.SetMinimum(0.4)
    g_pion_recable.SetMaximum(1.3)
  g_pion_recable.SetMarkerSize(1.5)
  g_pion_recable.SetMarkerColor(ROOT.kBlue+2) 
  g_pion_recable.SetLineColor(ROOT.kBlue+2) 
  g_pion_recable.SetLineWidth(2) 
  g_pion_recable.SetMarkerStyle(22)
  #Draw only axis is needed to draw line under the markers
  g_pion_recable.GetHistogram().Draw("AXIS")

  c.Update()
  line = ROOT.TLine(c.GetUxmin(), 1., c.GetUxmax(), 1.)
  if plotRatio:
    line = ROOT.TLine(p1.GetUxmin(), 1., p1.GetUxmax(), 1.)
  line.SetLineStyle(2)
  line.SetLineColor(ROOT.kGray+1)
  line.Draw("same")

  g_pion_recable.Draw("P")

  g_pion_CLUE = lib_plotting.fillPlotError(energy, pion_values_CLUE, pion_errors_CLUE)
  g_pion_CLUE.SetMarkerSize(1.5)
  g_pion_CLUE.SetMarkerStyle(26)
  g_pion_CLUE.SetMarkerColor(ROOT.kAzure+2)
  g_pion_CLUE.SetLineColor(ROOT.kAzure+2) 
  g_pion_CLUE.Draw("P")

  g_photon_recable = lib_plotting.fillPlotError(energy, photon_values_recable, photon_errors_recable)
  g_photon_recable.SetMarkerSize(1.5)
  g_photon_recable.SetMarkerStyle(20)
  g_photon_recable.SetMarkerColor(ROOT.kOrange+1)
  g_photon_recable.SetLineColor(ROOT.kOrange+1)
  g_photon_recable.SetLineWidth(2) 
  g_photon_recable.Draw("P")

  g_photon_CLUE = lib_plotting.fillPlotError(energy, photon_values_CLUE, photon_errors_CLUE)
  g_photon_CLUE.SetMarkerSize(1.5)
  g_photon_CLUE.SetMarkerStyle(24)
  g_photon_CLUE.SetMarkerColor(ROOT.kOrange+2)
  g_photon_CLUE.SetLineColor(ROOT.kOrange+2)
  g_photon_CLUE.Draw("P")

  leg.SetHeader("PU = 0")
  leg.AddEntry(g_photon_recable, "Single-#gamma, Rec/able", "P")
  leg.AddEntry(g_pion_recable, "Single-#pi^{+/-}, Rec/able", "P")
  leg.AddEntry(g_photon_CLUE, "Single-#gamma, Clustered", "P")
  leg.AddEntry(g_pion_CLUE, "Single-#pi^{+/-}, Clustered", "P")
  leg.Draw("same")

  if plotRatio :
    p2.cd();
    pion_ratio = lib_plotting.fillPlotRatio(energy, pion_values_recable, pion_values_CLUE, pion_errors_recable, pion_errors_CLUE) 
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
    #Draw only axis is needed to draw line under the markers
    pion_ratio.GetHistogram().Draw("AXIS")
  
    c.Update()
    lineRatio = ROOT.TLine(p2.GetUxmin(), 1., p2.GetUxmax(), 1.)
    lineRatio.SetLineStyle(2)
    lineRatio.SetLineColor(ROOT.kGray+1)
    lineRatio.Draw("same")
  
    pion_ratio.Draw("P");
  
    photon_ratio = lib_plotting.fillPlotRatio(energy, photon_values_recable, photon_values_CLUE, photon_errors_recable, photon_errors_CLUE) 
    photon_ratio.SetMarkerSize(1.5)
    photon_ratio.SetMarkerStyle(24)
    photon_ratio.SetMarkerColor(ROOT.kOrange+2)
    photon_ratio.SetLineColor(ROOT.kOrange+2)
    photon_ratio.SetLineWidth(2)
    photon_ratio.Draw("P");

  CMS_lumi.CMS_lumi(c, iPeriod, iPos)

  c.Draw()
  lib_plotting.savePlot(c, "ACAT2021/plot"+variable)
  return

acceptedOps = ["ratio", "difference"]
def plotOneOperation(energy,
                     photon_values_recable, photon_errors_recable, photon_values_CLUE, photon_errors_CLUE,
                     pion_values_recable, pion_errors_recable, pion_values_CLUE, pion_errors_CLUE,
                     electron_values_recable, electron_errors_recable, electron_values_CLUE, electron_errors_CLUE,
                     kaon_values_recable, kaon_errors_recable, kaon_values_CLUE, kaon_errors_CLUE,
                     variable="Resolution", operation = "ratio"):
  if operation not in acceptedOps:
    print("ERROR:Plotting %s not defined."%(operation))
    return
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

  leg = TLegend(0.30,0.20,0.9,0.45)
  leg.SetNColumns(2)
  leg.SetTextSize(0.03 / topSize)

  pion_operation = lib_plotting.fillPlotRatio(energy, pion_values_CLUE, pion_values_recable, pion_errors_CLUE, pion_errors_recable)
  if variable == "Resolution":
    if operation == "ratio":
      pion_operation.GetYaxis().SetTitle("#sigma_{rel,E_{CLUE}}/#sigma_{rel,E_{Rec/able}}")
      pion_operation.SetMinimum(0.5)
      pion_operation.SetMaximum(1.5)
    elif operation == "difference":
      pion_operation = lib_plotting.fillPlotDifference(energy, pion_values_CLUE, pion_values_recable, pion_errors_CLUE, pion_errors_recable)
      pion_operation.GetYaxis().SetTitle("#sigma_{E_{CLUE}}/E_{CLUE}-#sigma_{E_{Rec/able}}/E_{Rec/able}")
      pion_operation.SetMinimum(-0.20)
      pion_operation.SetMaximum(+0.20)
      pion_operation.GetYaxis().SetNdivisions(205)

  if variable == "Response":
    if operation == "ratio":
      pion_operation.GetYaxis().SetTitle("E_{CLUE}/E_{Rec/able}")
      pion_operation.SetMinimum(0.85)
      pion_operation.SetMaximum(1.1)
    elif operation == "difference":
      pion_operation = lib_plotting.fillPlotDifference(energy, pion_values_CLUE, pion_values_recable, pion_errors_CLUE, pion_errors_recable)
      pion_operation.GetYaxis().SetTitle("(E_{CLUE}-E_{Rec/able})/E_{GEN}")
      pion_operation.SetMinimum(-0.10)
      pion_operation.SetMaximum(+0.05)
      pion_operation.GetYaxis().SetNdivisions(205)

  pion_operation.GetXaxis().SetTitle("E_{GEN} [GeV]")
  pion_operation.GetXaxis().SetTitleOffset( 1.00 )
  pion_operation.SetMarkerSize(1.5)
  pion_operation.SetMarkerStyle(22)
  pion_operation.SetMarkerColor(ROOT.kBlue+2)
  pion_operation.SetLineColor(ROOT.kBlue+1)
  pion_operation.SetLineWidth(2)
  #Draw only axis is needed to draw line under the markers
  pion_operation.GetHistogram().Draw("AXIS")

  c.Update()
  line_operation = ROOT.TLine(c.GetUxmin(), 1., c.GetUxmax(), 1.)
  if operation == "difference":
    line_operation = ROOT.TLine(c.GetUxmin(), 0., c.GetUxmax(), 0.)
  line_operation.SetLineStyle(2)
  line_operation.SetLineColor(ROOT.kGray+1)
  line_operation.Draw("same")

  pion_operation.Draw("P");

  photon_operation = lib_plotting.fillPlotRatio(energy, photon_values_CLUE, photon_values_recable, photon_errors_CLUE, photon_errors_recable)
  if operation == "difference":
    photon_operation = lib_plotting.fillPlotDifference(energy, photon_values_CLUE, photon_values_recable, photon_errors_CLUE, photon_errors_recable)
  photon_operation.SetMarkerSize(1.5)
  photon_operation.SetMarkerStyle(21)
  photon_operation.SetMarkerColor(ROOT.kOrange+2)
  photon_operation.SetLineColor(ROOT.kOrange+2)
  photon_operation.SetLineWidth(2)
  photon_operation.Draw("P");

  electron_operation = lib_plotting.fillPlotRatio(energy, electron_values_CLUE, electron_values_recable, electron_errors_CLUE, electron_errors_recable)
  if operation == "difference":
    electron_operation = lib_plotting.fillPlotDifference(energy, electron_values_CLUE, electron_values_recable, electron_errors_CLUE, electron_errors_recable)
  electron_operation.SetMarkerSize(1.5)
  electron_operation.SetMarkerStyle(20)
  electron_operation.SetMarkerColor(ROOT.kOrange-4)
  electron_operation.SetLineColor(ROOT.kOrange-4)
  electron_operation.SetLineWidth(2)
  electron_operation.Draw("P");

  kaon_operation = lib_plotting.fillPlotRatio(energy, kaon_values_CLUE, kaon_values_recable, kaon_errors_CLUE, kaon_errors_recable)
  if operation == "difference":
    kaon_operation = lib_plotting.fillPlotDifference(energy, kaon_values_CLUE, kaon_values_recable, kaon_errors_CLUE, kaon_errors_recable)
  kaon_operation.SetMarkerSize(2.0)
  kaon_operation.SetMarkerStyle(33)
  kaon_operation.SetMarkerColor(ROOT.kAzure-4)
  kaon_operation.SetLineColor(ROOT.kAzure-4)
  kaon_operation.SetLineWidth(2)
  kaon_operation.Draw("P");

  leg.SetHeader("PU = 0")
  leg.AddEntry(photon_operation, "Single-#gamma", "PL")
  leg.AddEntry(electron_operation, "Single-e^{+/-}", "PL")
  leg.AddEntry(pion_operation, "Single-#pi^{+/-}", "PL")
  leg.AddEntry(kaon_operation, "Single-K_{L}^{0}", "PL")
  leg.Draw("same")

  CMS_lumi.CMS_lumi(c, iPeriod, iPos)

  c.Draw()
  lib_plotting.savePlot(c, "ACAT2021/plot"+variable+"_" + operation)
  return

def plotResolution():
  energy = lib_plotting.extractValues("ACAT2021/data_singlephoton.csv", "energy")
  energyPi = lib_plotting.extractValues("ACAT2021/data_singlepion.csv", "energy")
  lib_plotting.isSameArray(energy, "energyPhoton", energyPi, "energyPion")

  photon_values_recable, photon_errors_recable = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlephoton.csv", "recable_reso", "recable_reso_error")
  photon_values_CLUE, photon_errors_CLUE = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlephoton.csv", "CLUE_reso", "CLUE_reso_error")
  pion_values_recable, pion_errors_recable = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlepion.csv", "recable_reso", "recable_reso_error")
  pion_values_CLUE, pion_errors_CLUE = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlepion.csv", "CLUE_reso", "CLUE_reso_error")
  plotValues(energy, 
             photon_values_recable, photon_errors_recable, photon_values_CLUE, photon_errors_CLUE, 
             pion_values_recable, pion_errors_recable, pion_values_CLUE, pion_errors_CLUE, 
             "Resolution", False)

  energyEle = lib_plotting.extractValues("ACAT2021/data_singleelectron.csv", "energy")
  lib_plotting.isSameArray(energy, "energyPhoton", energyEle, "energyEle")

  electron_values_recable, electron_errors_recable = lib_plotting.extractValuesWithErrors("ACAT2021/data_singleelectron.csv", "recable_reso", "recable_reso_error")
  electron_values_CLUE, electron_errors_CLUE = lib_plotting.extractValuesWithErrors("ACAT2021/data_singleelectron.csv", "CLUE_reso", "CLUE_reso_error")

  energyKaon = lib_plotting.extractValues("ACAT2021/data_singlekaon.csv", "energy")
  lib_plotting.isSameArray(energy, "energyPhoton", energyKaon, "energyKaon")

  kaon_values_recable, kaon_errors_recable = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlekaon.csv", "recable_reso", "recable_reso_error")
  kaon_values_CLUE, kaon_errors_CLUE = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlekaon.csv", "CLUE_reso", "CLUE_reso_error")

  for ops in ["ratio", "difference"]:
    plotOneOperation(energy,
                     photon_values_recable, photon_errors_recable, photon_values_CLUE, photon_errors_CLUE,
                     pion_values_recable, pion_errors_recable, pion_values_CLUE, pion_errors_CLUE,
                     electron_values_recable, electron_errors_recable, electron_values_CLUE, electron_errors_CLUE,
                     kaon_values_recable, kaon_errors_recable, kaon_values_CLUE, kaon_errors_CLUE,
                     "Resolution", ops)

def plotResponse():
  energy = lib_plotting.extractValues("ACAT2021/data_singlephoton.csv", "energy")
  energyPi = lib_plotting.extractValues("ACAT2021/data_singlepion.csv", "energy")
  lib_plotting.isSameArray(energy, "energyPhoton", energyPi, "energyPion")

  photon_values_recable, photon_errors_recable = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlephoton.csv", "recable_resp", "recable_resp_error")
  photon_values_CLUE, photon_errors_CLUE = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlephoton.csv", "CLUE_resp", "CLUE_resp_error")
  pion_values_recable, pion_errors_recable = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlepion.csv", "recable_resp", "recable_resp_error")
  pion_values_CLUE, pion_errors_CLUE = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlepion.csv", "CLUE_resp", "CLUE_resp_error")

  plotValues(energy, 
             photon_values_recable, photon_errors_recable, photon_values_CLUE, photon_errors_CLUE, 
             pion_values_recable, pion_errors_recable, pion_values_CLUE, pion_errors_CLUE, 
             "Response", False)

  energyEle = lib_plotting.extractValues("ACAT2021/data_singleelectron.csv", "energy")
  lib_plotting.isSameArray(energy, "energyPhoton", energyEle, "energyEle")

  electron_values_recable, electron_errors_recable = lib_plotting.extractValuesWithErrors("ACAT2021/data_singleelectron.csv", "recable_resp", "recable_resp_error")
  electron_values_CLUE, electron_errors_CLUE = lib_plotting.extractValuesWithErrors("ACAT2021/data_singleelectron.csv", "CLUE_resp", "CLUE_resp_error")

  energyKaon = lib_plotting.extractValues("ACAT2021/data_singlekaon.csv", "energy")
  lib_plotting.isSameArray(energy, "energyPhoton", energyKaon, "energyKaon")

  kaon_values_recable, kaon_errors_recable = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlekaon.csv", "recable_resp", "recable_resp_error")
  kaon_values_CLUE, kaon_errors_CLUE = lib_plotting.extractValuesWithErrors("ACAT2021/data_singlekaon.csv", "CLUE_resp", "CLUE_resp_error")

  for ops in ["ratio", "difference"]:
    plotOneOperation(energy,
                     photon_values_recable, photon_errors_recable, photon_values_CLUE, photon_errors_CLUE,
                     pion_values_recable, pion_errors_recable, pion_values_CLUE, pion_errors_CLUE,
                     electron_values_recable, electron_errors_recable, electron_values_CLUE, electron_errors_CLUE,
                     kaon_values_recable, kaon_errors_recable, kaon_values_CLUE, kaon_errors_CLUE,
                     "Response", ops)

if __name__ == "__main__":
  plotResolution()
  plotResponse()
