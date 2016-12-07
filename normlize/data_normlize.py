from __future__ import division
import numpy as np
def normlize_data(data,size=150):
    for idx1 in range(len(data)):
        for idx2 in range(len(data[idx1])):
            tmp=[]
            for idx3 in range(len(data[idx1][idx2])):
                tmp+=data[idx1][idx2][idx3]
            tmp=np.array(tmp)
            mean=np.mean(tmp[:,:2],0)
            max=np.max(tmp[:,:2],0)
            min=np.min(tmp[:,:2],0)
            true_size=max-min
            scale=np.max(true_size/size)
            for idx3 in range(len(data[idx1][idx2])):
                tmp=np.array(data[idx1][idx2][idx3],dtype=float)
                tmp[:, :2]=(tmp[:,:2]-mean)/scale
                tmp[:,3]=np.sqrt(tmp[:,3]/(scale**2))
                data[idx1][idx2][idx3]=tmp
