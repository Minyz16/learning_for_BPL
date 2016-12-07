from __future__ import division
import scipy.stats as stats
import numpy as np

def learn_theta(gmm,all_cpts,num_components,scale_norm_factor):
    groupdata={}
    for i in range(num_components):
        groupdata[i]=[]
    for cpts in all_cpts:
        tmp = np.array([cpts['scale'], cpts['scale']])
        tmp2 = cpts['data'].reshape([1, -1])
        feature = np.concatenate([tmp2[0], tmp / scale_norm_factor])

        label=gmm.predict(feature.reshape(1, -1))[0]
        scale=cpts['scale']
        invscale=1/scale

        groupdata[label].append(invscale)
    rst=np.zeros([num_components,2])

    for i in range(num_components):
        data=groupdata[i]
        a, loc, b = stats.gamma.fit(data, floc=0)
        rst[i]=[a,b]

    return rst


