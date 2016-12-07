import os

from sklearn import mixture

from bspline.bspline import *
from empirical import num_of_strokes
from normlize import data_normlize, substroke_normlize
from plot.plot_utils import *
from utils import utils
from mle import gammamle

print "PWD="+os.path.abspath(".")

#params
filename="data/top500-data.txt"
samplenum_each_char=10   #sample number of each character
time_interval=1    #ms, approximately 25, equal 1 for convenient
norm_dis=1       #sub_stroke is normalized to lenth norm_dis between 2 points

pause_dis=4     #if move less than pause_dis pixel(s) between 2 points, marked as a pause (deprecated)
pause_rate=0.4
min_len=20     #sub_stroke less than min_len dis are removed

num_cpts=5      #number of control points
num_components=200  #component number of gmm clustering

scale_norm_factor=1000
#consts
checkpoints=[False,False,False,False]   #CHECKPOINT1: check strokes
                                       #CHECKPOINT2: check normalized substrokes extracted from data
                                       #CHECKPOINT3: check b-spline fitting
                                       #CHECKPOINT4: check primitives

#main
infile=open(filename,'r')
#data=[ [char1], [char2], ...,]  char=[ [strokes1], [strokes2], ...]
#strokes=[ [stroke1], [stroke2], ...,]    stroke=[[x1,y1,t1,dis1], [x2,y2,t2,dis2], ...] dis is the distance between this point and its previous point
print "Reading data..."
data=[]
char=[]
loopid=0
charid_old=0
for line in infile:
    if loopid % 1000 == 0:
        print str(loopid/1000)+' of 500'

    if loopid % 1000 >= samplenum_each_char:
        loopid+=1
        continue

    charid=loopid/1000
    if(charid == charid_old+1):
        charid_old=charid
        data.append(char)
        char=[]
    tmp=line.strip('\r\n')
    tmp=tmp.replace(';',',')
    tmp = tmp.replace('=', ',')
    tmp=tmp.split(',')
    #print tmp
    del tmp[0]
    del tmp[-1]
    strokes=[]
    stroke=[]
    l=len(tmp)
    t=0
    for i in range(0,l,2):
        if int(tmp[i])== -1:
            assert(int(tmp[i+1])==0 or int(tmp[i+1])==-1)
            if int(tmp[i+1]) == -1:
                break
            elif int(tmp[i+1]) == 0:
                strokes.append(stroke)
                stroke=[]
                t=t+time_interval
        else:
            if(len(stroke) == 0):
                dis=0
            else:
                x1=stroke[-1][0]
                y1=stroke[-1][1]
                x2=int(tmp[i])
                y2=int(tmp[i+1])
                dis=pow((x1-x2),2)+pow((y1-y2),2)
            stroke.append([int(tmp[i]), int(tmp[i + 1]), t, dis])
            t=t+time_interval
    char.append(strokes)

    loopid += 1
data.append(char)
print "character="+str(len(data))+", each character has "+str(len(data[0]))+" samples"
data_normlize.normlize_data(data)

#CHECKPOINT1: check strokes
checkpoint1=checkpoints[0]
if checkpoint1:
    start=0
    end=10
    stk_per_char=10
    tmp=data[start:end][:stk_per_char]
    plot_multi_strokes(tmp,pause_dis)
    os._exit(1)

#extract sub-strokes
print "extracting substrokes & normalizing ..."
substrokes=[]   #all_substrokes=[{substroke1}, {substroke2}, ...] substroke={data:[[x1,y1], [x2,y2], ...],scale:scale_factor,id:(charid,personid,strokeid,substrokeid)}
                    #use data[charid][personid][strokeid][substrokeid] to find the specific substroke, all index information are saved in the 'id' field
                    #1 pixel distance between points, zero mean, common scale along its longest dimension
                    #substroke less than min_len points are removed
for char_id in range(len(data)):
    for person_id in range(len(data[char_id])):
        average_dis=utils.compute_average_dis(data[char_id][person_id])
        for stroke_id in range(len(data[char_id][person_id])):
            stroke_len=utils.compute_accumulate_dis(data[char_id][person_id][stroke_id])
            tmp_substroke=[]
            tmp_substrokes=[]
            substroke_id = 0
            #special case for very short stroke (such as one "point" )

            '''if stroke_len > 2 and stroke_len < min_len:
                tmp_substrokes.append(np.array(data[char_id][person_id][stroke_id]))
                tmp_substroke = substroke_normlize.normlize(data[char_id][person_id][stroke_id], norm_dis)
                tmp_substroke['id'] = (char_id, person_id, stroke_id, substroke_id)
                substrokes.append(tmp_substroke)
                data[char_id][person_id][stroke_id] = tmp_substrokes
                continue'''

            for point_id in range(len(data[char_id][person_id][stroke_id])):
                if point_id==0:
                    tmp_substroke.append(data[char_id][person_id][stroke_id][point_id])
                    continue
                if data[char_id][person_id][stroke_id][point_id][3] <= (average_dis * pause_rate):  #so that this point may be a stop-point
                    tmp_substroke.append(data[char_id][person_id][stroke_id][point_id])
                    accumulate_dis=utils.compute_accumulate_dis(tmp_substroke)
                    if accumulate_dis >= min_len:           #now we actually get a substroke
                        tmp_substrokes.append(np.array(tmp_substroke))
                        tmp_substroke= substroke_normlize.normlize(tmp_substroke, norm_dis)
                        tmp_substroke['id']=(char_id,person_id,stroke_id,substroke_id)
                        substrokes.append(tmp_substroke)
                        substroke_id+=1
                        tmp_substroke = [data[char_id][person_id][stroke_id][point_id]]
                    else:       #this fake sub-stroke is too short
                        tmp_substroke = [data[char_id][person_id][stroke_id][point_id]]
                else:
                    tmp_substroke.append(data[char_id][person_id][stroke_id][point_id])
            #don't forget the last point, it must be a stop point
            accumulate_dis = utils.compute_accumulate_dis(tmp_substroke)
            if accumulate_dis >= min_len:
                tmp_substrokes.append(np.array(tmp_substroke))
                tmp_substroke = substroke_normlize.normlize(tmp_substroke, norm_dis)
                tmp_substroke['id'] = (char_id, person_id, stroke_id, substroke_id)
                substrokes.append(tmp_substroke)
            # Warning: some strokes are too "slow" to have substrokes
            # so maybe data[char_id][person_id][stroke_id]=tmp_substrokes=[]
            data[char_id][person_id][stroke_id]=tmp_substrokes

print "There're "+str(len(substrokes))+" normalized substrokes extracted before clustering"


#CHECKPOINT2: check normalized substrokes extracted from data
checkpoint2=checkpoints[1]
if checkpoint2:
    #plot_substrokes(substrokes,start=0,row=10,col=10)
    plot_new_data(data,start=400,row=10,col=10)
    os._exit(2)

#fit substrokes to bspline
#all_cpts=[cpts1,cpts2,...]    cpts={data:[[x1,y1],[x2,y2],...[x5,y5]],scale:scale_factor,id:(id)}
print "Fitting to b-spline..."
all_cpts=[]
for substroke in substrokes:
    #if type(substroke) != dict:
    #   print substroke
    tmp=substroke['data']
    rst={}
    rst['data']=np.array(fit_bspline_to_traj(tmp,num_cpts))
    rst['scale']=substroke['scale']
    rst['id']=substroke['id']
    all_cpts.append(rst)

#CHECKPOINT3: check b-spline fitting
checkpoint3=checkpoints[2]
if checkpoint3:
    plot_bspline_fit_refit(all_cpts, substrokes, start=0, row=5, col=5)
    os._exit(3)

#GMM clustering
print "GMM clustering..."
g = mixture.GaussianMixture(n_components=num_components,covariance_type='diag',max_iter=200)
feature_map=np.zeros([len(all_cpts),2*num_cpts+2])    # N*K, N quals to the number of substrokes and K = 2* #cpts + #scale
for i in range(len(all_cpts)):
    tmp=np.array([all_cpts[i]['scale'],all_cpts[i]['scale']])
    tmp2=all_cpts[i]['data'].reshape([1,-1])
    feature_map[i]=np.concatenate([tmp2[0],tmp/scale_norm_factor])
    #print feature_map[i]
    #raw_input('pause')
g.fit(feature_map)
print num_components," clusters \n ","GMM converged? ",g.converged_

#CHECKPOINT4: check primitives
checkpoint4=checkpoints[3]
if checkpoint4:
    plt.figure()
    start = 0
    row = 10
    col = 20
    end = start + row * col
    tmp=g.means_[start:end]
    for i in range(row * col):
        #tmparray=tmp[i,:-2]
        tmparray=tmp[i][:-2]
        tmparray.shape=-1,2
        scale_factor=tmp[i][-1]
        new_stk = get_stk_from_bspline(tmparray, 100)
        new_stk = new_stk * scale_factor *scale_norm_factor
        #print new_stk
        #print scale_factor
        #raw_input('pause')
        ax = plt.subplot(row, col, i + 1)
        plt.plot(new_stk[:, 0], -new_stk[:, 1])
        plt.xlim(-70, 70)
        plt.ylim(-70, 70)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.sca(ax)
    plt.show()
    os._exit(4)

#parameter estimation
print "Estimating parameters..."
mu=(np.array(g.means_))[:,:-2]                      #200*10
sigma=(np.array(g.covariances_))[:,:-2]      #200*10
vsd=np.sqrt(g.covariances_)         #200*10
mixprob=np.array(g.weights_)    #1*200
print 'mixprob', mixprob
freq=np.array(mixprob*len(substrokes),dtype=int)    #1*200
logT=num_of_strokes.compute_logT(g,all_cpts,num_components,scale_norm_factor)   #200*200
print 'logT', logT
logStart=num_of_strokes.compute_logstart(g, all_cpts, num_components, scale_norm_factor)   #200*1
print 'logstart', logStart
pkappa=num_of_strokes.compute_num_strokes(data,15)   #10?*1
print 'pkappa', pkappa
pmat_nsub=num_of_strokes.compute_num_substrokes(data,[15,15])      #10?*10?
print 'pmat_nsub', pmat_nsub
theta=gammamle.learn_theta(g,all_cpts,num_components,scale_norm_factor)  #200*2
print 'theta', theta
#logpYX     25*25

print "Saving data..."
np.savetxt("data/mu.txt",mu)
np.savetxt("data/sigma.txt",sigma)
np.savetxt("data/vsd.txt",vsd)
np.savetxt("data/mixprob.txt",mixprob)
np.savetxt("data/freq.txt",freq)
np.savetxt("data/logT.txt",logT)
np.savetxt("data/logStart.txt",logStart)
np.savetxt("data/pkappa.txt",pkappa)
np.savetxt("data/pmat_nsub.txt",pmat_nsub)
np.savetxt("data/theta.txt",theta)