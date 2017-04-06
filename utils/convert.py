import scipy.io
import numpy as np
mymat='../data/mylib.mat'
mydict={}
mydict['freq']=np.loadtxt('../data/freq.txt')
mydict['logStart']=np.loadtxt('../data/logStart.txt')
mydict['logT']=np.loadtxt('../data/logT.txt')
mydict['mixprob']=np.loadtxt('../data/mixprob.txt')
mydict['mu']=np.loadtxt('../data/mu.txt')
mydict['pkappa']=np.loadtxt('../data/pkappa.txt')
mydict['pmat_nsub']=np.loadtxt('../data/pmat_nsub.txt')
mydict['sigma']=np.loadtxt('../data/sigma.txt')
mydict['theta']=np.loadtxt('../data/theta.txt')
mydict['vsd']=np.loadtxt('../data/vsd.txt')
scipy.io.savemat(mymat,mydict)

