% --- Approximating e two ways -------------------------------
n = 1e6;
e_limit  = (1 + 1/n)^n            % compound-interest limit
e_series = sum(1 ./ factorial(0:15)) % series: converges FAST
abs(e_series - exp(1))             % error ~ 1e-13 with 16 terms

% --- Euler's formula: exp(i*theta) == cos + i*sin -----------
theta = linspace(0, 2*pi, 9).';
lhs = exp(1i*theta);
rhs = cos(theta) + 1i*sin(theta);
max(abs(lhs - rhs))               % ~ 1e-16: machine epsilon

% --- Euler's identity ---------------------------------------
exp(1i*pi) + 1                     % ~ 0 + 1.2246e-16i

% --- Draw the unit circle from pure exponentials ------------
t = linspace(0, 2*pi, 400);
z = exp(1i*t);
plot(real(z), imag(z), 'linewidth', 2); axis equal; grid on;
title('The unit circle is e^{i\theta}');
