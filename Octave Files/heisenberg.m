% Matrix mechanics in ten lines: build X and P for the harmonic
% oscillator (hbar = m = omega = 1), truncated to N levels, and
% verify  X*P - P*X = i*eye(N)  ... except the truncation corner.

N = 6;
n = 1:N-1;
a = diag(sqrt(n), 1);            % annihilation operator: a|n> = sqrt(n)|n-1>
X = (a + a') / sqrt(2);
P = 1i * (a' - a) / sqrt(2);

C = X*P - P*X;                   % the commutator
disp("imag(diag(C)) — expect all ones, last entry -(N-1):")
disp(imag(diag(C))')

% Why the corner is wrong: trace(X*P - P*X) = 0 identically for
% finite matrices, but trace(i*eye(N)) = i*N. Heisenberg's arrays
% must be infinite; the -(N-1) is the escape hatch.
printf("trace check: %.1f (always zero for finite N)\n", trace(imag(C)));

% Kennard's bound by direct computation: build a Gaussian wave
% packet, get its momentum distribution with an FFT, and measure
% sigma_x * sigma_p. Gaussians saturate the bound: product = 0.5.

L = 200;  Npts = 2^12;  hbar = 1;
x  = linspace(-L/2, L/2, Npts);  dx = x(2) - x(1);
sx = 2.0;                                  % try 0.5, 2, 8 ...

psi = exp(-x.^2 / (4*sx^2));
psi = psi / sqrt(sum(abs(psi).^2) * dx);   % normalize

p    = fftshift((-Npts/2 : Npts/2-1) * 2*pi*hbar/(Npts*dx));
phi  = fftshift(fft(psi)) * dx / sqrt(2*pi*hbar);
Pp   = abs(phi).^2;  Pp = Pp / (sum(Pp) * (p(2)-p(1)));

sigx = sqrt(sum(x.^2  .* abs(psi).^2) * dx);
sigp = sqrt(sum(p.^2  .* Pp) * (p(2)-p(1)));
printf("sigma_x = %.4f   sigma_p = %.4f   product = %.4f  (bound 0.5)\n", ...
       sigx, sigp, sigx*sigp);

% Sharpen the packet (smaller sx) and sigma_p rises to compensate.
% Replace the Gaussian with any other shape: the product only grows.
