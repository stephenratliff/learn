function nash_embedding_demo(k,amp)
% NASH_EMBEDDING_DEMO Corrugation preserves length
if nargin<1, k=30; amp=0.8; end
t=linspace(0,2*pi,4000); base=sin(t);
y=base+amp*sin(k*t)/k;
L_base=trapz(t,sqrt(1+cos(t).^2));
L_new=trapz(t,sqrt(1+(cos(t)+amp*cos(k*t)).^2));
fprintf('L base=%.5f L new=%.5f ratio=%.5f (should ~1)\n',L_base,L_new,L_new/L_base);
plot(t,y); title('Nash-Kuiper corrugation intuition');
end
