import numpy as np
from tqdm import tqdm
from copy import deepcopy as dc
import math

def Test_Fun2(s):
    x1,x2=s
    return -(x2+47)*math.sin(math.sqrt(abs(x2+(x1/2)+47)))-x1*math.sin(math.sqrt(abs(x1-(x2+47))))
def Test_Fun1(coor):
    return np.sum(np.square(coor))


def simple_bouns(pos,Lb,Ub):
    ns=pos
    a=ns < Lb
    ns[a]=Lb[a]
    a=ns > Ub
    ns[a]=Ub[a]
    return ns

"""ba"""
def BA(Func,Lb,Ub,n=20,m_i=500,dim=2,minf=1,loud_A=0.5,r=0.3,qmin=0,qmax=5,prog=False):
    #qmin,qmax=0,5
    niter=0
    Q=np.zeros((n,1))
    V=np.zeros((n,dim))
    S=np.zeros((n,dim))

    sol=np.zeros((n,dim))
    fit = np.zeros(n)

    for i in range(n):
        sol[i]=Lb+(Ub-Lb)*np.random.rand(dim)
        fit[i] =Func(sol[i])

    fmin,I=np.min(fit),np.argmin(fit)
    best=sol[I]
    #print(fmin)
    #print(sol)
    if prog:
        bar=tqdm(range(m_i))
    else:
        bar=range(m_i)

    for it in bar:#tqdm(range(m_i)):
        res=dc(sol)
        for i in range(n):
            Q[i]=qmin+(qmax-qmin)*np.random.rand()
            V[i]=V[i]+(sol[i]-best)*Q[i]
            S[i]=sol[i]+V[i]
            #sol[i]=simple_bouns(sol[i],Lb,Ub)

            if np.random.rand() > r:
                S[i]=best+0.1*np.random.uniform(-1,1,dim)

            S[i]=simple_bouns(S[i],Lb,Ub)
            Fnew=Func(S[i])

            if minf==1:#minimize
                if Fnew<=fit[i] and np.random.rand() < loud_A:
                    sol[i]=S[i]
                    fit[i]=Fnew
                if Fnew <= fmin:
                    best=dc(S[i])
                    fmin=dc(Fnew)
            else:#maxmize
                if Fnew>=fit[i] and np.random.rand() < loud_A:
                    sol[i]=S[i]
                    fit[i]=Fnew
                if Fnew >= fmin:
                    best=dc(S[i])
                    fmin=dc(Fnew)


    return fmin,best

"""pso"""
def update_pos(p,v):
    """
    p: [w,x,y,z,...],pos[i]
    v: [wv,xv,yv,zv,...],vel[i]
    """
    return p+v

def update_velocity(pos,vel,p,g,w=0.5,ro_max=0.5,ro_min=-0.5):
    """
    pos: [w,x,y,z,...],new_pos[i]
    vel: [wv,xv,yv,zv,...],vel[i]
    p: pbp[i]
    g: gbp[i]
    w: weight
    ro_max: param
    """
    ro1=np.random.uniform(ro_min,ro_max,len(pos))
    ro2=np.random.uniform(ro_min,ro_max,len(pos))
    #return   np.random.uniform(-0.5,0.5)
    return w*vel + ro1*(p-pos)+ro2*(g-pos)#new_vel[i]
#np.random.uniform(-0.5,0.5)+()


def PSO(Func,lb,ub,n=20,m_i=500,dim=None,minf=1,prog=False):
#     n=20
#     m_i=5000
#     dim=10
#     minf=1
#     lb=np.ones(dim)*-100
#     ub=np.ones(dim)*500

    pos=np.random.uniform(ub,lb,(n,dim))#np.zeros((n,dim))
    vel=np.zeros((n,dim))
    pbp=dc(pos)
    pbs=[Func(c) for c in  pos]

    if minf==1:
        b_ind=np.argmin(pbs)
    else:
        b_ind=np.argmax(pbs)
    best_pos=dc(pos[b_ind])
    best_val=dc(pbs[b_ind])
    if prog:
        bar=tqdm(range())
    else:
        bar=range(m_i)

    #print("{0:.10f}:  \n".format(best_val),", ".join(["{0:.8}".format(p) for p in best_pos]))
    for it in bar:#range(m_i):
        for i in range(n):
            #p=pbp[i]
            gbp=best_pos
            new_vel=update_velocity(pos[i],vel[i],pbp[i],gbp)
            vel[i]=new_vel

            new_pos=simple_bouns(update_pos(pos[i],vel[i]),lb,ub)
            pos[i]=new_pos
            val=Func(new_pos)
            if minf==1:
                if val < pbs[i]:
                    pbs[i]=val
                    pbp[i]=new_pos
            else:
                if val > pbs[i]:
                    pbs[i]=val
                    pbp[i]=new_pos

                #print(val,"".join(list(map(str,new_pos))))
        if minf ==1:
            b_ind=np.argmin(pbs)
        else:
            b_ind=np.argmax(pbs)

        best_pos=dc(pbp[b_ind])
        best_val=dc(pbs[b_ind])
    return best_val,best_pos
    #print("{0:.10f}:  ".format(best_val),", ".join(["{0:.8}".format(p) for p in best_pos]))
