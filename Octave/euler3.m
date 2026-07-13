% --- Partial sums of the Basel series -----------------------
N = 100000;
n = 1:N;
partial = cumsum(1 ./ n.^2);
target  = pi^2 / 6;
printf('sum of 1/n^2 (N=%d): %.10f\n', N, partial(end));
printf('pi^2/6            : %.10f\n', target);
printf('remaining gap ~1/N: %.2e\n', target - partial(end));

% --- Visualize convergence ----------------------------------
semilogx(n, partial, 'linewidth', 1.5); hold on;
yline(target, '--');
xlabel('terms'); ylabel('partial sum');
title('Basel problem: crawling toward \pi^2/6');

% --- Euler product over primes vs the zeta sum, s = 2 --------
p = primes(2000);
euler_product = prod(1 ./ (1 - p.^(-2)));
printf('Euler product : %.10f\n', euler_product);
printf('zeta(2)       : %.10f\n', target);
% Two utterly different computations, one number.
