% helper: Octave's built-in is powmod; alias for portability
if ~exist('powermod','file')
  function r = powermod(a,e,n), r = powmod(a,e,n); endfunction
endif

% --- Congruence basics --------------------------------------
mod(1777, 7)                     % Gauss's birth year on a 7-clock
mod(-3, 12)                      % Octave gives 9: always in 0..m-1

% --- A multiplication table mod 7 (a field!) ----------------
m = 7;
[K, J] = meshgrid(0:m-1);
mod(K .* J, m)                   % every nonzero row is a permutation

% --- Quadratic residues: which numbers are squares mod p? ---
p = 13;
QR = unique(mod((1:p-1).^2, p))  % -> 1 3 4 9 10 12 (exactly (p-1)/2)

% --- Euler's criterion links the two men directly -----------
% a is a square mod p  <=>  a^((p-1)/2) ≡ 1 (mod p)
a = 10;
powermod(a, (p-1)/2, p)          % 1 -> yes, 10 is a QR mod 13
a = 5;
powermod(a, (p-1)/2, p)          % p-1 (i.e. -1) -> not a square
