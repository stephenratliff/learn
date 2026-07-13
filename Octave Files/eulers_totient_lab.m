%% =====================================================================
%%  EULER'S TOTIENT FUNCTION  phi(n)  --  A GNU Octave Worked Lab
%% =====================================================================
%%
%%  phi(n) = the count of integers k, 1 <= k <= n, with gcd(k, n) = 1.
%%
%%  This script works the totient out from first principles:
%%
%%    S1  Naive count straight from the definition
%%    S2  Euler's product formula  phi(n) = n * prod(1 - 1/p)
%%    S3  A table of phi(1..20) computed both ways (cross-check)
%%    S4  Worked example: phi(360) three different ways
%%    S5  Euler's theorem  a^phi(n) == 1 (mod n)  verified numerically
%%    S6  Fermat's little theorem as the prime special case
%%    S7  Gauss's identity  sum over divisors d|n of phi(d) = n
%%    S8  Toy RSA: the totient as the trapdoor
%%
%%  Run with:   octave eulers_totient_lab.m
%%  Companion to the interactive HTML guide "Euler's Totient Function".
%% =====================================================================

1;  % marks this file as a script

%% =====================================================================
%%  THE TOOLBOX -- Octave scripts require functions defined before use
%% =====================================================================

function t = totient_naive (n)
  %% phi(n) straight from the definition. O(n log n); fine for small n.
  t = sum(gcd(1:n, n) == 1);
end

function t = totient_fast (n)
  %% phi(n) via Euler's product formula over distinct prime divisors.
  if n == 1
    t = 1;                       % factor(1) is empty; handle explicitly
    return
  end
  p = unique(factor(n));
  t = round(n * prod(1 - 1 ./ p));   % round() clears float dust
end

function t = prime_power_phi (p, k)
  %% phi(p^k) = p^(k-1) * (p - 1)
  t = p^(k - 1) * (p - 1);
end

function r = mod_pow (a, e, n)
  %% Square-and-multiply modular exponentiation: a^e mod n.
  %% Never forms a^e itself, so it is safe for large exponents.
  r = 1;
  a = mod(a, n);
  while e > 0
    if mod(e, 2) == 1
      r = mod(r * a, n);
    end
    a = mod(a * a, n);
    e = floor(e / 2);
  end
end

function d = mod_inverse (e, m)
  %% Inverse of e mod m via the extended Euclidean algorithm.
  [old_r, r] = deal(e, m);
  [old_s, s] = deal(1, 0);
  while r != 0
    q = floor(old_r / r);
    [old_r, r] = deal(r, old_r - q * r);
    [old_s, s] = deal(s, old_s - q * s);
  end
  if old_r != 1
    error("mod_inverse: e = %d is not invertible mod %d", e, m);
  end
  d = mod(old_s, m);
end

function d = divisors_of (n)
  %% All positive divisors of n, in increasing order.
  k = 1:n;
  d = k(mod(n, k) == 0);
end

function s = yesno (tf)
  if tf, s = "YES"; else, s = "NO"; end
end

%% =====================================================================
%%  THE LAB
%% =====================================================================

printf("=====================================================\n");
printf(" EULER'S TOTIENT FUNCTION -- worked lab in GNU Octave\n");
printf("=====================================================\n\n");

%% --------------------------------------------------------------------
%% S1. The definition, verbatim: count k in 1..n with gcd(k,n) = 1
%% --------------------------------------------------------------------
%% gcd() in Octave is vectorized, so the whole definition is one line:
%% survivors of n = 12 should be 1, 5, 7, 11.

n = 12;
k = 1:n;
survivors = k(gcd(k, n) == 1);

printf("S1. Definition-based count, n = %d\n", n);
printf("    residues coprime to %d : %s\n", n, mat2str(survivors));
printf("    phi(%d) = %d\n\n", n, numel(survivors));

%% --------------------------------------------------------------------
%% S2. Euler's product formula: phi(n) = n * prod over p|n of (1 - 1/p)
%% --------------------------------------------------------------------
%% Each distinct prime divisor p "claims" the fraction 1/p of residues.
%% factor(360) = [2 2 2 3 3 5]; unique() keeps each prime once.

n = 360;
p = unique(factor(n));
phi360 = round(n * prod(1 - 1 ./ p));

printf("S2. Product formula, n = %d\n", n);
printf("    distinct primes of %d : %s\n", n, mat2str(p));
printf("    phi(%d) = %d * (1-1/2)(1-1/3)(1-1/5) = %d\n\n", n, n, phi360);

%% --------------------------------------------------------------------
%% S3. Cross-check the two methods on n = 1..20
%% --------------------------------------------------------------------

N = 20;
naive = arrayfun(@totient_naive, 1:N);
fast  = arrayfun(@totient_fast,  1:N);

printf("S3. phi(n) for n = 1..%d, both methods\n", N);
printf("      n : %s\n", sprintf("%4d", 1:N));
printf("    phi : %s\n", sprintf("%4d", fast));
if isequal(naive, fast)
  printf("    naive and product-formula versions AGREE on all %d values.\n\n", N);
else
  printf("    *** DISAGREEMENT -- check the implementations! ***\n\n");
end

%% --------------------------------------------------------------------
%% S4. Worked example: phi(360) three ways
%% --------------------------------------------------------------------
%% 360 = 2^3 * 3^2 * 5.
%%   (a) brute count of coprime residues
%%   (b) product formula
%%   (c) multiplicativity: phi(8) * phi(9) * phi(5), using
%%       phi(p^k) = p^(k-1) * (p - 1) on each prime power.

a = totient_naive(360);
b = totient_fast(360);
c = prime_power_phi(2,3) * prime_power_phi(3,2) * prime_power_phi(5,1);

printf("S4. phi(360) three ways        (360 = 2^3 * 3^2 * 5)\n");
printf("    (a) brute-force count        : %d\n", a);
printf("    (b) product formula          : %d\n", b);
printf("    (c) phi(8)*phi(9)*phi(5)     : %d * %d * %d = %d\n", ...
        prime_power_phi(2,3), prime_power_phi(3,2), prime_power_phi(5,1), c);
printf("    all three agree: %s\n\n", yesno(a == b && b == c));

%% --------------------------------------------------------------------
%% S5. Euler's theorem: gcd(a,n)=1  =>  a^phi(n) == 1 (mod n)
%% --------------------------------------------------------------------
%% Verified with square-and-multiply exponentiation (mod_pow, below),
%% for EVERY unit a mod 360 -- all 96 of them.

n   = 360;
phn = totient_fast(n);
units = find(gcd(1:n, n) == 1);
ok = arrayfun(@(a) mod_pow(a, phn, n) == 1, units);

printf("S5. Euler's theorem, n = %d, phi(n) = %d\n", n, phn);
printf("    a^%d mod %d == 1 for all %d units a : %s\n", ...
        phn, n, numel(units), yesno(all(ok)));
printf("    spot check: 7^%d mod %d = %d\n\n", phn, n, mod_pow(7, phn, n));

%% Practical corollary: exponents reduce mod phi(n).
%% 7^2026 mod 12: phi(12) = 4, and 2026 = 4*506 + 2, so it equals 7^2 mod 12.
e_big = 2026;  n = 12;  phn = totient_fast(n);
printf("    exponent reduction: 7^%d mod %d = %d  (= 7^%d mod %d, since %d mod %d = %d)\n\n", ...
        e_big, n, mod_pow(7, e_big, n), mod(e_big, phn), n, e_big, phn, mod(e_big, phn));

%% --------------------------------------------------------------------
%% S6. Fermat's little theorem: the prime special case
%% --------------------------------------------------------------------
%% For prime p, phi(p) = p - 1, so Euler's theorem reads
%% a^(p-1) == 1 (mod p) for all a not divisible by p.

p = 31;
ok = arrayfun(@(a) mod_pow(a, p - 1, p) == 1, 1:(p-1));
printf("S6. Fermat's little theorem, p = %d (phi(%d) = %d)\n", p, p, p-1);
printf("    a^%d mod %d == 1 for all a in 1..%d : %s\n\n", ...
        p-1, p, p-1, yesno(all(ok)));

%% --------------------------------------------------------------------
%% S7. Gauss's identity: sum over divisors d of n of phi(d) = n
%% --------------------------------------------------------------------
%% The residues 1..n partition by gcd: exactly phi(n/d) of them have
%% gcd = d with n. Summing the classes recovers n itself.

printf("S7. Gauss's identity  sum_{d|n} phi(d) = n\n");
for n = [12 30 360]
  d = divisors_of(n);
  s = sum(arrayfun(@totient_fast, d));
  printf("    n = %3d : divisors %s\n", n, mat2str(d));
  printf("              sum of phi over divisors = %d  -> %s\n", s, yesno(s == n));
end
printf("\n");

%% --------------------------------------------------------------------
%% S8. Toy RSA: phi(n) is the trapdoor
%% --------------------------------------------------------------------
%% Real RSA uses ~2048-bit n. The arithmetic is identical at toy scale.
%%   keygen : n = p*q,  phi = (p-1)(q-1),  pick e coprime to phi,
%%            d = e^{-1} mod phi   (extended Euclid via gcd -- here brute)
%%   encrypt: c = m^e mod n        decrypt: m = c^d mod n
%% Decryption works because ed == 1 (mod phi(n)) + Euler's theorem.

p = 61;  q = 53;
n   = p * q;                    % 3233 -- public
phn = (p - 1) * (q - 1);        % 3120 -- SECRET (needs the factors!)
e   = 17;                       % public exponent, gcd(17, 3120) = 1
d   = mod_inverse(e, phn);      % private exponent

m = 1234;                       % the "message"
c = mod_pow(m, e, n);           % encrypt with the PUBLIC key
m2 = mod_pow(c, d, n);          % decrypt with the PRIVATE key

printf("S8. Toy RSA with p = %d, q = %d\n", p, q);
printf("    public  : n = %d, e = %d\n", n, e);
printf("    secret  : phi(n) = (p-1)(q-1) = %d,  d = e^-1 mod phi = %d\n", phn, d);
printf("    check   : e*d mod phi(n) = %d\n", mod(e*d, phn));
printf("    message m  = %d\n", m);
printf("    cipher  c  = m^e mod n = %d\n", c);
printf("    decrypt m' = c^d mod n = %d   round trip OK: %s\n\n", m2, yesno(m2 == m));

printf("    The asymmetry: knowing p, q makes phi(n) trivial;\n");
printf("    knowing only n = %d, an attacker must factor it first.\n", n);
printf("    (Recovering phi(n) from n is provably as hard as factoring.)\n\n");

printf("================================ end of lab =========\n");
