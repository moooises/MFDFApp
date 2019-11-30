    for ns in range(0,ind):#Primera seccion

        segments.append(math.floor(len(data)/scale[ns]))#tamaño del segmento
        RMS.append([])
        Idx_start=0
        sum=int(scale[ns])
        Idx_stop=sum-1
        qRMS.append([])
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)#indice en data
            X_Idx=data[Index]
            C=np.polyfit(Index,X_Idx,m)
            fit=np.polyval(C,Index)
            RMS[ns].append(np.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+sum
            
        print(RMS[ns])
        print(type(RMS[ns]))
        print()


    print("PArt 2")
    for ns in range(ind,len(scale)):#Segunda seccion

        segments.append(math.floor(len(data)/scale[ns]))#tamaño del segmento
        RMS.append([])
        Idx_start=0
        sum=int(scale[ns])
        Idx_stop=sum-1
        qRMS.append([])
        for v in range(0,segments[-1]):
            Index=range(Idx_start,Idx_stop)#indice en data
            X_Idx=data[Index]
            C=np.polyfit(Index,X_Idx,m)
            fit=np.polyval(C,Index)
            RMS[ns].append(np.sqrt(np.mean((X_Idx-fit)**2)))
            Idx_start=Idx_stop+1
            Idx_stop=Idx_stop+sum

        print(RMS[ns])
        print(type(RMS[ns]))
        print()
    print()
    print()
    print()


    for ns in range(0,len(scale)):#Calculo de los q con RMS de ambas secciones

        for nq in range(0,len(q)):
            qRMS[ns]=RMS[ns]**q[nq]
            #print(qRMS[ns])
            #print(type(RMS[ns]))
            #print()
            #print(qRMS[-1])
            #print(type(qRMS[ns]))

            if q[nq]==0:
                #Fq[nq].append(np.exp(0.5*np.mean([l**2 for l in np.log(RMS[ns])])))
                i=nq
            else:

                Fq[nq].append(np.mean(qRMS[ns])**(1.0/q[nq]))
                #print(Fq[ns])

        sumaFq=[]
        for j in range(0,len(Fq[i-1])):
            sumaFq.append(Fq[i-1][j]+Fq[i+1][j])


        Fq[i]=[x/2 for x in sumaFq]

#############################################################3

if len(q_min)>2:
            if q_min[0]=='-':
                i=1
            else:
                i=0

            while q_min[i]!='.' or i==len(q_min):
                aux=aux+q_min[i]
                i=i+1

            if q_min[i]=='.':
                if (i+1)!=len(q_min):
                    i=i+1
                    aux=aux+q_min[i]
                else:
                    aux=aux+'0'
            else:
                aux=aux+'0'

        else:
            if q_min[0]=='-':
                aux=q_min[1]+'0'
            else:
                aux=q_min[0]+'0'
        cant=int(aux)
        
        aux=""
        if len(q_max)>2:
            if q_max[0]=='-':
                i=1
            else:
                i=0

            while q_max[i]!='.' or i==len(q_max):
                aux=aux+q_max[i]
                i=i+1

            if q_max[i]=='.':
                if (i+1)!=len(q_max):
                    i=i+1
                    aux=aux+q_max[i]
                else:
                    aux=aux+'0'
            else:
                aux=aux+'0'

        else:
            if q_max[0]=='-':
                aux=q_max[1]+'0'
            else:
                aux=q_max[0]+'0'
        cant=cant+int(aux)+1

        print(cant)

################################################3

    q=np.around(q,1)
    aux=np.around(q[0],0)
    aux=int(aux)
    auxm=int(np.around(q[-1],0))
    div=list(range(aux,auxm))
    print(div)
    if aux<0:
        aux=aux+1
        auxm=(-1*aux)+1
    print(aux)
    print("------")
    print(auxm)
    div=list(range(aux-1,auxm+1))
    print(div)
    i=0
    j=0
    qindex=[]
    print(len(q))
    while j<len(q) and i<len(div):
        if div[i]!=0 and q[j]/div[i]==1:
            i=i+1
            qindex.append(j)
        else:
            if q[j]==0:
                i=i+1
                qindex.append(j)
        
        j=j+1

    i=0
    q_index=[]
    while i<len(qindex):
        if i%2!=0:
            q_index.append(qindex[i])
        i=i+1

    return q_index

        