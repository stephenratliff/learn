Euler & Gauss Octave Lab Bundle
-------------------------------
All files run in GNU Octave 7+ with no toolboxes.

Files:
 phi_euler.m            - Euler's totient
 totient_sieve.m        - visualize coprimes
 euler_identity_basel.m - e^{i pi}, Basel sum, e series
 euler_method.m         - explicit Euler ODE integrator
 euler_product_zeta.m   - Euler product for zeta(s)
 konigsberg_check.m     - Eulerian trail condition, V-E+F
 modular_clock.m        - congruence a mod m visualization
 gaussian_integers.m    - Z[i] norm and prime test
 gaussian_bell.m        - normal distribution 68-95-99.7
 gauss_fit.m            - least squares (Gauss 1809)
 curvature_demo.m       - Theorema Egregium K = kappa1*kappa2

Usage:
 octave> phi_euler(12)
 octave> euler_method(@(x,y) -1.5*y, 0,1,4,0.2)
 octave> gauss_fit((0:10)', 2*(0:10)'+randn(11,1))
 octave> gaussian_bell(0,1)
 octave> curvature_demo(1,1)
 octave> modular_clock(7,12)

These correspond 1-to-1 with the interactive demos in the HTML compendium.
