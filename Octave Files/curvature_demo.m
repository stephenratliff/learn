function curvature_demo(a,b)
% CURVATURE_DEMO Gaussian curvature K for paraboloid z = a*x^2 + b*y^2
% K = 4ab / (1+4a^2 x^2+4b^2 y^2)^2  (Theorema Egregium)
% Example: curvature_demo(1,1)
  if nargin<1, a=1; b=0.5; end
  [U,V]=meshgrid(linspace(-1,1,120));
  K = 4*a*b ./ (1+4*a^2*U.^2+4*b^2*V.^2).^2;
  Z = a*U.^2 + b*V.^2;
  figure; subplot(1,2,1); surf(U,V,Z); shading interp; title('Paraboloid z=a x^2 + b y^2'); xlabel('x'); ylabel('y');
  subplot(1,2,2); surf(U,V,K); shading interp; title('Gaussian curvature K'); xlabel('x'); ylabel('y');
  fprintf('At origin K(0,0)=4ab=%.3f\n', 4*a*b);
end
