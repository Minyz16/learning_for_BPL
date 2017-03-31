import os

from sklearn import mixture

from bspline.bspline import *
from empirical import num_of_strokes
from normlize import data_normlize, substroke_normlize
from plot.plot_utils import *
from mle import gammamle

print "PWD="+os.path.abspath(".")

#params
filename="../data/top500-data.txt"
samplenum_each_char=10   #sample number of each character
time_interval=1    #ms, approximately 25, equal 1 for convenient
norm_dis=1       #sub_stroke is normalized to lenth norm_dis between 2 points

pause_dis=4     #if move less than pause_dis pixel(s) between 2 points, marked as a pause (deprecated)
pause_rate=0.4
min_len=20     #sub_stroke less than min_len dis are removed

num_cpts=5      #number of control points
num_components=200  #component number of gmm clustering

scale_norm_factor=1000

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

if True:
    start=0
    end=10
    stk_per_char=10
    tmp=data[start:end][:stk_per_char]
    plot_multi_strokes(tmp,pause_dis)
    os._exit(1)
