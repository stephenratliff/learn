function [x,y] = euler_method(f, x0, y0, x_end, h)
% EULER_METHOD Simple explicit Euler integrator
% f = @(x,y) dy/dx, x0,y0 initial, x_end final, h step
% Example: f=@(x,y) -1.5*y; [x,y]=euler_method(f,0,1,4,0.2);
  x = x0:h:x_end;
  y = zeros(size(x));
  y(1)=y0;
  for i=1:length(x)-1
    y(i+1)=y(i)+h*f(x(i),y(i));
  end
  % compare to exact if f = -1.5*y
  if isequal(f(0,1), -1.5)
    y_exact = y0*exp(-1.5*(x-x0));
    plot(x,y,'o-',x,y_exact,'-'); legend('Euler','Exact'); grid on;
    fprintf('Final error at x=%.2f: %.3e\n', x_end, abs(y(end)-y_exact(end)));
  else
    plot(x,y,'o-'); grid on;
  end
end
