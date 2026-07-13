% TOTIENT_SIEVE Visualize coprimes up to n
n = 36;  % change this
cop = gcd(1:n, n)==1;
phi = sum(cop);
fprintf('phi(%d) = %d\n', n, phi);
fprintf('coprimes: '); disp(find(cop));
stem(1:n, cop, 'filled'); ylim([-0.2 1.5]);
title(sprintf('Coprimes to %d (phi=%d)', n, phi));
xlabel('k'); ylabel('gcd(k,n)==1');
