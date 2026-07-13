function maxwell_circuits()
% MAXWELL_CIRCUITS Helmholtz plane wave + RLC impedance & transfer function
% Maxwell: plane wave E = E0 exp(i(kx - wt))
k=2*pi; w=2*pi*3e8/0.5; x=linspace(0,3,800);
E=cos(k*x); B=E; % in phase for vacuum, perpendicular in space
figure(1); plot(x,E,x,B,'--'); legend('E_y','B_z'); title('EM plane wave e^{i(kx-wt)}'); grid on;

% RLC series: Z = R + i(wL -1/wC), H = 1/(1+iQ(w/w0 - w0/w))
R=10; L=10e-3; C=100e-6; w0=1/sqrt(L*C); Q=w0*L/R;
w=logspace(2,5,1000); Z=R+1i*(w*L-1./(w*C));
H=1./(1+1i*Q*(w/w0 - w0./w));
figure(2); loglog(w,abs(Z)); grid on; title('|Z| vs w, resonance at w0'); xlabel('w rad/s');
figure(3); semilogx(w,20*log10(abs(H))); grid on; title('RLC transfer |H| dB'); xlabel('w');
fprintf('w0=%.1f rad/s f0=%.1f Hz Q=%.2f\n',w0,w0/2/pi,Q);
end
