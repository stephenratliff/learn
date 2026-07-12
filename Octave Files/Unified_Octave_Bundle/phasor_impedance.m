function phasor_impedance()
% PHASOR_IMPEDANCE Visualize V=IZ in complex plane
R=20; L=30e-3; C=150e-6; w=2*pi*60;
ZL=1i*w*L; ZC=1/(1i*w*C); Z=R+ZL+ZC;
I=1*exp(1i*0); VR=I*R; VL=I*ZL; VC=I*ZC;
fprintf('Z=%.2f%+.2fi |Z|=%.2f arg=%.1f deg\n',real(Z),imag(Z),abs(Z),angle(Z)*180/pi);
figure; hold on; quiver(0,0,real(VR),imag(VR),0,'LineWidth',2); quiver(real(VR),imag(VR),real(VL),imag(VL),0);
quiver(real(VR)+real(VL),imag(VR)+imag(VL),real(VC),imag(VC),0); axis equal; grid on;
legend('VR','VL','VC'); title('Phasor diagram V = IZ');
end
