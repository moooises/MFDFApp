a="-5.54"
k=list(range(-5,6))
print(k)
d=10.5//1
f=5.45
print(round(f,0))
print(d)
f=float(a)
print(f)
aux=""
if len(a)>2:
    if a[0]=='-':
        aux='-'
        i=1
    else:
        i=0

    while a[i]!='.' or i==len(a):
        aux=aux+a[i]
        i=i+1

    if a[i]=='.':
        if (i+1)!=len(a):
            i=i+1
            aux=aux+a[i]
        else:
            aux=aux+'0'
    else:
        aux=aux+'0'

else:
    if a[0]=='-':
        aux='-'+a[1]+'0'
    else:
        aux=a[0]+'0'
print(aux)