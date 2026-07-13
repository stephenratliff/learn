function residues = modular_clock(a, m, k)
% MODULAR_CLOCK Visualize multiples of a mod m
% Example: modular_clock(7,12,20) -> clock arithmetic
  if nargin<3, k=20; end
  residues = mod((1:k)*a, m);
  fprintf('%d * a mod %d: ', a, m); disp(residues);
  % plot on circle
  theta = 2*pi*(0:m-1)/m;
  figure; polarplot([theta theta(1)], [ones(1,m) 1], 'k:'); hold on;
  r = residues; th = 2*pi*r/m;
  polarplot(th, ones(size(th)), 'ro', 'MarkerFaceColor','r'); hold off;
  title(sprintf('Multiples of %d mod %d', a, m));
end
