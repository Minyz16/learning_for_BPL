import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

#substroke=[[x1,y1], [x2,y2], ...]
#1 pixel distance, zero mean, common scale, discard useless information

def normlize(substroke,norm_dis,plot=False):
    substroke = np.array(substroke)
    dis = np.sqrt(substroke[:, 3])
    dis[0] = 0
    cumdis = np.cumsum(dis)
    start_dis = cumdis[0]
    end_dis = cumdis[-1]
    x = cumdis[:]
    nint = max(round(end_dis / norm_dis), 2)
    xi = np.linspace(start_dis, end_dis, nint)
    f_linear1 = interpolate.interp1d(x, substroke[:, 0])
    f_linear2 = interpolate.interp1d(x, substroke[:, 1])
    y1 = f_linear1(xi)
    y2 = f_linear2(xi)
    yi = np.array([y1, y2]).transpose()
    yi=yi-np.mean(yi,0)
    scale_factor=max(np.max(yi,0)-np.min(yi,0))
    yi=yi/scale_factor
    if plot:
        ax=plt.subplot(1,2,1)
        plt.plot(substroke[:, 0], -substroke[:, 1], "*")
        plt.sca(ax)
        ax=plt.subplot(1,2,2)
        plt.plot(yi[:,0], -yi[:,1], ".")
        plt.sca(ax)
        plt.show()
    return yi