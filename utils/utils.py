from __future__ import division
import numpy as np

def compute_average_dis(strokes):
    total_dis=0
    total_interval_count=0
    for stroke in strokes:
        stroke=np.array(stroke)
        tmp=np.sum(stroke,0)
        total_dis+=tmp[3]
        total_interval_count+=(stroke.shape[0]-1)
    return total_dis/total_interval_count

def compute_accumulate_dis(stroke):
    if(len(stroke) <= 1):
        return 0
    rub=np.array(stroke)
    rub[0,3]=0
    tmp=np.sum(rub,0)
    return tmp[3]
