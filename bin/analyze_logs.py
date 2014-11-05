#!/usr/bin/env python

import cPickle
import sys
from matplotlib import pyplot as plt
from matplotlib import rcParams
import matplotlib.gridspec as gridspec
import numpy as np
import math
import argparse
import copy
import random
import wifi_im

def moving_average(x, y, window_size):
  bin_edges = np.arange(min(x), max(x), window_size)
  indices = np.digitize(x, bin_edges)
  bins = [[] for i in range(len(bin_edges))]
  for i in range(len(x)):
    bins[indices[i]-1].append(y[i])
  xx = [(bin_edges[i-1] + bin_edges[i])/2.0 for i in range(1, len(bin_edges))]
  xx.append((bin_edges[-1]+max(x))/2.0)
  yy = [np.mean(contents) for contents in bins]
  return xx, yy


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="analyze pickle files generated by wifi_im")
  parser.add_argument("filenames", help="pickle files", nargs="+")
  
  args = parser.parse_args()
  
  rcParams["font.family"] = "serif"
  rcParams["xtick.labelsize"] = 8
  rcParams["ytick.labelsize"] = 8
  rcParams["axes.labelsize"] = 8
  rcParams["axes.titlesize"] = 8

  for filename in args.filenames:
    with open(filename, "rb") as file_desc:
      data = cPickle.load(file_desc)
      plt.clf()
      gs = gridspec.GridSpec(3, 1)
      
      plt.subplot(gs[:2, 0])
      plt.plot([x for x,y in data["walls"]], [y for x,y in data["walls"]], "k,")
      plt.plot([x for t,x,y,r in data["xyr"]], [y for t,x,y,r in data["xyr"]], "b-")
      plt.plot(0.1, -1.2, "*r")
      plt.xticks([-10, -5, 0])
      plt.gca().set_xlabel("x [m]")
      plt.gca().set_ylabel("y [m]")
      
      plt.subplot(gs[2,0])
      lengths = [math.hypot(data["xyr"][i][1] - data["xyr"][i-1][1], data["xyr"][i][2]-data["xyr"][i][2]) for i in range(1, len(data["xyr"]))]
      dist = [0.0]
      for length in lengths:
        dist.append(dist[-1]+length)
      xx, yy = moving_average(dist, [r for t,x,y,r in data["xyr"]], 1.0)
      plt.plot(dist, [r for t,x,y,r in data["xyr"]], "b,")
      plt.plot(xx, yy, "k-")
      plt.gca().set_ylim((-80, -30))
      plt.gca().set_xlabel("distance travelled [m]")
      plt.gca().set_ylabel("rssi [dB]")
      
      plt.gcf().set_size_inches((3, 9))
      plt.savefig(filename[filename.rindex("/")+1:filename.rindex(".")]+".jpg", dpi=100, bbox_inches="tight")
