function curvature_strings()
% CURVATURE_STRINGS Gaussian curvature -> Ricci flat -> strings
% Gaussian curvature K = 4ab/(1+4a^2 u^2+4b^2 v^2)^2 for z=ax^2+by^2
[U,V]=meshgrid(linspace(-1,1,120));
a=1; b=-1; % saddle K<0
K=4*a*b./(1+4*a^2*U.^2+4*b^2*V.^2).^2;
Z=a*U.^2+b*V.^2;
figure(1); surf(U,V,Z); shading interp; title('Paraboloid / Saddle z=ax^2+by^2'); xlabel('u'); ylabel('v');
figure(2); surf(U,V,K); shading interp; title('Gaussian curvature K (intrinsic)'); colorbar;
fprintf('At origin K=4ab=%.2f : K>0 sphere-like, K<0 saddle, K=0 developable\n',4*a*b);

% String vibration modes (Fourier = string modes)
L=1; x=linspace(0,L,500); t=0;
for n=1:4
 yn=sin(n*pi*x/L);
 figure(3); subplot(2,2,n); plot(x,yn); title(sprintf('String mode n=%d',n)); grid on;
end
% Calabi-Yau toy: S^2 x S^2 approx Ricci-flat slice visualization
fprintf('Calabi-Yau condition R_{ij}=0 Ricci-flat Kahler -> string compactification\n');
end
