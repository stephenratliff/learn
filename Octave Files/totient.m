% helper: Octave's built-in is powmod; alias for portability
if ~exist('powermod','file')
  function r = powermod(a,e,n), r = powmod(a,e,n); endfunction
endif

% helper for portability: Octave builtin is powmod
if ~exist('powermod','file')
  function r = powermod(a,e,n), r = powmod(a,e,n); endfunction
endif

% --- Euler's totient from first principles ------------------
function t = totient(n)
  t = sum(gcd(1:n, n) == 1);
endfunction

arrayfun(@totient, 1:12)        % 1 1 2 2 4 2 6 4 6 4 10 4

% --- Verify Euler's theorem: a^phi(n) mod n == 1 ------------
n = 20; a = 7;                   % gcd(7,20)=1
printf('7^phi(20) mod 20 = %d\n', powermod(a, totient(n), n));

% --- Toy RSA in eight lines ---------------------------------
p = 61; q = 53;                  % (real keys use 300-digit primes)
n = p*q;                         % public modulus: 3233
phi = (p-1)*(q-1);               % Euler's totient: 3120
e = 17;                          % public exponent, coprime to phi
[g, d, ~] = gcd(e, phi); d = mod(d, phi);  % d = e^{-1} mod phi, requires g==1  % private key: e*d ≡ 1 mod phi
msg = 1707;                      % the message: Euler's birth year
c   = powermod(msg, e, n);       % encrypt with the PUBLIC key
back= powermod(c,   d, n);       % decrypt with the PRIVATE key
printf('message %d -> cipher %d -> decrypted %d\n', msg, c, back);
