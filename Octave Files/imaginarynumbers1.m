%% Gaussian Integer Arithmetic in GNU Octave
%% Represent a+bi as [a, b]; all operations return [real_part, imag_part]

function r = gn(z)
  r = z(1)^2 + z(2)^2;       % Gaussian norm N(a+bi) = a²+b²
end
function r = gmul(u, v)
  r = [u(1)*v(1)-u(2)*v(2),  u(1)*v(2)+u(2)*v(1)];
end
function [q, r] = gdivrem(alpha, beta)
  % α = q·β + r,  N(r) < N(β)
  nb = gn(beta);
  qr = (alpha(1)*beta(1) + alpha(2)*beta(2)) / nb;
  qi = (alpha(2)*beta(1) - alpha(1)*beta(2)) / nb;
  q  = [round(qr), round(qi)];
  r  = alpha - gmul(q, beta);
end
function g = ggcd(a, b)
  while any(b ~= 0)
    [~, r] = gdivrem(a, b);
    a = b; b = r;
  end
  g = a;
end
function tf = is_gaussian_prime(z)
  % A Gaussian integer z is prime if N(z) is prime, or
  % z = unit * p where p is an ordinary prime ≡ 3 (mod 4)
  n   = gn(z);
  tf  = isprime(n) || (z(2)==0 && isprime(abs(z(1))) && mod(abs(z(1)),4)==3) || ...
         (z(1)==0 && isprime(abs(z(2))) && mod(abs(z(2)),4)==3);
end

% Factoring 5 in Z[i]: 5 = (2+i)(2-i)
a = [2,1]; b = [2,-1];
prod = gmul(a,b);
printf('(2+i)(2-i) = %d+%di  [expect 5+0i]\n', prod(1), prod(2));
printf('2+i Gaussian prime? %d\n', is_gaussian_prime([2,1]));
printf('3   Gaussian prime? %d  (3≡3 mod 4)\n', is_gaussian_prime([3,0]));
printf('5   Gaussian prime? %d  (splits)\n',   is_gaussian_prime([5,0]));

% Gaussian GCD: gcd(11+3i, 1+8i)
g = ggcd([11,3], [1,8]);
printf('gcd(11+3i, 1+8i) = %d+%di\n', g(1), g(2));

% Print Gaussian primes with norm ≤ 25
printf('\nGaussian primes a+bi with 0≤a,b≤5:\n');
for a = 0:5; for b = 0:5
  if (a+b>0) && is_gaussian_prime([a,b])
    printf('  %d+%di (N=%d)\n', a, b, a^2+b^2);
  end
end; end

