from __future__ import division
import numpy as np
def vectorized_bspline_coeff(vi,vs):
    vi=np.array(vi)
    vs=np.array(vs)
    assert (np.array_equal(vi.shape,vs.shape))
    C=np.array(np.zeros(vi.shape))
    sel1 = np.logical_and(vs >= vi,vs < vi+1)
    C[sel1] = (1/6)*np.power((vs[sel1]-vi[sel1]),3)

    sel2 = np.logical_and(vs >= vi + 1 , vs < vi + 2)
    C[sel2] = (1 / 6) * (
    -3 * np.power((vs[sel2] - vi[sel2] - 1), 3) + 3 * np.power((vs[sel2] - vi[sel2] - 1), 2) + 3 * (vs[sel2] - vi[sel2] - 1) + 1)

    sel3 = np.logical_and(vs >= vi + 2 , vs < vi + 3)
    C[sel3] = (1 / 6) * (3 * np.power((vs[sel3] - vi[sel3] - 2), 3) - 6 * np.power((vs[sel3] - vi[sel3] - 2), 2) + 4)

    sel4 = np.logical_and(vs >= vi + 3 , vs < vi + 4)
    C[sel4] = (1/6)*np.power((1-(vs[sel4]-vi[sel4]-3)) , 3);

    return C


def bspline_gen_s(nland,neval):
    lb = 2
    ub = nland+1
    s=np.linspace(lb,ub,neval)
    return s

def bspline_fit(sval,X,L):
    sval=np.array(sval)
    X=np.array(X)
    ns=sval.shape[0]
    sval.shape = (ns, 1)
    assert(X.shape[0] == ns)
    S=np.tile(sval,[1,L])
    I=np.tile(np.arange(0,L),[ns,1])
    A=vectorized_bspline_coeff(I,S)
    sumA = np.sum(A,1)
    sumA.shape=(-1,1)
    Cof = A / np.tile(sumA,[1,L])
    Cof=np.matrix(Cof)
    Coft=np.matrix(Cof.transpose())
    X=np.matrix(X)
    P = (Coft * Cof).I * Coft * X
    return P

def fit_bspline_to_traj(stk,nland):
    stk=np.array(stk)
    neval=stk.shape[0]
    s = bspline_gen_s(nland, neval)
    P = bspline_fit(s, stk, nland)
    return P

def bspline_eval(sval,cpts):
    sval = np.array(sval)
    cpts=np.array(cpts)
    sval.shape=-1,1
    L=cpts.shape[0]
    ns=sval.shape[0]
    y=np.matrix(np.zeros([ns,2]))

    S = np.tile(sval,[1,L])
    I = np.tile(np.arange(0,L),[ns,1])
    Cof =  vectorized_bspline_coeff(I,S)
    sumC = np.sum(Cof,1)
    sumC.shape=-1,1
    Cof = Cof / np.tile(sumC,[1,L])
    Cof = np.matrix(Cof)
    cpts=np.matrix(cpts)
    y[:,0] = Cof*cpts[:,0]
    y[:,1] = Cof*cpts[:,1]
    return y


def get_stk_from_bspline(P,neval):
    nland = P.shape[0]
    s = bspline_gen_s(nland, neval)
    stk = bspline_eval(s, P)
    return stk