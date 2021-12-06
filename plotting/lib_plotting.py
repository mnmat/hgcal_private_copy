from ROOT import TGraphErrors

import os
import math
import pandas as pd
import numpy as np

def extractValues(fileName, variable):
  df = pd.read_csv(fileName)
  return df[variable]

def extractValuesWithErrors(fileName, variable, variableErr):
  df = pd.read_csv(fileName)
  return df[variable], df[variableErr]

def isSameArray(arr1, arr1Name, arr2, arr2Name):
  if not np.array_equal(arr1, arr2) :
    print("ERROR: Arrays (%s and %s) differ between data files!"%(arr1Name, arr2Name))
    exit()
  else:
    return

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
    graph.SetPointError(NPOINTS, 0, ierr*iy2/iy1)
    NPOINTS = NPOINTS + 1

  return graph

def fillPlotDifference(x, y1, y2, err1, err2):

  graph = TGraphErrors()
  NPOINTS = 0
  for (ix, iy1, iy2, ierr1, ierr2) in zip(x, y1, y2, err1, err2): 
    graph.SetPoint(NPOINTS, ix, iy1-iy2)
    ierr = math.sqrt(ierr1*ierr1 + ierr2*ierr2)
    graph.SetPointError(NPOINTS, 0, ierr)
    NPOINTS = NPOINTS + 1

  return graph

def savePlot(c, name):

  c.SaveAs(name+".eps", "eps")
  c.SaveAs(name+".C", "C")
  # The png version created using the canvas does not contain the CMS line. No idea why.
  command = "convert -density 600x600 " + name + ".eps " + name + ".png"
  print("%s.eps has been convented in PNG"%name)
  os.system(command)

  return
