function spectral_hilbert_demo(a,b,c)
% SPECTRAL_HILBERT_DEMO 2x2 symmetric eig = ellipse axes, plus Hilbert matrix cond
if nargin<3, a=2;b=1;c=1; end
A=[a b; b c]; [V,D]=eig(A); fprintf('eig: '); disp(diag(D)');
theta=linspace(0,2*pi,500); circ=[cos(theta); sin(theta)]; ell=A*circ;
figure; plot(ell(1,:),ell(2,:)); axis equal; grid on; title('A * S^1 = ellipse');
for n=[3 5 8 12], H=hilb(n); fprintf('hilb(%d) cond=%.2e\n',n,cond(H)); end
end
