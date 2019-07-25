close all
clear all
clc
load fractaldata.mat
X1=cumsum(multifractal-mean(multifractal));
X2=cumsum(monofractal-mean(monofractal));
X3=cumsum(whitenoise-mean(whitenoise));
X1=transpose(X1);
X2=transpose(X2);
X3=transpose(X3);

scmin=16;
scmax=1024;
scres=19;
exponents=linspace(log2(scmin),log2(scmax),scres);
scale1=round(2.^exponents);
sindex2=[1,4,7,10,13,16,19];

m1=1;
for ns=1:length(scale1),
    segments1(ns)=floor(length(X1)/scale1(ns));
    for v=1:segments1(ns),
        Index1=((((v-1)*scale1(ns))+1):(v*scale1(ns)));
        C1=polyfit(Index1,X1(Index1),m1);
        C2=polyfit(Index1,X2(Index1),m1);
        C3=polyfit(Index1,X3(Index1),m1);
        fit1=polyval(C1,Index1);
        fit2=polyval(C2,Index1);
        fit3=polyval(C3,Index1);
        RMS_scale1{ns}(v)=sqrt(mean((X1(Index1)-fit1).^2));
        RMS_scale2{ns}(v)=sqrt(mean((X2(Index1)-fit2).^2));
        RMS_scale3{ns}(v)=sqrt(mean((X3(Index1)-fit3).^2));
    end
    F1(ns)=sqrt(mean(RMS_scale1{ns}.^2));
    F2(ns)=sqrt(mean(RMS_scale2{ns}.^2));
    F3(ns)=sqrt(mean(RMS_scale3{ns}.^2));
end
Ch1 = polyfit(log2(scale1),log2(F1),1);
H1 = Ch1(1);
RegLine1 = polyval(Ch1,log2(scale1));

Ch2 = polyfit(log2(scale1),log2(F2),1);
H2 = Ch2(1);
RegLine2 = polyval(Ch2,log2(scale1));

Ch3 = polyfit(log2(scale1),log2(F3),1);
H3 = Ch3(1);
RegLine3 = polyval(Ch3,log2(scale1));

X1=log2(scale1);

figure;
hold on
plot(X1,log2(F2),'Color','r','Marker','o','Linestyle','none');
plot(X1,log2(F3),'Marker','o','Color','m','Linestyle','none');
plot(X1,log2(F1),'Marker','o','Color','b','Linestyle','none');
plot(X1,RegLine1,'Color','b');
plot(X1,RegLine2,'Color','r');
plot(X1,RegLine3,'Color','m');
legend('Monofractal time series','White Noise','Multifractal TIme Series',['Pendiente H = ' num2str(H1)],['Pendiente H = ' num2str(H2)],['Pendiente H = ' num2str(H3)],'Location','northwest')
%xticklabels({'16','32','64','128','256','512','1024'})
%yticklabels({'1','2','4','8','16','32'})
hold off