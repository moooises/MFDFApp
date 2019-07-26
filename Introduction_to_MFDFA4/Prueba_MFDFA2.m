%%
clear all
close all
load fractaldata.mat
warning off;

%%
X1=cumsum(multifractal-mean(multifractal));
X1=X1';
scale1=7:2:17;
scmin=16;
scmax=1024;
scres=19;
exponents=linspace(log2(scmin),log2(scmax),scres);
scale2=round(2.^exponents);
scale3=[scale1,scale2(2:end)];
q1=linspace(-5,5,101);
m1=2;%?????
%%
for ns=1:length(scale2),
    segments2(ns)=floor(length(X1)/scale2(ns));
    for v=1:segments2(ns),
        Index2=((((v-1)*scale2(ns))+1):(v*scale2(ns)));
        C2=polyfit(Index2,X1(Index2),m1);
        fit2=polyval(C2,Index2);
        RMS_scale2{ns}(v)=sqrt(mean((X1(Index2)-fit2).^2));
    end
    for nq=1:length(q1),
        qRMS2{ns}=RMS_scale2{ns}.^q1(nq);
        Fq2(nq,ns)=mean(qRMS2{ns}).^(1/q1(nq));
    end
    Fq2(q1==0,ns)=exp(0.5*mean(log(RMS_scale2{ns}.^2)));
end
for nq=1:length(q1),
    Ch1(1:2,nq) = polyfit(log2(scale2),log2(Fq2(nq,:)),1);
    Hq1(nq) = Ch1(1,nq);
    RegLine2(nq,1:length(scale2)) = polyval(Ch1(1:2,nq),log2(scale2));
end 
%%
halfmax1=floor(max(scale1)/2);
Time_index1=halfmax1+1:length(X1)-halfmax1;
%%
for ns=1:length(scale1),
    halfseg1=floor(scale1(ns)/2)
    for v=halfmax1+1:length(X1)-halfmax1;  
        Index1=v-halfseg1:v+halfseg1;
        C1=polyfit(Index1,X1(Index1),m1);
        fit1=polyval(C1,Index1);
        RMS_scale1{ns}(v)=sqrt(mean((X1(Index1)-fit1).^2));
        if(v==9)
           Index1 
        end
    end
end
%%
Ch2(1:2)=Ch1(:,q1==0);
Regfit1=polyval(Ch2,log2(scale1));
maxL1=length(Time_index1);
%%
for ns=1:length(scale1);
	RMSt1(ns,1:length(Time_index1))=RMS_scale1{ns}(Time_index1);
	resRMS1{ns}=log2(RMSt1(ns,:))-Regfit1(ns);
	logscale1(ns)=log2(scale1(ns))-log2(maxL1);
    Ht1(ns,:)=resRMS1{ns}./logscale1(ns) + Hq1(q1==0);
end
%%
halfmax3=floor(max(scale3)/2);
Time_index3=halfmax3+1:length(X1)-halfmax3;
for ns=1:length(scale3),
    halfseg3=floor(scale3(ns)/2);
    for v=halfmax3+1:length(X1)-halfmax3;
        Index3=v-halfseg3:v+halfseg3;
        C3=polyfit(Index3,X1(Index3),m1);
        fit3=polyval(C3,Index3);
        RMS_scale3{ns}(v)=sqrt(mean((X1(Index3)-fit3).^2));
    end
end
Regfit3=polyval(Ch2,log2(scale3));
maxL3=length(Time_index3);
for ns=1:length(scale3);
	RMSt3(ns,1:length(Time_index3))=RMS_scale3{ns}(Time_index3);
	resRMS3{ns}=log2(RMSt3(ns,:))-Regfit3(ns);
	logscale3(ns)=log2(scale3(ns))-log2(maxL3);
    Ht3(ns,:)=resRMS3{ns}./logscale3(ns) + Hq1(q1==0);
end
