% --- totient_naive.m : straight from the definition ---
function t = totient_naive(n)
  t = sum(gcd(1:n, n) == 1);
end

% --- totient_fast.m : Euler's product formula ---
function t = totient_fast(n)
  p = unique(factor(n));      % distinct prime divisors
  t = n * prod(1 - 1 ./ p);   % n * prod(1 - 1/p)
  t = round(t);               % clean up float dust
end

% --- sanity checks ---
totient_fast(12)               % ans = 4
totient_fast(360)              % ans = 96
arrayfun(@totient_naive, 1:12) % 1 1 2 2 4 2 6 4 6 4 10 4

% --- verify Euler's theorem: a^phi(n) ≡ 1 (mod n) ---
n = 360;  a = 7;               % gcd(7,360) = 1
powermod = @(a,e,n) mod_pow(a,e,n);  % see below

function r = mod_pow(a, e, n)  % square-and-multiply
  r = 1;  a = mod(a, n);
  while e > 0
    if mod(e, 2) == 1, r = mod(r*a, n); end
    a = mod(a*a, n);  e = floor(e/2);
  end
end

mod_pow(7, totient_fast(360), 360)   % ans = 1  ✓ Euler
