# Last update with 12_0_1_pre4
# Command example
# python3 plotting_metrics.py --filesin /data2/user/ebrondol/HGCal/production/CMSSW_12_0_0_pre3/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e10GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_0_0_pre3/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e20GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_0_0_pre3/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e50GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_0_0_pre3/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e100GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_0_0_pre3/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e200GeV__nopu.root /data2/user/ebrondol/HGCal/production/CMSSW_12_0_0_pre3/vanilla//singlephoton_closeBy_hgcalCenter/step4/DQM_V0001_R000000001__step4_singlephoton__e300GeV__nopu.root  --folderout vanilla/singlephoton/ --sample "Single-#gamma, PU = 0" --features "10 GeV:94:20" "20 GeV:51:5" "50 GeV:54:26" "100 GeV:64:22" "200 GeV:99:3" "300 GeV:57:23" --iter "Merge:ticlTrackstersMerge:94:20" "TrkEM:ticlTrackstersTrkEM:64:22" "EM:ticlTrackstersEM:99:3" "TrkHAD:ticlTrackstersTrk:57:23" "HAD:ticlTrackstersHAD:30:4"

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import gROOT, TFile, TCanvas, TGraphErrors, TH1F, TLegend, gPad, TLatex, TLine
import json, array
import argparse

def list_with_negatives(value):
  values = value.split(" ")
  print(values)
  return values

#gROOT.Macro("CLICdpStyle.C") 
parser = argparse.ArgumentParser(description='Produce root files with tracking analysis plots')
parser.add_argument('--filesin', nargs='+', help='List of root file used as input')
parser.add_argument('--features', nargs='+', help='List of features used for this input file as label:color:markerStyle (ex. "p_{T} = 1 GeV:1:20:False")')
parser.add_argument('--iters', nargs='+', help='List of iterations label:fullName (ex. "EM:ticlMultiClustersFromTrackstersEM")')
parser.add_argument('--folderout', help='Name of output folder')
parser.add_argument('--sample', help="Data sample", type=str)
parser.add_argument('--test', help="Testing the code only with eff plots", action="store_true")
parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
args = parser.parse_args()

TEST = args.test
VERBOSE = args.verbose
if TEST : VERBOSE = True 
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

GRAPHS = []

# From https://twiki.cern.ch/twiki/pub/CMS/Internal/FigGuidelines/myMacro.py.txt
import CMS_lumi, tdrstyle

#set the tdr style
tdrstyle.setTDRStyle() # this changes too many things

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
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
L = 0.12*W_ref
R = 0.04*W_ref

def plotVersusEnergy(label):
  histoname = "globalEfficiencies"
  if VERBOSE : 
    print("> Plotting %s histogram:"%histoname)
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
  #c.SetGrid()
  if not VERBOSE : gROOT.SetBatch(True);

  gPad.Update()
  leg = TLegend(0.60,0.70,0.95,0.90)
  leg.SetNColumns(round(len(LABELS_ITERS)/3))
  leg.SetTextSize(0.03)
  leg.SetHeader(SAMPLE)

  GRAPHS = []
  NPOINTS = []
  for label_iter in LABELS_ITERS :
    graph_iter = TGraphErrors()
    graph_iter.SetName(label_iter)
    GRAPHS.append(graph_iter)
    NPOINTS.append(0)

  if VERBOSE: print("  Input files:")
  for i_en in range(0, len(INPUTFILES)):
    if VERBOSE: print(("  %s"%(INPUTFILES[i_en])))
    beginIdx = INPUTFILES[i_en].find("__e") + 3
    endIdx = INPUTFILES[i_en].find("GeV")
    energy = float(INPUTFILES[i_en][beginIdx:endIdx])
    inputTFile = TFile(INPUTFILES[i_en], "r")
    if inputTFile.IsZombie(): continue
    for i_iter in range(0, len(FULL_ITERS)) :
      histofullname = HISTOPREFIX+'/'+FULL_ITERS[i_iter]+'/TSToCP_linking/'+histoname
      graph = inputTFile.Get(histofullname)
      for ibin in range(0,graph.GetNbinsX()) :
        if graph.GetXaxis().GetBinLabel(ibin) == label:
          #print("%f %f %f"%(energy, graph.GetBinContent(ibin),graph.GetBinError(ibin)))
          if graph.GetBinContent(ibin) == 0.0 :
            GRAPHS[i_iter].SetPoint(NPOINTS[i_iter], energy, graph.GetBinContent(ibin))
            GRAPHS[i_iter].SetPointError(NPOINTS[i_iter], 0.0, graph.GetBinError(ibin))
            NPOINTS[i_iter] = NPOINTS[i_iter] + 1
          else :
            GRAPHS[i_iter].SetPoint(NPOINTS[i_iter], energy, graph.GetBinContent(ibin))
            GRAPHS[i_iter].SetPointError(NPOINTS[i_iter], 0.0, graph.GetBinError(ibin))
            NPOINTS[i_iter] = NPOINTS[i_iter] + 1
        else :
          continue

  for i_gr in range(0, len(LABELS_ITERS)):
    GRAPHS[i_gr].SetMarkerStyle(MARKERS_ITERS[i_gr])
    GRAPHS[i_gr].SetMarkerColor(COLORS_ITERS[i_gr])
    GRAPHS[i_gr].SetLineWidth(2)
    GRAPHS[i_gr].SetLineColor(COLORS_ITERS[i_gr])
    GRAPHS[i_gr].SetLineStyle(i_gr+1)
    GRAPHS[i_gr].SetMarkerSize(1.3)
    if i_gr == 0 :
      GRAPHS[i_gr].SetMaximum(1.5)
      GRAPHS[i_gr].SetMinimum(0.0)
      GRAPHS[i_gr].GetYaxis().SetLabelSize(0.05)
      GRAPHS[i_gr].GetXaxis().SetLabelSize(0.05)
      GRAPHS[i_gr].GetYaxis().SetTitleSize(0.07)
      GRAPHS[i_gr].GetXaxis().SetTitleSize(0.07)
      if label == "effic_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Efficiency")
      elif label == "purity_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Purity")
      elif label == "duplicate_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Duplicate Rate")
      elif label == "fake_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Fake Rate")
      elif label == "merge_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Merge Rate")
      GRAPHS[i_gr].GetYaxis().SetTitleOffset(0.8)
      GRAPHS[i_gr].GetXaxis().SetTitleOffset(0.9)
      GRAPHS[i_gr].GetXaxis().SetTitle("E_{GEN} [GeV]")
      GRAPHS[i_gr].GetHistogram().Draw("AXIS")
      c.Update()
      line = ROOT.TLine(c.GetUxmin(), 1., c.GetUxmax(), 1.)
      line.SetLineStyle(2)
      line.SetLineColor(ROOT.kGray+1)
      line.Draw("same")

    GRAPHS[i_gr].Draw("PLsame")
    leg.AddEntry(GRAPHS[i_gr], LABELS_ITERS[i_gr], "PL")

    inputTFile.Close()

  gPad.Update()
  leg.Draw("same")

  CMS_lumi.CMS_lumi(c, iPeriod, iPos)

  c.Draw()
  nameOutputPlot = OUTPUTFOLDER+histoname+"_"+label+"_vsEnergy"
  c.SaveAs(nameOutputPlot+".eps","eps")
  c.SaveAs(nameOutputPlot+".png","png")
  c.SaveAs(nameOutputPlot+".C","C")

  return

def plotAllMetrics(labels, inputFile):
  histoname = "globalEfficiencies"
  if VERBOSE : print(("> Plotting %s histogram:"%histoname))
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
  if not VERBOSE : gROOT.SetBatch(True);

  gPad.Update()
  leg = TLegend(0.40,0.70,0.95,0.90)
  leg.SetTextSize(0.03)
  leg.SetHeader(SAMPLE)
  leg.SetNColumns(round(len(LABELS_ITERS)/2))

  GRAPHS = []
  NPOINTS = []
  for i_iter in LABELS_ITERS :
    graph_iter = TH1F(i_iter, i_iter, len(labels), 0., len(labels))
    GRAPHS.append(graph_iter)
    NPOINTS.append(0)

  if VERBOSE: 
    print("  Input files:")
    print("  %s"%(inputFile))
  for i_iter in range(0, len(LABELS_ITERS)) :
    inputTFile = TFile(inputFile, "r")
    if inputTFile.IsZombie(): continue
    histofullname = HISTOPREFIX+'/'+FULL_ITERS[i_iter]+'/TSToCP_linking/'+histoname
    graph = inputTFile.Get(histofullname)
    for label in range(0, len(labels)) :
      for ibin in range(0,graph.GetNbinsX()) :
        if graph.GetXaxis().GetBinLabel(ibin) == labels[label]:
          content = graph.GetBinContent(ibin)
          if graph.GetBinContent(ibin) == 0.0:
            content = 0.000001
          GRAPHS[i_iter].SetBinContent(label+1, content)
          GRAPHS[i_iter].SetBinError(label+1, graph.GetBinError(ibin))
          GRAPHS[i_iter].GetXaxis().SetBinLabel(label+1,"%s" % labels[label] )
        else :
          continue

  for i_gr in range(0, len(LABELS_ITERS)):
    offset = - 0.5 + 1/(len(LABELS_ITERS)+1)*(i_gr+1)
    GRAPHS[i_gr].SetBarOffset(offset)
    GRAPHS[i_gr].SetMarkerStyle(MARKERS_ITERS[i_gr])
    GRAPHS[i_gr].SetMarkerColor(COLORS_ITERS[i_gr])
    GRAPHS[i_gr].SetLineColor(COLORS_ITERS[i_gr])
    GRAPHS[i_gr].SetLineStyle(i_gr+1)
    GRAPHS[i_gr].SetMarkerSize(1.3)
    if i_gr == 0 :
      GRAPHS[i_gr].SetMaximum(1.5)
      GRAPHS[i_gr].SetMinimum(0.0)
      GRAPHS[i_gr].SetLabelSize(0.07)
      GRAPHS[i_gr].GetYaxis().SetLabelSize(0.05)
      GRAPHS[i_gr].GetXaxis().SetLabelSize(0.05)
      GRAPHS[i_gr].GetYaxis().SetTitleSize(0.07)
      GRAPHS[i_gr].GetXaxis().SetTitleSize(0.07)
      if label == "effic_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Efficiency")
      elif label == "purity_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Purity")
      elif label == "duplicate_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Duplicate Rate")
      elif label == "fake_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Fake Rate")
      elif label == "merge_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Merge Rate")
      GRAPHS[i_gr].GetYaxis().SetTitleOffset(0.8)
      GRAPHS[i_gr].GetXaxis().SetTitleOffset(0.9)

      GRAPHS[i_gr].Draw("PE0")
    else :
      GRAPHS[i_gr].Draw("PE0same")

    leg.AddEntry(GRAPHS[i_gr], LABELS_ITERS[i_gr], "P")

  leg.Draw("same")

#  CMS_lumi.CMS_lumi(c, iPeriod, iPos)

  c.Draw()
  nameOutputPlot = OUTPUTFOLDER+"_MetricsVsIter"
  c.SaveAs(nameOutputPlot+".eps","eps")
  c.SaveAs(nameOutputPlot+".png","png")

  return

def plotDifferentIters(label):
  histoname = "globalEfficiencies"

  if VERBOSE : print(("> Plotting %s histogram:"%histoname))
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
  if not VERBOSE : gROOT.SetBatch(True);

  gPad.Update()
  leg = TLegend(0.40,0.70,0.95,0.90)
  leg.SetTextSize(0.03)
  leg.SetHeader(SAMPLE)
  leg.SetNColumns(round(len(LABELS_ITERS)/2))

  GRAPHS = []
  NPOINTS = []
  for label_en in LABELS_EN :
    graph = TH1F(label_en, label_en, len(FULL_ITERS), 0., len(FULL_ITERS))
    GRAPHS.append(graph)
    NPOINTS.append(0)

  if VERBOSE: print("  Input files:")
  for i_en in range(0, len(LABELS_EN)):
    if VERBOSE: print(("  %s"%(INPUTFILES[i_en])))
    inputTFile = TFile(INPUTFILES[i_en], "r")
    if inputTFile.IsZombie(): continue
    for i_iter in range(0, len(FULL_ITERS)) :
      histofullname = HISTOPREFIX+'/'+FULL_ITERS[i_iter]+'/TSToCP_linking/'+histoname
      graph = inputTFile.Get(histofullname)
      for ibin in range(0,graph.GetNbinsX()) :
        if graph.GetXaxis().GetBinLabel(ibin) == label:
          GRAPHS[i_en].SetBinContent(i_iter+1, graph.GetBinContent(ibin))
          GRAPHS[i_en].SetBinError(i_iter+1, graph.GetBinError(ibin))
          GRAPHS[i_en].GetXaxis().SetBinLabel(i_iter+1,"%s" % LABELS_ITERS[i_iter] )
        else :
          continue

  for i_gr in range(0, len(LABELS_EN)):
    offset = - 0.5 + 1/(len(LABELS_EN)+1)*(i_gr+1)
    GRAPHS[i_gr].SetBarOffset(offset)
    GRAPHS[i_gr].SetMarkerStyle(MARKERS_EN[i_gr])
    GRAPHS[i_gr].SetMarkerColor(COLORS_EN[i_gr])
    GRAPHS[i_gr].SetLineWidth(len(INPUTFILES)-i_gr)
    GRAPHS[i_gr].SetLineColor(COLORS_EN[i_gr])
    GRAPHS[i_gr].SetLineStyle(i_gr+1)
    GRAPHS[i_gr].SetMarkerSize(1.3)
    if i_gr == 0 :
      GRAPHS[i_gr].SetMaximum(1.5)
      GRAPHS[i_gr].SetMinimum(0.0)
      GRAPHS[i_gr].SetLabelSize(0.07)
      GRAPHS[i_gr].GetYaxis().SetLabelSize(0.05)
      GRAPHS[i_gr].GetXaxis().SetLabelSize(0.05)
      GRAPHS[i_gr].GetYaxis().SetTitleSize(0.07)
      GRAPHS[i_gr].GetXaxis().SetTitleSize(0.07)
      if label == "effic_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Efficiency")
      elif label == "purity_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Purity")
      elif label == "duplicate_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Duplicate Rate")
      elif label == "fake_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Fake Rate")
      elif label == "merge_eta":
        GRAPHS[i_gr].GetYaxis().SetTitle("Tracksters Merge Rate")
      GRAPHS[i_gr].GetYaxis().SetTitleOffset(0.8)
      GRAPHS[i_gr].GetXaxis().SetTitleOffset(0.9)

      GRAPHS[i_gr].Draw("PE0")
    else :
      GRAPHS[i_gr].Draw("PE0same")

    leg.AddEntry(GRAPHS[i_gr], LABELS_EN[i_gr], "P")

  leg.Draw("same")

  if LABELS_ITERS[-1] == "Merge":
    vert = TLine(len(FULL_ITERS)-1, gPad.GetUymin(), len(FULL_ITERS)-1, gPad.GetUymax())
    vert.Draw()

  CMS_lumi.CMS_lumi(c, iPeriod, iPos)

  c.Draw()
  nameOutputPlot = OUTPUTFOLDER+histoname+"_"+label+"_vsIter"
  c.SaveAs(nameOutputPlot+".eps","eps")
  c.SaveAs(nameOutputPlot+".png","png")

  return

if __name__ == "__main__":
  labels = ["effic_eta", "purity_eta", "duplicate_eta", "fake_eta", "merge_eta"]
  if TEST :
    labels = ["effic_eta"]
  plotAllMetrics(labels, INPUTFILES[0])
  for lab in labels:
    plotDifferentIters(lab)
    plotVersusEnergy(lab)
