import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import math

def DFA(data):
    #plot the data
    plt.figure(figsize=(6,3))
    plt.figure(1)
    plt.plot(data,label='time series')
    plt.xlabel('time')
    plt.ylabel('Amplitude')
    plt.plot(np.cumsum(data-np.mean(data)),label='Random Walk')
    plt.legend()
    exponents=np.linspace(math.log2(16),math.log2(1024),19)
    scale=np.around(2**exponents,0)
    #scale=[16,32,64,128,256,512,1024]
    m=1
    segments=[]
    F=[]
    RMS=[]
    #print(data)
    data=np.cumsum(data-np.mean(data))
    #print(data)

    for ns in range(0,len(scale)):
        segments.append(math.floor(len(data)/scale[ns]))
        RMS.append([])
        Idx_start=0
        sum=int(scale[ns])
        Idx_stop=sum
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)
            X_Idx=data[Index]
            #print(Index)
            #print(len(Index))
            #print(X_Idx)
            C=np.polyfit(Index,X_Idx,m)
            #print(C)
            #print()
            fit=np.polyval(C,Index)
            #0.036
            RMS[ns].append(math.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+sum
        F.append(np.sqrt(np.mean([l**2 for l in RMS[ns]])))
        
        

    X=np.log2(scale)
    Ch=np.polyfit(X,np.log2(F),1)
    H=Ch[0]
    RegLine=np.polyval(Ch,X)

    plt.figure(2)
    plt.xlabel('Scale')
    plt.ylabel('Overall RMS')
    plt.plot(X,RegLine,"b-",label='Multifractal time series')
    plt.plot(X,np.log2(F),"o",color="blue",label="slope H = "+str(H))
    plt.xticks(X,np.linspace(16,1024,19))
    plt.yticks(RegLine,np.round(np.linspace(1,32,19)))
    plt.legend()
    plt.show()
    
    return H

def MFDFA1(data):
    #probar con los arrays de numpy
    data=np.cumsum(data-np.mean(data))

    exponents=np.linspace(math.log2(16),math.log2(1024),19)
    scale=np.around(2**exponents,0)
    q=np.linspace(-5,5,101)
    m=1
    qindex=[20,40,60,80]
    segments=[]
    RMS=[]
    qRMS=[]
    Fq=[]
    Hq=[]
    qRegLine=[]

    for i in range(0,len(q)):
        Fq.append([])


    for ns in range(0,len(scale)):
        segments.append(math.floor(len(data)/scale[ns]))
        RMS.append([])
        Idx_start=0
        sum=int(scale[ns])
        Idx_stop=sum-1
        qRMS.append([])
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)
            X_Idx=data[Index]
            C=np.polyfit(Index,X_Idx,m)
            fit=np.polyval(C,Index)
            RMS[ns].append(np.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+sum


        for nq in range(0,len(q)):
            qRMS[ns]=RMS[ns]**q[nq]
            if q[nq]==0:
                Fq[nq].append(np.exp(0.5*np.mean([l**2 for l in np.log(RMS[ns])])))
            else:
                Fq[nq].append(np.mean(qRMS[-1])**(1/q[nq]))


    for nq in range(0,len(q)):
        C=np.polyfit(np.log2(scale),np.log2(Fq[nq]),1)
        Hq.append(C[0])
        qRegLine.append(np.polyval(C,np.log2(scale)))


    X=np.log2(scale)         
    
    plt.figure(3)
    plt.xlabel('scale')
    plt.ylabel('Fq')
    for k in qindex:
        plt.plot(X,np.log2(Fq[k]),"o",color="blue")
        plt.plot(X,qRegLine[k],color="blue")

    plt.xticks(X,np.linspace(16,1024,19))
    #plt.yticks(,np.round(np.linspace(-1,32,20)))
    plt.legend()

    tq=Hq*q-1

    plt.figure(4)
    plt.xlabel('q-order')
    plt.ylabel('tq')
    plt.plot(q,tq,color="blue")

    hq=np.diff(tq)/(q[1]-q[0])
    Dq=(q[0:-1]*hq)-tq[0:-1]

    plt.figure(5)
    plt.xlabel('q-order')
    plt.ylabel('Dq')
    plt.plot(q[0:-1],Dq,color="blue")

    plt.figure(6)
    plt.xlabel('hq')
    plt.ylabel('Dq')
    plt.plot(hq,Dq,color="blue")

    plt.show()

    return  Hq,tq,hq,Dq,Fq
    
def MDFA2(data):
    data=np.cumsum(data-np.mean(data))

    exponents=np.linspace(math.log2(16),math.log2(1024),19)
    scale=np.around(2**exponents)
    halfmax=math.floor(max(scale)/2)
    Time_index=list(range(halfmax+1,len(data)-halfmax))

    q=np.linspace(-5,5,101)

    m=2
    segments=[]
    RMS=[]
    qRMS=[]
    Fq=[]
    Hq=[]
    qRegLine=[]
    RMS=[]

    
    #i=(np.where(q==0))#la posisicon de 0 en q

    for i in range(0,len(q)):
        Fq.append([])


    for ns in range(0,len(scale)):
        segments.append(math.floor(len(data)/scale[ns]))
        RMS.append([])
        Idx_start=0
        sum=int(scale[ns])
        Idx_stop=sum-1
        qRMS.append([])
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)
            X_Idx=data[Index]
            C=np.polyfit(Index,X_Idx,m)
            fit=np.polyval(C,Index)
            RMS[ns].append(np.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+sum


        for nq in range(0,len(q)):
            qRMS[ns]=RMS[ns]**q[nq]
            if q[nq]==0:
                i=nq
                Fq[nq].append(np.exp(0.5*np.mean([l**2 for l in np.log(RMS[ns])])))
            else:
                Fq[nq].append(np.mean(qRMS[-1])**(1/q[nq]))


    for nq in range(0,len(q)):
        C=np.polyfit(np.log2(scale),np.log2(Fq[nq]),1)
        Hq.append(C[0])
        qRegLine.append(np.polyval(C,np.log2(scale)))



    for ns in range(0,len(scale)):
        halfseg=math.floor(scale[ns]/2)
        RMS.append([])
        for v in Time_index:
            T_index=range(v-halfseg,v+halfseg)
            C=np.polyfit(T_index,data[T_index],m)
            fit=np.polyval(C,T_index)
            RMS[ns].append(np.sqrt(np.mean((data[T_index]-fit)**2)))

    C=np.polyfit(np.log2(scale),np.log2(Fq[i]),1)
    Regfit=np.polyval(C,np.log2(scale))
    maxL=len(data)

    resRMS=[]
    logscale=[]
    Ht=[]

    for ns in range(0,len(scale)):
        Ht.append([])
        RMSt=RMS[ns][Time_index[0]:Time_index[-1]]
        resRMS.append(Regfit[ns]-np.log2(RMSt))
        logscale.append(np.log2(maxL)-np.log2(scale[ns]))
        Ht[ns].append(resRMS[ns]/logscale[ns]+Hq[i])

    X=np.matrix(Ht)
    Ht_aux=X.getA1()
    Ht_row=[]
    for i in range(0,len(Ht_aux)):
        Ht_row=Ht_row+(Ht_aux[i].tolist())

    BinNumb=int(np.around(np.sqrt(len(Ht_row))))
    freq,Htbin=np.histogram(Ht_row,BinNumb)
    Ph=freq/np.sum(freq)
    Ph_norm=Ph/max(Ph)
    Dh=1-(np.log(Ph_norm)/np.log(np.mean(np.diff(Htbin))))# las divisiones entre cero pueden ocurrir
    plt.figure(6)
    print(len(Htbin))
    print(Htbin)
    print(len(Dh))
    print(Dh)
    plt.hist(Htbin,Dh)
    plt.show()


if __name__ == "__main__":
    data= scipy.io.loadmat('fractaldata.mat')
    multifractal=data['multifractal']
    #H=DFA(multifractal)
 
    #Hq,tq,hq,Dq,Fq=MFDFA1(multifractal)

    #if H<0.2:
    #    Hq-=1
    #    Ht-=1
    #else:
    #    if H>1.2 and H<1.8:
    #        Hq+=1
    #        Ht+=1
    #    else:
    #        if H>1.8:
    #            Hq+=2
    #            Ht+=2
    #print(Hq,tq,hq,Dq,Fq)

    MDFA2(multifractal)
        