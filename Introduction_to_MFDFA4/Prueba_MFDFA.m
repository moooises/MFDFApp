%%
clear all
close all
load fractaldata.mat;
%%
qindex=[21,41,61,81];
X=cumsum(multifractal-mean(multifractal));
X=transpose(X);
exponents=linspace(log2(16),log2(1024),19);
scale=round(2.^exponents);
q=linspace(-5,5,101);
m=1;
qindex=[21,41,61,81];% Son las posiciones del -3,-1,1 y 3
for ns=1:length(scale)
    segments(ns)=floor(length(X)/scale(ns));
    for v=1:segments(ns)
       Idx_start=((v-1)*scale(ns))+1;
       Idx_stop=v*scale(ns);
       %X_index=[X_index Idx_start]
       Index{v,ns}=Idx_start:Idx_stop;
       X_Idx=X(Index{v,ns});
       C=polyfit(Index{v,ns},X(Index{v,ns}),m);
       fit{v,ns}=polyval(C,Index{v,ns});
       RMS{ns}(v)=sqrt(mean((X_Idx-fit{v,ns}).^2));
    end

    for nq=1:length(q)
        qRMS{ns}=RMS{ns}.^q(nq);
        Fq(nq,ns)=mean(qRMS{ns}).^(1/q(nq));
    end
    
    Fq(q==0,ns)=exp(0.5*mean(log(RMS{ns}.^2)));
    
end


for nq=1:length(q)
        C=polyfit(log2(scale),log2(Fq(nq,:)),1);
        C
        Hmu(nq)=C(1);
        qRegLine(nq,1:length(scale))=polyval(C,log2(scale));
end

X1=log2(scale);

figure;
hold on
title('Multifractal')
plot(X1,log2(Fq(qindex,:)),'Color','b','Marker','o','Linestyle','none');
plot(X1,qRegLine(qindex,:),'Color','b');
hold off

%%
X=cumsum(monofractal-mean(monofractal));
X=transpose(X);

for ns=1:length(scale)
    segments(ns)=floor(length(X)/scale(ns));
    for v=1:segments(ns)
       Idx_start=((v-1)*scale(ns))+1;
       Idx_stop=v*scale(ns);
       %X_index=[X_index Idx_start];
       Index{v,ns}=Idx_start:Idx_stop;
       X_Idx=X(Index{v,ns});
       C=polyfit(Index{v,ns},X(Index{v,ns}),m);
       fit{v,ns}=polyval(C,Index{v,ns});
       RMS{ns}(v)=sqrt(mean((X_Idx-fit{v,ns}).^2));
%        sqrt(mean((X_Idx-fit{v,ns}).^2));
%        if(RMS{ns}(v)==0)
%             ns
%             v
%             X(Index)
%             fit
%          X(Index)-fit
%             
%             sum(X(Index)-fit)
%             
%             (mean(X(Index)-fit).^2)
%             RMS{ns}(v)=0.0001;
%        end
    end

   for nq=1:length(q)
        qRMS{ns}=RMS{ns}.^q(nq);
        Fq(nq,ns)=mean(qRMS{ns}).^(1/q(nq));
    end
    
    Fq(q==0,ns)=exp(0.5*mean(log(RMS{ns}.^2)));
    
end


for nq=1:length(q)
        C=polyfit(log2(scale),log2(Fq(nq,:)),1);
        Hmo(nq)=C(1);
        qRegLine(nq,1:length(scale))=polyval(C,log2(scale));
end

X1=log2(scale);

figure;
hold on
title('Monofractal')
plot(X1,log2(Fq(qindex,:)),'Color','r','Marker','o','Linestyle','none');
plot(X1,qRegLine(qindex,:),'Color','r');
hold off

X=cumsum(whitenoise-mean(whitenoise));
X=transpose(X);
for ns=1:length(scale)
    segments(ns)=floor(length(X)/scale(ns));
    for v=1:segments(ns)
       Idx_start=((v-1)*scale(ns))+1;
       Idx_stop=v*scale(ns);
       %X_index=[X_index Idx_start];
       Index{v,ns}=Idx_start:Idx_stop;
       X_Idx=X(Index{v,ns});
       C=polyfit(Index{v,ns},X(Index{v,ns}),m);
       fit{v,ns}=polyval(C,Index{v,ns});
       RMS{ns}(v)=sqrt(mean((X_Idx-fit{v,ns}).^2));
%        sqrt(mean((X_Idx-fit{v,ns}).^2));
%        if(RMS{ns}(v)==0)
%             ns
%             v
%             X(Index)
%             fit
%          X(Index)-fit
%             
%             sum(X(Index)-fit)
%             
%             (mean(X(Index)-fit).^2)
%             RMS{ns}(v)=0.0001;
%        end
    end

   for nq=1:length(q)
        qRMS{ns}=RMS{ns}.^q(nq);
        Fq(nq,ns)=mean(qRMS{ns}).^(1/q(nq));
    end
    
    Fq(q==0,ns)=exp(0.5*mean(log(RMS{ns}.^2)));
    
end


for nq=1:length(q)
        C=polyfit(log2(scale),log2(Fq(nq,:)),1);
        Hw(nq)=C(1);
        qRegLine(nq,1:length(scale))=polyval(C,log2(scale));
end

X1=log2(scale);

figure;
hold on
title('Whitenoise')
plot(X1,log2(Fq(qindex,:)),'Color','c','Marker','o','Linestyle','none');
plot(X1,qRegLine(qindex,:),'Color','c');
hold off
figure;
hold on
plot(q,Hmu,'b');
plot(q,Hmo,'r');
plot(q,Hw,'g');
legend('Multifractal','Monofractal','Whitenoise');

hold off


   tqmu=Hmu.*q-1;
   tqmo=Hmo.*q-1;
   tqw=Hw.*q-1; 
   
   hqmu=diff(tqmu)./(q(2)-q(1));
   Dqmu=(q(1:end-1).*hqmu)-tqmu(1:end-1);
   hqmo=diff(tqmo)./(q(2)-q(1));
   Dqmo=(q(1:end-1).*hqmo)-tqmo(1:end-1);
   hqw=diff(tqw)./(q(2)-q(1));
   Dqw=(q(1:end-1).*hqw)-tqw(1:end-1);

   figure;
   subplot(1,2,1);plot(q,Hmu,'b');hold on;plot(q,Hmo,'r');hold off;hold on;plot(q,Hw,'c');hold off
   subplot(1,2,2);plot(q(1:end-1),Dqmu,'b');hold on;plot(q(1:end-1),Dqmo,'r');hold off;hold on;plot(q(1:end-1),Dqw,'c');hold off


    figure;
    plot(q,tqmu,'b');hold on; plot(q,tqmo,'r'); plot(q,tqw,'c');hold off;
    
    figure;
    plot(hqmu,Dqmu,'b');hold on;plot(hqmo,Dqmo,'r');plot(hqw,Dqw,'c');hold off
    
    
    

