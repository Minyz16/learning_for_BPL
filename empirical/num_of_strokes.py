from __future__ import division
import numpy as np
def compute_num_strokes(data,maxsize=10):
    rst=np.ones([maxsize,1]) * 0.01
    for char in data:
        for person in char:
            if(len(person) <= maxsize):
                rst[len(person)-1,0]+=1
    return rst/np.sum(rst)

def compute_num_substrokes(data,maxsize=[10,10]):
    rst = np.ones(maxsize) * 0.01
    for char in data:
        for person in char:
            if(len(person) <= maxsize[0]):
                for stroke in person:
                    if (len(stroke) <= maxsize[1]):
                        rst[len(person)-1,len(stroke)-1]+=1
    return rst/np.sum(rst,1,keepdims=True)

def compute_logstart(gmm,all_cpts,num_components,scale_norm_factor):
    rst=np.ones([num_components,1]) * 0.01
    for cpts in all_cpts:
        id=cpts['id']
        if id[2] == 0 and id[3] == 0:    #the first stroke's first substroke
            tmp = np.array([cpts['scale'], cpts['scale']])
            tmp2 = cpts['data'].reshape([1, -1])
            feature = np.concatenate([tmp2[0], tmp/scale_norm_factor])
            rst[gmm.predict(feature.reshape(1,-1))[0]]+=1
    return np.log(rst / np.sum(rst))


def compute_logT(gmm,all_cpts,num_components,scale_norm_factor):
    #print len(all_cpts)
    rst=np.ones([num_components,num_components]) * 0.01
    old_class=None
    old_stroke_id=-1
    old_substroke_id=-1
    old_person_id=-1
    old_char_id=-1
    change=0
    for cpts in all_cpts:
        id = cpts['id']
        if(id[0] != old_char_id or id[1] != old_person_id or id[2] != old_stroke_id):
            #raw_input("pause")
            #print id[0], old_char_id, id[1],old_person_id, id[2],old_stroke_id

            old_char_id = id[0]
            old_person_id = id[1]
            old_stroke_id = id[2]
            old_substroke_id = id[3]

            tmp = np.array([cpts['scale'], cpts['scale']])
            tmp2 = cpts['data'].reshape([1, -1])
            feature = np.concatenate([tmp2[0], tmp / scale_norm_factor])
            old_class=gmm.predict(feature.reshape(1, -1))[0]

        else:
            assert id[3] == old_substroke_id+1

            tmp = np.array([cpts['scale'], cpts['scale']])
            tmp2 = cpts['data'].reshape([1, -1])
            feature = np.concatenate([tmp2[0], tmp / scale_norm_factor])
            new_class = gmm.predict(feature.reshape(1, -1))[0]
            rst[old_class, new_class] += 1
            change+=1
            old_char_id = id[0]
            old_person_id = id[1]
            old_stroke_id = id[2]
            old_substroke_id = id[3]
            old_class = new_class
    #print "#############", change, "##########################"
    return np.log( rst/ np.sum(rst,1,keepdims=True) )



