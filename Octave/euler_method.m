% euler_method.m
% Solves an ODE y' = f(t, y) using Euler's Method.
%
% Usage:
%   [t, y] = euler_method(f, t0, tf, y0, h)
%
% Inputs:
%   f   - function handle for the ODE: f(t, y)
%   t0  - initial time
%   tf  - final time
%   y0  - initial condition y(t0)
%   h   - step size
%
% Outputs:
%   t   - vector of time points
%   y   - vector of approximate solution values
%
% Example (run this file directly to see a demo):
%   f = @(t, y) -2 * y;          % y' = -2y, exact solution: y = e^(-2t)
%   [t, y] = euler_method(f, 0, 3, 1, 0.1);

function [t, y] = euler_method(f, t0, tf, y0, h)
  % Build time vector
  t = (t0 : h : tf)';
  n = length(t);

  % Preallocate solution vector
  y = zeros(n, 1);
  y(1) = y0;

  % Euler iteration: y_{n+1} = y_n + h * f(t_n, y_n)
  for i = 1 : n - 1
    y(i + 1) = y(i) + h * f(t(i), y(i));
  end
end

% ── Demo ─────────────────────────────────────────────────────────────────────
% Runs automatically when you execute this file directly.
% Remove or comment out this block if you want a library-only file.

f      = @(t, y) -2 * y;          % ODE:   y' = -2y
t0     = 0;                        % start time
tf     = 3;                        % end time
y0     = 1;                        % initial condition y(0) = 1
h      = 0.1;                      % step size

[t, y_euler] = euler_method(f, t0, tf, y0, h);
y_exact      = exp(-2 * t);        % analytical solution

% Print a sample of results
fprintf('%6s  %12s  %12s  %12s\n', 't', 'Euler', 'Exact', 'Error');
fprintf('%6s  %12s  %12s  %12s\n', '------', '------------', '------------', '------------');
idx = 1 : 5 : length(t);           % print every 5th row
for k = idx
  fprintf('%6.2f  %12.8f  %12.8f  %12.2e\n', ...
          t(k), y_euler(k), y_exact(k), abs(y_euler(k) - y_exact(k)));
end

% Plot
figure;
plot(t, y_exact, 'b-',  'LineWidth', 2, 'DisplayName', 'Exact');
hold on;
plot(t, y_euler, 'r--', 'LineWidth', 1.5, 'DisplayName', sprintf('Euler (h = %g)', h));
hold off;
xlabel('t');
ylabel('y');
title("Euler's Method vs Exact Solution");
legend('show', 'Location', 'northeast');
grid on;
