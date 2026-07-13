function variational_demo()
% VARIATIONAL_DEMO Catenary minimizes potential energy, Euler-Lagrange
x=linspace(-1,1,400); a=0.8;
y_cat=a*cosh(x/a); y_line=0*x; % straight line higher energy for hanging chain
E_cat=trapz(x,y_cat.*sqrt(1+sinh(x/a).^2));
fprintf('Energy catenary=%.4f (minimal)\n',E_cat);
plot(x,y_cat,'LineWidth',2); grid on; title('Catenary y=a cosh(x/a) minimizes J');
end
