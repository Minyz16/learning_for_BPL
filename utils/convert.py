import scipy.io
import matplotlib.pyplot as plt
import numpy as np
matfile='../data/library.mat'
data=scipy.io.loadmat(file_name=matfile)
data.viewkeys()
