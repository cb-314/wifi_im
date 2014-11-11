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


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="analyze pickle files generated by wifi_im")
  parser.add_argument("filenames", help="pickle files", nargs="+")

  args = parser.parse_args()
  
  rcParams["font.family"] = "serif"
  rcParams["xtick.labelsize"] = 8
  rcParams["ytick.labelsize"] = 8
  rcParams["axes.labelsize"] = 8
  rcParams["axes.titlesize"] = 8

  xyr = []
  walls = []
  for filename in args.filenames:
    with open(filename, "rb") as file_desc:
      data = cPickle.load(file_desc)
      if "walls" in data.keys():
        walls = data["walls"]
      xyr.extend(data["xyr"])
  plt.hexbin([x for t, x, y, r in xyr], [y for t, x, y, r in xyr], [r for t, x, y, r in xyr], gridsize=40, cmap=plt.get_cmap("gnuplot2"), vmin=-80, vmax=-20, extent=(-12, 2, -15, 20))
  plt.plot([x for x,y in walls], [y for x,y in walls], "k,")
  plt.xticks([-10, -5, 0])
  plt.gca().set_xlim((-12, 2))
  plt.gca().set_xlabel("x [m]")
  plt.gca().set_ylim((-15, 20))
  plt.gca().set_ylabel("y [m]")
  cbar = plt.colorbar()
  cbar.set_label("mean rssi [dB]")
  plt.gcf().set_size_inches((4, 8))
  plt.savefig("rssi_hexbin.pdf", bbox_inches="tight")
  plt.clf()
  plt.hexbin([y for t, x, y, r in xyr], [x for t, x, y, r in xyr], [r for t, x, y, r in xyr], gridsize=40, cmap=plt.get_cmap("gnuplot2"), vmin=-80, vmax=-20, extent=(-15, 20, -12, 2))
  plt.plot([y for x,y in walls], [x for x,y in walls], "k,")
  plt.yticks([-10, -5, 0])
  plt.gca().set_ylim((-12, 2))
  plt.gca().set_ylabel("x [m]")
  plt.gca().set_xlim((-15, 20))
  plt.gca().set_xlabel("y [m]")
  cbar = plt.colorbar()
  cbar.set_label("mean rssi [dB]")
  plt.gcf().set_size_inches((14, 4))
  plt.savefig("rssi_hexbin_r.pdf", bbox_inches="tight")
