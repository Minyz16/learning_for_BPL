import os
import numpy as np
import matplotlib.pyplot as plt
import substroke_normalize
from scipy import interpolate

print "PWD="+os.path.abspath(".")

#params
filename="../top500-data.txt"
samplenum_each_char=5   #sample number of each character
time_interval=25    #ms
pause_dis=2     #if move less than pause_dis pixel(s) between 2 points, marked as a pause
min_len=10       #sub_stroke less than min_len points are removed
norm_dis=1       #sub_stroke is normalized to lenth norm_dis between 2 points

#consts
colorlst=['b','c','g','k','m','r','y']


#functions
def plot_stroke(stroke, color='b', show=True, marker=True):
    plt.plot(stroke[:,0], -stroke[:,1], color=color)
    tmp=stroke[stroke[:,3]<=pause_dis]
    plt.plot(tmp[:,0],-tmp[:,1],"*")
    plt.plot(stroke[0,0], -stroke[0,1],"*")
    plt.plot(stroke[-1,0],-stroke[-1,1],"*")
    if show:
        plt.show()

def plot_strokes(strokes, show=True):
    idx=0
    for stroke in strokes:
        #print idx
        stroke=np.asarray(stroke)
        plot_stroke(stroke,color=colorlst[idx % len(colorlst)],show=False)
        idx=idx+1
    if show:
        plt.show()

def plot_multi_strokes(multi_strokes, show=True):
    row=len(multi_strokes)
    col=len(multi_strokes[0])
    for i in range(0,row):
        for j in range(0,col):
            ax=plt.subplot(row,col,i*col+(j+1))
            plot_strokes(multi_strokes[i][j],show=False)
            plt.sca(ax)
    plt.show()

#
infile=open(filename,'r')
#data=[ [char1], [char2], ...,]  char=[ [strokes1], [strokes2], ...]
#strokes=[ [stroke1], [stroke2], ...,]    stroke=[[x1,y1,t1,dis1], [x2,y2,t2,dis2], ...] dis is the distance between this point and its previous point
data=[]
char=[]
loopid=0
charid_old=0
for line in infile:
    print loopid

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
                dis=pause_dis+1
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
#plot_multi_strokes(data[100:105])


#extract sub-strokes
substrokes=[]       #substrokes=[[substroke1], [substroke2], ...] substroke=[[x1,y1], [x2,y2], ...]
                    #1 pixel distance between points, zero mean, common scale along its longest dimension
                    #substroke less than points are removed
for char in data:
    for strokes in char:
        for stroke in strokes:
            substroke=[]
            for i in range(0,len(stroke)):
                if stroke[i][3]<=pause_dis:
                    substroke.append(stroke[i])
                    if len(substroke)>min_len:
                        substroke_normalize.normlize(substroke,norm_dis)            #1 pixel distance, zero mean, common scale, discard useless information
                        substrokes.append(substroke)
                    substroke=[]
                else:
                    substroke.append(stroke[i])

print len(substrokes)
print data[0][0]


