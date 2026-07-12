UNIFIED FIELD Octave Bundle — Fourier, Maxwell, Crypto, Curvature, Strings, Zeta
--------------------------------------------------------------------------------
GNU Octave 7+ , no toolboxes.

Files:
 fourier_machinery.m     - Fourier series synthesis, FFT spectrum, Parseval, Gibbs
 maxwell_circuits.m      - EM plane wave e^{i(kx-wt)}, Helmholtz, RLC Z=R+i(wL-1/wC), transfer H(w), resonance w0=1/sqrt(LC)
 crypto_gauss.m          - Gauss totient phi, Euler theorem a^phi=1 mod n, extended Euclid modinv, fast modpow, RSA toy, Diffie-Hellman g^ab
 curvature_strings.m     - Gaussian curvature K=4ab/(1+4a^2u^2+4b^2v^2)^2, saddle vs sphere, string vibration modes sin(n pi x/L), Calabi-Yau Ricci-flat note
 zeta_basel.m            - Basel sum pi^2/6, Euler product prod(1-p^{-s})^{-1}, zeta(2), zeta(4), zeta(-1)=-1/12, zeta(-3)=1/120, Casimir -pi^2/240 hbar c / d^4, pi(x) ~ x/log x
 phasor_impedance.m      - Phasor diagram V=IZ, VR+VL+VC, |Z| arg(Z)
 hilbert_curve_zeta.m    - Space-filling curve [0,1]->[0,1]^2, cardinality, link to Hilbert space completeness

Connections:
 Fourier -> Maxwell: time->freq gives Helmholtz, waves are Fourier modes
 Fourier -> Circuits: phasor analysis, Bode plots, RLC resonance
 Gauss phi/mod -> Crypto: RSA ed=1 mod phi(N), security = factoring
 Gauss K intrinsic -> Strings: K -> Riemann R_{ijkl} -> Ricci flat Calabi-Yau R_{ij}=0 -> 6 extra dimensions, Polyakov action
 Basel zeta(2) -> Zeta: Euler product links primes to analysis, zeta regularization gives string critical dimension D=26 via 1+2+...=-1/12 and Casimir energy

Usage:
 octave> fourier_machinery()
 octave> maxwell_circuits()
 octave> crypto_gauss()
 octave> curvature_strings()
 octave> zeta_basel()
 octave> phasor_impedance()
 octave> hilbert_curve_zeta(5)
