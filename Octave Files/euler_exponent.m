%% Euler's formula: the circle as a complex exponential

% Verify Euler's formula numerically
theta = linspace(0, 2*pi, 7);
printf('θ(deg)   e^(iθ) computed        cos+i·sin\n');
for t = theta
  euler = exp(1i*t);
  trig  = cos(t) + 1i*sin(t);
  printf('%6.1f°  %+.4f%+.4fi    %+.4f%+.4fi   match:%d\n', ...
    rad2deg(t), real(euler), imag(euler), ...
    real(trig), imag(trig), abs(euler-trig)<1e-10);
end

% Encryption as rotation: multiply by e^(iθ) rotates the complex plane
% This is the Cayley-Klein parameterization of rotations — same algebra as RSA
msg   = 3 + 4*1i;        % complex message
key   = exp(1i*pi/3);   % rotation by 60°
enc   = msg * key;
dec   = enc * conj(key); % rotate back (inverse = conjugate on unit circle)
printf('\nMessage:   %+.4f%+.4fi\n', real(msg), imag(msg));
printf('Encrypted: %+.4f%+.4fi  (rotated 60°)\n', real(enc), imag(enc));
printf('Decrypted: %+.4f%+.4fi  (back to start)\n', real(dec), imag(dec));

