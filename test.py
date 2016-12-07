import os

from sklearn import mixture

from bspline.bspline import *
from empirical.num_of_strokes import *
from normlize import data_normlize, substroke_normlize
from plot.plot_utils import *
from utils import utils
from scipy import stats
import numpy as np

import scipy.stats as stats
alpha = 5
loc = 0
beta = 0.005
data = stats.gamma.rvs(alpha, loc=loc, scale=beta, size=100)
print(data)

fit_alpha, fit_loc, fit_beta=stats.gamma.fit(data,floc=0)
print(fit_alpha, fit_loc, fit_beta)

np.savetxt("filename.txt",data)
d=np.loadtxt("filename.txt")
print d