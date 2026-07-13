% EULER_PRODUCT_ZETA Approximates zeta(s) via Euler product over primes
s = 2; % Basel -> pi^2/6
primes_list = primes(100);
prod_est = prod(1./(1 - primes_list.^(-s)));
fprintf('Euler product over primes <=100 for zeta(%d)=%.8f, true=%.8f\n', s, prod_est, sum(1./(1:1e6).^s));
