% EULER_IDENTITY_BASEL
% 1) Euler's identity on unit circle
% 2) Basel problem and e series

theta = linspace(0, 2*pi, 400);
z = exp(1i*theta);
figure(1); plot(real(z), imag(z)); axis equal; grid on;
title('e^{i\theta} on unit circle'); xlabel('Re'); ylabel('Im');

% Basel problem
N = 1e5;
basel = sum(1./(1:N).^2);
fprintf('sum 1/n^2 to %d = %.10f, pi^2/6 = %.10f, err=%.2e\n', N, basel, pi^2/6, pi^2/6-basel);

% e via series
e_approx = sum(1./factorial(0:12));
fprintf('e approx = %.12f, error vs exp(1)=%.2e\n', e_approx, exp(1)-e_approx);

% Euler identity
fprintf('e^{i pi}+1 = %.2e + %.2ei (should be 0)\n', real(exp(1i*pi)+1), imag(exp(1i*pi)+1));
