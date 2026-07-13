function [m,b] = gauss_fit(x,y)
% GAUSS_FIT Least squares fit y = m*x + b (Gauss 1809)
% x,y column vectors. Returns slope m, intercept b, plots residuals.
% Example: x=(0:10)'; y=2*x+1+randn(size(x)); gauss_fit(x,y);

  if size(x,2)>1, x=x(:); end
  if size(y,2)>1, y=y(:); end
  X = [ones(length(x),1) x];
  beta = X \ y;  % solves normal equations
  b = beta(1); m = beta(2);
  yhat = X*beta;
  mse = mean((y-yhat).^2);
  figure; plot(x,y,'o',x,yhat,'-','LineWidth',2); grid on;
  for i=1:length(x)
    line([x(i) x(i)], [y(i) yhat(i)], 'Color',[0.8 0.3 0.3], 'LineStyle','--');
  end
  legend('data','fit','residuals'); title(sprintf('y=%.4f x + %.4f, MSE=%.4f', m,b,mse));
  fprintf('Fit: y = %.6f x + %.6f, MSE=%.6e\n', m,b,mse);
end
