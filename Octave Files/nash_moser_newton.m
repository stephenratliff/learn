function nash_moser_newton()
% NASH_MOSER_NEWTON Smoothed Newton vs plain Newton when derivative loses regularity
f=@(x) x^3-2*x+2; df=@(x) 3*x.^2-2;
x=0; for i=1:10, x=x-f(x)/df(x); fprintf('Newton %d x=%.6f f=%.3e\n',i,x,f(x)); end
% Smoothed version with damping
x=0; alpha=0.7; for i=1:12, x=x-alpha*f(x)/(df(x)+0.5); fprintf('Smoothed %d x=%.6f f=%.3e\n',i,x,f(x)); end
end
