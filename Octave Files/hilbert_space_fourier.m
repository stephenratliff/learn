function [err]=hilbert_space_fourier(N,type)
% HILBERT_SPACE_FOURIER L2 Fourier approximation, Parseval
if nargin<1, N=15; end; if nargin<2, type="square"; end
x=linspace(-pi,pi,4000); 
if type=="square", f=sign(sin(x));
elseif type=="saw", f=x/pi;
else f=double(abs(x)<0.5); end
S=zeros(size(x));
for k=1:N
 if strcmp(type,"square") && mod(k,2)==0, continue; end
 if strcmp(type,"square"), ck=4/pi/k; S+=ck*sin(k*x);
 elseif strcmp(type,"saw"), ck=2*(-1)^(k+1)/k; S+=ck*sin(k*x);
 else S+=sin(k*2*pi*x/ (2*pi))/k; end
end
err=sqrt(trapz(x,(f-S).^2)/(2*pi));
fprintf('N=%d L2 error=%.5f\n',N,err);
plot(x,f,'Color',[0.8 0.8 0.8]); hold on; plot(x,S,'LineWidth',1.5); hold off; grid on;
title(sprintf('Fourier N=%d err=%.3f',N,err));
end
