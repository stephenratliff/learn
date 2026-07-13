% GAUSSIAN_INTEGERS Explore Z[i]
% Norm N(a+bi)=a^2+b^2. Prime in Z[i] iff norm is prime or (a==0 or b==0 and |other| prime 3 mod 4)

function is_gi_prime = is_gaussian_prime(a,b)
  if a==0 || b==0
    p = abs(a+b*1i); % actually abs gives sqrt, use abs(a)+abs(b)
    n = abs(a)+abs(b);
    is_gi_prime = isprime(n) && mod(n,4)==3;
  else
    is_gi_prime = isprime(a^2+b^2);
  end
end

% demo grid
[A,B]=meshgrid(-5:5,-5:5);
for i=1:numel(A)
  a=A(i); b=B(i);
  if a==0 && b==0, continue; end
  N=a^2+b^2;
  if isprime(N)
    fprintf('%2d+%2di N=%3d prime in Z[i]\n', a,b,N);
  end
end

% Gaussian integer factorization demo via norm
z = 5+2i; fprintf('Norm of %s = %d\n', mat2str(z), real(z)^2+imag(z)^2);
