function fourier_machinery()
% FOURIER_MACHINERY Series, Transform, Parseval, DFT
% Square wave Fourier series and FFT spectrum
N=20; L=pi; x=linspace(-L,L,2048); f=sign(sin(x));
% Fourier coefficients via trapz
S=zeros(size(x));
for k=1:2:2*N-1
 ck=4/pi/k; S+=ck*sin(k*x);
end
err=sqrt(trapz(x,(f-S).^2)/(2*L));
fprintf('Square wave N=%d L2 err=%.4f (Parseval)\n',N,err);
figure(1); plot(x,f,'Color',[0.8 0.8 0.8]); hold on; plot(x,S,'LineWidth',1.5); hold off; grid on; title('Fourier synthesis');
% FFT spectrum
F=fftshift(abs(fft(f))/length(f)); freq=linspace(-0.5,0.5,length(f));
figure(2); stem(freq, F); title('|c_k| spectrum decaying 1/k'); xlabel('normalized freq');
end
