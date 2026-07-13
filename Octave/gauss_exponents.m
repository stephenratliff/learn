% A signal with two hidden tones + noise -----------------------
fs = 512;  t = (0:fs-1)/fs;
sig = sin(2*pi*17*t) + 0.6*sin(2*pi*60*t) + 0.4*randn(size(t));
%              ^ a 17 Hz tone, in Gauss's honor

% The DFT is literally a matrix of Euler's formula --------------
N = numel(sig);
[k, n] = meshgrid(0:N-1);
W = exp(-2i*pi*k.*n/N);          % e^{-2πikn/N}: pure Euler
slow = W * sig.';                 % O(N^2) multiply

fast = fft(sig).';               % O(N log N): pure Gauss
max(abs(slow - fast))            % ~1e-10: same numbers

% Time them ------------------------------------------------------
tic; W * sig.';   t_slow = toc;
tic; fft(sig);    t_fast = toc;
printf('matrix DFT: %.4fs   fft: %.6fs   speedup: %.0fx\n', ...
       t_slow, t_fast, t_slow/max(t_fast,eps));

% Find the hidden tones ------------------------------------------
P = abs(fast)/N;
f = (0:N-1)*fs/N;
plot(f(1:N/2), 2*P(1:N/2), 'linewidth', 1.5);
xlabel('Hz'); title('Spectrum: peaks at 17 and 60 Hz');
