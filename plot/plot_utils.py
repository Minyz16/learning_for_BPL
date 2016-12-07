import matplotlib.pyplot as plt
import numpy as np
from bspline import bspline

colorlst=['b','c','g','k','m','y']

def plot_stroke(stroke, pause_dis,color='b', show=True, marker=True):
    #plt.plot(stroke[:,0], -stroke[:,1], '.', color=color)
    plt.plot(stroke[:, 0], -stroke[:, 1], color=color)
    #tmp=stroke[stroke[:,3]<=pause_dis]
    #plt.plot(tmp[:,0],-tmp[:,1],"r*")
    #plt.plot(stroke[-1,0],-stroke[-1,1],"r*")
    if show:
        plt.show()

def plot_strokes(strokes,pause_dis, show=True):
    idx=0
    for stroke in strokes:
        stroke=np.asarray(stroke)
        plot_stroke(stroke,pause_dis,color=colorlst[idx % len(colorlst)],show=False)
        idx=idx+1
    if show:
        plt.show()

def plot_multi_strokes(multi_strokes,pause_dis, show=True):
    row=len(multi_strokes)
    col=len(multi_strokes[0])
    for i in range(0,row):
        for j in range(0,col):
            ax=plt.subplot(row,col,i*col+(j+1))
            plot_strokes(multi_strokes[i][j],pause_dis,show=False)
            plt.xlim(-120, 120)
            plt.ylim(-120, 120)
            ax.set_xticks([])
            ax.set_yticks([])
            plt.sca(ax)
    plt.show()

def plot_substrokes(substrokes,start=0,row=10,col=10):
    plt.figure()
    end=start+row*col
    tmp=substrokes[start:end]
    for i in range(row*col):
        ax=plt.subplot(row,col,i+1)
        tmparray=np.array(tmp[i]['data'])
        plt.plot(tmparray[:,0],-tmparray[:,1])
        plt.xlim(-0.6, 0.6)
        plt.ylim(-0.6, 0.6)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.sca(ax)
    plt.show()

def plot_bspline_fit_refit(all_cpts,substrokes,start,row,col):
    plt.figure()
    end=start+row*col
    tmp1=substrokes[start:end]
    tmp2=all_cpts[start:end]
    for i in range(row*col):
        ax=plt.subplot(row,col,i+1)
        tmparray=np.array(tmp1[i]['data'])
        tmpcpts=np.array(tmp2[i]['data'])
        new_stk=bspline.get_stk_from_bspline(tmpcpts,100)
        plt.plot(tmparray[:,0],-tmparray[:,1],'b-')
        plt.plot(tmpcpts[:,0],-tmpcpts[:,1],'r.')
        plt.plot(new_stk[:,0],-new_stk[:,1],'y-')
        plt.xlim(-1, 1)
        plt.ylim(-1, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.sca(ax)
    plt.show()

def plot_new_data(data,start,row,col):
    plt.figure()
    for i in range(row):
        for j in range(col):
            idx = 0
            ax = plt.subplot(row, col, i*col+(j+1))
            char=data[start+i][j]
            for stroke in char:
                #print stroke
                #raw_input('pause')
                if len(stroke) == 0:
                    continue
                for substroke in stroke:
                    plt.plot(substroke[:,0],-substroke[:,1],color=colorlst[idx % len(colorlst)])
                    idx+=1
                #tmp=stroke[0]
                #plt.plot(tmp[0,0],-tmp[0,1],'r.')
                #plt.plot(tmp[-1,0], -tmp[-1, 1], 'r.')
            plt.xlim(-130, 130)
            plt.ylim(-130, 130)
            ax.set_xticks([])
            ax.set_yticks([])
            plt.sca(ax)
    plt.show()


