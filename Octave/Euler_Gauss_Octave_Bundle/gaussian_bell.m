function gaussian_bell(mu, sigma)
% GAUSSIAN_BELL Plot normal distribution and shade 68-95-99.7
% Example: gaussian_bell(0,1)
  if nargin<1, mu=0; sigma=1; end
  x = linspace(mu-4*sigma, mu+4*sigma, 800);
  y = 1/(sigma*sqrt(2*pi))*exp(-(x-mu).^2/(2*sigma^2));
  figure; plot(x,y,'LineWidth',2); grid on; hold on;
  for k=1:3
    idx = abs(x-mu)<=k*sigma;
    area(x(idx), y(idx), 'FaceAlpha',0.15); 
  end
  title(sprintf('N(\\mu=%.2f, \\sigma=%.2f)  68-95-99.7 rule', mu, sigma));
  xlabel('x'); ylabel('f(x)');
  fprintf('P(|X-mu|<=sigma)=%.4f, <=2sigma=%.4f, <=3sigma=%.4f\n', erf(1/sqrt(2)), erf(2/sqrt(2)), erf(3/sqrt(2)));
end
