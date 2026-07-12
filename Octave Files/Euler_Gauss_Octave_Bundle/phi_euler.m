function p = phi_euler(n)
% PHI_EULER Euler's totient function
% p = phi_euler(n) returns count of 1<=k<=n with gcd(k,n)==1
% Example: phi_euler(12) -> 4  (1,5,7,11)
  p = sum(gcd(1:n, n) == 1);
end
