%%Algoritmo DFA para calcular el componente de Hust

%Tenemos tres series de tiempo con ruido aplicado sobre ellas
%Whitenoise,multifractal y monofractal
clear all
close all
%%
load fractaldata.mat

%%
RW1=cumsum(whitenoise-mean(whitenoise));
RW2=cumsum(monofractal-mean(monofractal));
RW3=cumsum(multifractal-mean(multifractal));

figure;
title("Whitenoise")
subplot(3,1,1);plot(whitenoise,'r');
title("Monofractal")
subplot(3,1,2);plot(monofractal,'r');
title("Multifractal")
subplot(3,1,3);plot(multifractal,'r');

%%Convertir Ruido a Random Walk
%Se sustrae la media de los ruidos y se integra en la serie de tiempo

figure;
title("Whitenoise")
subplot(3,1,1);plot(RW1);
title("Monofractal")
subplot(3,1,2);plot(RW2);
title("Multifractal")
subplot(3,1,3);plot(RW3);

%plot1

%%
%Podemos calcular la variacion media(amplitud media) de las series a traves de
%RMS(Root-Mean-Square)

RMS_ordinary=sqrt(mean(whitenoise.^2));
RMS_monofractal=sqrt(mean(monofractal.^2));
RMS_multifractal=sqrt(mean(multifractal.^2));

%plot2
%este plot no funciona

%Todas las amplitudes son alrededor de 1, incluso en la multifractal

%%
%Pero de esa forma las fluctuaciones locales quedan poco representadas
%Para arreglar esto se divide la series en segmentos del mismo tamaño y se
%se calcula la variacion media sobre cada uno de esos segmentos



X=cumsum(multifractal-mean(multifractal));% Aqui calculamos el perfil de la serie
X=X';
scale=1000;
segments=floor(length(X)/scale);% Obtenemos el numero de segmentos

c=["lineal","cuadratico", "cubico"];
figure;
for n=1:3
subplot(3,1,n);hold on;plot(X,'b');title(c(n))

m=n; %grado del ajuste
    for v=1:segments
        %establecemos la longitud del segmento
        Idx_start=((v-1)*scale)+1;
        Idx_stop=v*scale;
        Index{v}=Idx_start:Idx_stop;
        X_Idx=X(Index{v});
        C=polyfit(Index{v},X(Index{v}),m);
        fit{v}=polyval(C,Index{v});
        RMS{m}(v)=sqrt(mean((X_Idx-fit{v}).^2));% calculamos la moda/tendencia local del segmento
        plot(Index{v},fit{v},'-- r');
        plot(Index{v},fit{v}+RMS{m}(1),'- r');
        plot(Index{v},fit{v}-RMS{m}(1),'- r');
    end 
    
    %Para plotear en cada segmento, la clave es fit
    %hold on;plot(Index{1},fit{1}-RMS{1}(1),'- r');hold off;
hold off
end
%plot3

%Mirar como plotear correctamente esto en X,

%% Ahora calculamos un RMS general de la serie, este RMS es muy sensible a los cambios de fluctuaciones
% tanto lentos como rapidos(fluctuaciones poco o muy drasticas),lo calculamos 
% para destarcar los dos tipos de evoluciones de fluctuaciones en la serie
% Cambiando el tamaño de los segmentos, en el codigo scale, se puede
% apreciar mejor en cuales de ellos es rapido o lenta segun su tamaño

X=cumsum(multifractal-mean(multifractal));
X=X';
scale=[16,32,64,128,256,512,1024];
m=1;
figure;
hold on
    for ns=1:length(scale)
    X_index=[];
        segments(ns)=floor(length(X)/scale(ns));
        for v=1:segments(ns)
            Idx_start=((v-1)*scale(ns))+1;
            Idx_stop=v*scale(ns);
            X_index=[X_index Idx_start];
            Index{v,ns}=Idx_start:Idx_stop;
            X_Idx=X(Index{v,ns});
            C=polyfit(Index{v,ns},X(Index{v,ns}),m);
            fit{v,ns}=polyval(C,Index{v,ns});
            RMS{ns}(v)=sqrt(mean((X_Idx-fit{v,ns}).^2));
        end
        
        RMS{ns}(v+1)= RMS{ns}(v);
        X_index=[X_index Index{v,ns}(end)];
                
        F(ns)=sqrt(mean(RMS{ns}.^2));
        
        subplot(7,1,length(scale)+1-ns);stairs(X_index,RMS{ns},'b');line([0,8000],[F(ns),F(ns)],'Color','red');
                title(scale(ns))

    end
    legend('Local Fluctuation ','RMS of local fluctuation')
    hold off
    
    %%
    %Mediante el exponente de Hust, que obtemos a traves de la pendiente de la
    %linea de regresion, podemos calcular la estructura
    %monofractal de la serie observando como de rapido crece la linea de
    %regresion.
    %Realizamos log2 para obtener el exponente de F(2)~=n^2, ya que de este se obtiene el exponente de Hust  
    
    C=polyfit(log2(scale),log2(F),1);
    H=C(1);
    RegLine=polyval(C,log2(scale));
    
    Prueba_RMS()
    
    %% Con Prueba_RMS se realiza el algoritmo DFA, que a traves del Exponete de Hust (H) nos permite saber
    % la estructura monofractal de la serie de tiempo. Sin embargo este
    % algoritmo no nos permite distinguir estre la serie multifractal y la
    % monofractal, que en con DFA obtenemos que tienen una estructura
    % similar. Para poder distinguirlas se usa el algoritmo MF-DFA
    %% La serie multifractal tiene fluctuaciones locales muy grandes o muy pequeñas a diferencia de la serie monofractal.
    % La ausencia de fluctuaciones tan extremas en la serie monofractal
    % resultan en una distribucion normal donde la variacion es la varianza
    % solamente, que es el segundo momento estadistico, con q=2.
    % https://en.wikipedia.org/wiki/Moment_(mathematics)
    % La serie multifractal no esta normalmente distribuida y por lo tanto
    % todos sus momentos estadisticos, q, deben ser ser considerados.
    % Con esta premisa empieza MF-DFA.
    
    q=[-5,-3,-1,0,1,3,5];
    for nq=1:length(q)
        qRMS_1{nq}=RMS_scale1{1}.^q(nq);
        qRMS_2{nq}=RMS_scale2{1}.^q(nq);
        Fq1(nq)=mean(qRMS_1{nq}).^(1/q(nq));
        Fq2(nq)=mean(qRMS_2{nq}).^(1/q(nq));

    end
    
    Fq1(q==0)=exp(.5*mean(log(RMS_scale1{1}.^2)));
    Fq2(q==0)=exp(.5*mean(log(RMS_scale2{1}.^2)));

    figure;
    subplot(4,1,1);stairs(1:500,qRMS_1{2},'Color','b');title('q = -3');hold on ;stairs(1:500,qRMS_2{2},'Color','g');hold off
    subplot(4,1,2);stairs(1:500,qRMS_1{3},'Color','b');title('q = -1');hold on ;stairs(1:500,qRMS_2{3},'Color','g');hold off
    subplot(4,1,3);stairs(1:500,qRMS_1{5},'Color','b');title('q = 1');hold on ;stairs(1:500,qRMS_2{5},'Color','g');hold off
    subplot(4,1,4);stairs(1:500,qRMS_1{6},'Color','b');title('q = 3');hold on ;stairs(1:500,qRMS_2{6},'Color','g');hold off
    %Aqui se pueden ver las fluctiones grandes y pequeñas
    
    %Se puede ver que los momentos negativos son influenciados por
    %segmentos con poco RMS y tiene pequeñas fluctuaciones. 
    %Al contrario que con los momentos positivos, que tienen mucho RMS y
    %grandes fluctuaciones. Cuanto mayor o menor sean mas 
    
    %Los del grafico del pdf corresponden a los 125 primero parametros del
    %eje x en la figura de arriba
     
    
