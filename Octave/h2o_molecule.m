% ==============================================================================
%  h2o_molecule.m
%
%  Water: H₂O as a Quantum Three-Body Problem
%  ─────────────────────────────────────────────────────────────────────────────
%  The same three-body framework that governs Newton's gravitational problem
%  governs the water molecule -- but the "force law" is quantum covalent
%  bonding rather than gravity.
%
%  THREE-BODY ANALOGY:
%    Gravitational    |   Molecular (H₂O)
%    ─────────────────|──────────────────────────────────────────────────
%    Body 1 (left)    |   Hydrogen atom H1
%    Body 2 (right)   |   Hydrogen atom H2
%    Body 3 (middle)  |   Oxygen atom O  ← the quantum "glue"
%    Gravity          |   Covalent bond (shared electron quantum state)
%    F = Gm/r²        |   F = -dV/dr  (harmonic stretch + angle bend)
%    Newton (1687)    |   Schrodinger (1926)
%
%  COVALENT BOND = SCHRODINGER'S CAT FOR ELECTRONS
%  ─────────────────────────────────────────────────────────────────────────────
%  Each O-H bond electron is in quantum superposition:
%
%      |psi_bond> = c_O |electron on O> + c_H |electron on H>
%
%  This is Schrodinger's equation applied to chemistry. The shared electron
%  is NEITHER purely on O nor purely on H -- it exists in both states
%  simultaneously (LCAO: Linear Combination of Atomic Orbitals).
%  The resulting charge density between the atoms IS the covalent bond.
%
%  H₂O MOLECULAR PROPERTIES:
%  ─────────────────────────────────────────────────────────────────────────────
%  Bond length   r_OH   =  0.9572 Å             (1 Å = 10^-10 m)
%  Bond angle    θ_HOH  =  104.52°              (bent, not linear, due to lone pairs)
%  Dipole moment μ      =  1.85 Debye           (polar molecule; ice floats because of this)
%  O mass        m_O    =  15.9994 amu           (1 amu = 1.66054 × 10^-27 kg)
%  H mass        m_H    =  1.00794 amu
%
%  THREE VIBRATIONAL NORMAL MODES (IR active):
%    ν₁  symmetric stretch   ω₁ = 3657 cm⁻¹   T₁ =  9.1 fs
%    ν₂  bending (scissor)   ω₂ = 1595 cm⁻¹   T₂ = 20.9 fs
%    ν₃  asymmetric stretch  ω₃ = 3756 cm⁻¹   T₃ =  8.9 fs
%
%  POTENTIAL ENERGY MODEL (harmonic force field):
%    V = ½ k_r (r_OH1 - r₀)² + ½ k_r (r_OH2 - r₀)² + ½ k_θ (θ - θ₀)²
%    k_r = 0.47 amu/fs²   (O-H stretch force constant)
%    k_θ = 0.045 amu·Å²/fs²/rad²  (H-O-H bend force constant)
%
%  QUANTUM MECHANICS (O-H stretch, harmonic oscillator):
%    Ĥ ψ_n = E_n ψ_n     Schrodinger's time-independent equation
%    E_n = (n + ½) ħ ω   (quantized energy levels)
%    Zero-point energy E₀ = ħω/2 ≈ 0.23 eV  (bond vibrates even at T=0!)
%    ψ_n(r) = N_n · H_n(ξ/α) · exp(-ξ²/2α²)   (Hermite-Gaussian)
%    α = √(ħ/μω) ≈ 0.069 Å   (quantum position uncertainty)
%
%  DEMONSTRATIONS:
%  ─────────────────────────────────────────────────────────────────────────────
%  A  --  Molecular Geometry      (bond lengths, angle, dipole, lone pairs)
%  B  --  Normal Mode Analysis    (Hessian → eigenvalues → vibrational modes)
%  C  --  Classical Molecular MD  (ode45, same solver as gravitational 3-body)
%  D  --  FFT Vibrational Spectrum  (MD trajectory → frequency peaks)
%  E  --  Quantum HO Wavefunctions  (Schrodinger equation for O-H bond)
%  F  --  LCAO Covalent Bond       (electron superposition = chemical bond)
%
%  UNITS THROUGHOUT:
%    Length:  Ångström (Å)          1 Å  = 1e-10 m
%    Mass:    atomic mass unit (amu) 1 amu = 1.66054e-27 kg
%    Time:    femtosecond (fs)       1 fs  = 1e-15 s
%    Energy:  eV  or  cm⁻¹
%    hbar     = 0.006351 amu·Å²/fs
%
%  USAGE:  octave h2o_molecule.m
%
%  OUTPUT:
%    h2o_geometry.png    --  molecular structure and bond parameters
%    h2o_modes.png       --  normal mode displacement patterns
%    h2o_dynamics.png    --  MD time evolution and FFT spectrum
%    h2o_quantum.png     --  QHO wavefunctions and LCAO bonding
% ==============================================================================

clear all; close all; clc;

printf('\n');
printf('==============================================================\n');
printf('  H2O Water Molecule -- Quantum Three-Body Problem\n');
printf('  GNU Octave Simulation\n');
printf('==============================================================\n\n');


% ==============================================================================
%  PHYSICAL PARAMETERS
% ==============================================================================

% Molecular geometry (experimental values)
r0_OH  = 0.9572;                    % O-H bond length [Ang]
theta0 = 104.52 * pi / 180;         % H-O-H bond angle [rad]

% Masses
m_H = 1.00794;                      % hydrogen [amu]
m_O = 15.9994;                      % oxygen   [amu]

% Force field (harmonic potential)
k_r = 0.47;                         % O-H stretch force constant [amu/fs^2]
k_t = 0.045;                        % H-O-H bend force constant  [amu*Ang^2/fs^2/rad^2]

% Quantum / unit-conversion constants
hbar  = 0.006351;                   % reduced Planck constant [amu*Ang^2/fs]
C_WN  = 1e15 / (2*pi*2.99792e10);  % rad/fs --> cm^-1  (= 5308.84)
C_EV  = 1.66054e-17 / 1.60218e-19; % amu*Ang^2/fs^2 --> eV  (= 103.64)
a0    = 0.529177;                   % Bohr radius [Ang]

% Experimental vibrational frequencies [cm^-1]
nu_exp = [1595, 3657, 3756];

% ODE solver options (same tight tolerances as gravitational simulation)
opts = odeset('RelTol', 1e-10, 'AbsTol', 1e-12);

printf('Force-field parameters:\n');
printf('  k_r = %.4f amu/fs^2     (O-H stretch)\n', k_r);
printf('  k_t = %.4f amu*Ang^2/fs^2/rad^2  (H-O-H bend)\n', k_t);
printf('  hbar = %.6f amu*Ang^2/fs\n', hbar);
printf('  C_WN (rad/fs -> cm^-1) = %.2f\n\n', C_WN);


% ==============================================================================
%  EQUILIBRIUM GEOMETRY
%
%  O placed at origin; molecule symmetric about y-axis.
%  H atoms below O, separated by the H-O-H angle.
%
%       O  (0, 0)
%      / \
%  H1 /   \ H2
%    (-x,-y)  (+x,-y)   where x = r0*sin(θ/2), y = r0*cos(θ/2)
% ==============================================================================

x_O  = 0.0;  y_O  = 0.0;
x_H1 = -r0_OH * sin(theta0/2);   y_H1 = -r0_OH * cos(theta0/2);
x_H2 =  r0_OH * sin(theta0/2);   y_H2 = -r0_OH * cos(theta0/2);

q_eq = [x_O; y_O; x_H1; y_H1; x_H2; y_H2];   % equilibrium state vector

% Mass vector for each degree of freedom [m_O m_O m_H m_H m_H m_H]
mass_dof = [m_O; m_O; m_H; m_H; m_H; m_H];

printf('Equilibrium geometry:\n');
printf('  O  = (%.4f, %.4f) Ang\n', x_O, y_O);
printf('  H1 = (%.4f, %.4f) Ang\n', x_H1, y_H1);
printf('  H2 = (%.4f, %.4f) Ang\n', x_H2, y_H2);
printf('  Bond angle theta0 = %.2f deg\n\n', theta0*180/pi);


% ==============================================================================
%  PART B  --  NORMAL MODE ANALYSIS
%
%  The Hessian (force constant matrix) is computed by finite differences
%  of the force function -- exactly as in numerical linear algebra.
%  The mass-weighted Hessian (dynamical matrix) D_ij = H_ij / sqrt(m_i * m_j)
%  has eigenvalues omega_k^2 and eigenvectors giving the mode shapes.
%
%  For a nonlinear molecule with N=3 atoms in 2D:
%    2*N = 6 degrees of freedom
%    -2 translations (COM motion in x,y)
%    -1 rotation
%    = 3 vibrational modes
% ==============================================================================

printf('PART B: Normal Mode Analysis\n');
printf('--------------------------------------------------------------\n');

% Compute Hessian: H_ij = -dF_i/dq_j = d^2V/(dq_i dq_j)
n_dof = 6;
H_mat = zeros(n_dof, n_dof);
dq    = 1e-5;   % finite difference step [Ang]

for i = 1:n_dof
  qp = q_eq; qp(i) = qp(i) + dq;
  qm = q_eq; qm(i) = qm(i) - dq;
  F_plus  = compute_forces(qp, k_r, k_t, r0_OH, theta0);
  F_minus = compute_forces(qm, k_r, k_t, r0_OH, theta0);
  H_mat(:,i) = -(F_plus - F_minus) / (2*dq);
end
H_mat = (H_mat + H_mat') / 2;   % symmetrize (numerical noise)

% Mass-weighted dynamical matrix
D_mat = H_mat ./ sqrt(mass_dof * mass_dof');

% Diagonalize: D * V = V * Lambda
[V_modes, Lambda] = eig(D_mat);
omega2_all = diag(Lambda);

% Extract vibrational modes (positive eigenvalues only)
vib_mask = omega2_all > 1e-3;
omega2_vib = omega2_all(vib_mask);
V_vib      = V_modes(:, vib_mask);

% Sort by ascending frequency
[omega2_vib, sort_idx] = sort(omega2_vib);
V_vib = V_vib(:, sort_idx);

omega_vib = sqrt(omega2_vib);          % angular frequencies [rad/fs]
nu_calc   = omega_vib * C_WN;          % [cm^-1]

% Atomic displacements for each mode (unnormalize from mass-weighted coords)
displ = zeros(n_dof, 3);
mode_names = {'Bending (scissor)', 'Symmetric stretch', 'Asymmetric stretch'};
for k = 1:3
  for j = 1:n_dof
    displ(j,k) = V_vib(j,k) / sqrt(mass_dof(j));
  end
  % Normalize displacements to unit max displacement for arrow scaling
  displ(:,k) = displ(:,k) / max(abs(displ(:,k)));
end

printf('  Normal mode frequencies:\n');
printf('  Mode   Computed   Experimental   Assignment\n');
printf('  ─────────────────────────────────────────────────────────\n');
for k = 1:3
  printf('  %d      %4.0f cm^-1   %4d cm^-1     %s\n', ...
         k, nu_calc(k), nu_exp(k), mode_names{k});
end
printf('\n');
printf('  Displacement vectors (normalized, from Hessian eigenvectors):\n');
for k = 1:3
  printf('  Mode %d: dO=(%+.3f,%+.3f)  dH1=(%+.3f,%+.3f)  dH2=(%+.3f,%+.3f)\n', ...
         k, displ(1,k), displ(2,k), displ(3,k), displ(4,k), displ(5,k), displ(6,k));
end
printf('\n');


% ==============================================================================
%  PART C  --  CLASSICAL MOLECULAR DYNAMICS  (ode45)
%
%  The molecular ODE has EXACTLY the same structure as the gravitational
%  three-body problem: 12 coupled first-order ODEs (3 atoms x 2D x 2 eqs).
%
%  State vector (identical structure to gravitational case):
%    y = [x_O, Y_O, x_H1, Y_H1, x_H2, Y_H2,
%         vx_O, vY_O, vx_H1, vY_H1, vx_H2, vY_H2]
%
%  The ONLY difference: force law.
%    Gravity:  F = -G*m*M/r^2 * r_hat  (power law, long range)
%    H2O:      F = -dV/dr  (harmonic springs for bonds + angle)
%
%  We simulate THREE initial conditions, one per normal mode:
%    IC1: symmetric stretch  (displace both H outward along bonds)
%    IC2: bending            (displace H atoms laterally)
%    IC3: combined kick      (excites all 3 modes; use FFT to see spectrum)
% ==============================================================================

printf('PART C: Classical Molecular Dynamics  (ode45, 3 initial conditions)\n');
printf('--------------------------------------------------------------\n');

t_end  = 120.0;   % femtoseconds  (~6 bending periods, ~13 stretch periods)
tspan  = [0, t_end];
N_time = 3000;
t_uni  = linspace(0, t_end, N_time)';

% Arrow scale for displacement perturbations
A_stretch = 0.06;   % Ang perturbation amplitude for stretch
A_bend    = 0.05;   % Ang perturbation amplitude for bending

% IC1: Symmetric stretch -- displace H atoms outward along their bonds
q_sym = q_eq;
u1_hat = [x_H1 - x_O; y_H1 - y_O] / r0_OH;   % unit O->H1
u2_hat = [x_H2 - x_O; y_H2 - y_O] / r0_OH;   % unit O->H2
q_sym(3:4) = q_sym(3:4) + A_stretch * u1_hat;
q_sym(5:6) = q_sym(5:6) + A_stretch * u2_hat;
y0_sym = [q_sym; zeros(6,1)];   % zero initial velocities

% IC2: Bending -- displace H atoms perpendicular to their bonds (toward each other)
perp1 = [ u1_hat(2); -u1_hat(1)];   % rotate u1 by -90 (inward)
perp2 = [-u2_hat(2);  u2_hat(1)];   % rotate u2 by +90 (inward)
q_bend = q_eq;
q_bend(3:4) = q_bend(3:4) + A_bend * perp1;
q_bend(5:6) = q_bend(5:6) + A_bend * perp2;
y0_bend = [q_bend; zeros(6,1)];

% IC3: Combined kick (arbitrary displacement -- excites all modes)
q_combo = q_eq;
q_combo(3:4) = q_combo(3:4) + A_stretch * u1_hat + 0.5*A_bend*perp1;
q_combo(5:6) = q_combo(5:6) - 0.3*A_stretch * u2_hat + 0.5*A_bend*perp2;
y0_combo = [q_combo; zeros(6,1)];

% Run all three MD simulations
printf('  MD run 1: symmetric stretch IC...\n');
tic; [t_s, Y_s] = ode45(@(t,y) h2o_ode(t, y, k_r, k_t, m_H, m_O, r0_OH, theta0), ...
                          tspan, y0_sym, opts);
printf('  Done: %.3f s  |  %d steps\n', toc, numel(t_s));

printf('  MD run 2: bending IC...\n');
tic; [t_b, Y_b] = ode45(@(t,y) h2o_ode(t, y, k_r, k_t, m_H, m_O, r0_OH, theta0), ...
                          tspan, y0_bend, opts);
printf('  Done: %.3f s  |  %d steps\n', toc, numel(t_b));

printf('  MD run 3: combined IC (all modes excited)...\n');
tic; [t_c, Y_c] = ode45(@(t,y) h2o_ode(t, y, k_r, k_t, m_H, m_O, r0_OH, theta0), ...
                          tspan, y0_combo, opts);
printf('  Done: %.3f s  |  %d steps\n', toc, numel(t_c));

% Interpolate all onto common grid and extract observables
Yi_s = interp1(t_s, Y_s, t_uni);
Yi_b = interp1(t_b, Y_b, t_uni);
Yi_c = interp1(t_c, Y_c, t_uni);

% O-H bond lengths and H-O-H angle from each run
[rOH1_s, rOH2_s, theta_s] = bond_observables(Yi_s);
[rOH1_b, rOH2_b, theta_b] = bond_observables(Yi_b);
[rOH1_c, rOH2_c, theta_c] = bond_observables(Yi_c);

printf('\n  Bond oscillation amplitudes (symmetric stretch IC):\n');
printf('  max(r_OH1 - r0) = %.4f Ang\n', max(abs(rOH1_s - r0_OH)));
printf('  max(theta - t0) = %.4f deg\n', max(abs((theta_s - theta0)*180/pi)));
printf('\n  Bond oscillation amplitudes (bending IC):\n');
printf('  max(r_OH1 - r0) = %.4f Ang\n', max(abs(rOH1_b - r0_OH)));
printf('  max(theta - t0) = %.4f deg\n', max(abs((theta_b - theta0)*180/pi)));
printf('\n');

% Energy conservation check
E0_sym   = h2o_energy(y0_sym,   m_H, m_O, k_r, k_t, r0_OH, theta0);
E0_bend  = h2o_energy(y0_bend,  m_H, m_O, k_r, k_t, r0_OH, theta0);
Ef_sym   = h2o_energy(Yi_s(end,:)', m_H, m_O, k_r, k_t, r0_OH, theta0);
Ef_bend  = h2o_energy(Yi_b(end,:)', m_H, m_O, k_r, k_t, r0_OH, theta0);
printf('  Energy conservation:\n');
printf('  Stretch run |dE/E| = %.2e\n', abs(Ef_sym-E0_sym)/abs(E0_sym));
printf('  Bend    run |dE/E| = %.2e\n\n', abs(Ef_bend-E0_bend)/abs(E0_bend));


% ==============================================================================
%  PART D  --  FFT VIBRATIONAL SPECTRUM
%
%  The Fourier transform of r_OH1(t) from the combined run reveals all three
%  normal mode frequencies as sharp peaks -- just as an IR spectrometer would
%  detect them experimentally via molecular absorption of light.
%
%  This directly connects: MD trajectory --> experimental IR spectrum.
% ==============================================================================

% FFT of bond length oscillation in combined run
dr_OH1 = rOH1_c - mean(rOH1_c);   % remove mean (DC component)
N_fft  = N_time;
dt_fft = t_end / (N_time - 1);    % femtoseconds

fft_amp  = abs(fft(dr_OH1));
fft_amp  = fft_amp(1:floor(N_fft/2));
freq_fs  = (0:floor(N_fft/2)-1) / (N_fft * dt_fft);   % [1/fs = fs^-1]
nu_fft   = freq_fs * C_WN;                               % [cm^-1]

% Find the three main peaks
[~, peak_order] = sort(fft_amp(nu_fft < 5000), 'descend');
peak_idx = peak_order(1:min(10, numel(peak_order)));
% Filter: keep only well-separated peaks
peak_keep = [];
for k = 1:numel(peak_idx)
  if isempty(peak_keep) || min(abs(nu_fft(peak_idx(k)) - nu_fft(peak_keep))) > 100
    peak_keep(end+1) = peak_idx(k);
  end
end
peak_keep = peak_keep(1:min(3, numel(peak_keep)));
nu_peaks  = sort(nu_fft(peak_keep));

printf('PART D: FFT Vibrational Spectrum\n');
printf('--------------------------------------------------------------\n');
printf('  Peaks extracted from FFT of combined MD run:\n');
printf('  Peak     FFT [cm^-1]   Experimental [cm^-1]   Assignment\n');
for k = 1:min(3, numel(nu_peaks))
  printf('  %d        %4.0f           %4d                   %s\n', ...
         k, nu_peaks(k), nu_exp(k), mode_names{k});
end
printf('\n');


% ==============================================================================
%  PART E  --  QUANTUM HARMONIC OSCILLATOR: O-H BOND
%
%  The O-H stretch is quantized. The Schrodinger equation for the
%  displacement xi = r - r0 along the O-H bond:
%
%      -hbar^2/(2*mu) * d^2psi/dxi^2  +  (1/2)*k_r*xi^2 * psi  =  E * psi
%
%  Analytical solutions (Hermite-Gaussian):
%      psi_n(xi) = N_n * H_n(xi/alpha) * exp(-xi^2 / (2*alpha^2))
%      E_n  = (n + 1/2) * hbar * omega     [quantized energy levels]
%      alpha = sqrt(hbar / (mu * omega))   [position uncertainty scale]
%      N_n  = 1 / sqrt(2^n * n! * sqrt(pi) * alpha)
%
%  Key quantum result:  ZPE = hbar*omega/2 ≠ 0
%  The bond CANNOT be still, even at absolute zero (Heisenberg uncertainty).
% ==============================================================================

printf('PART E: Quantum Harmonic Oscillator (O-H bond)\n');
printf('--------------------------------------------------------------\n');

% Reduced mass and frequency for symmetric stretch
mu_OH   = m_O * m_H / (m_O + m_H);   % [amu]
om_str  = nu_calc(2) / C_WN;          % [rad/fs]  (computed symmetric stretch)
alpha_q = sqrt(hbar / (mu_OH * om_str));   % [Ang]  (char. length)

% Energy levels (in eV and cm^-1)
for n = 0:4
  E_n_eV  = (n + 0.5) * hbar * om_str * C_EV;
  E_n_cm  = (n + 0.5) * nu_calc(2);
  printf('  E_%d = %.4f eV  =  %.0f cm^-1', n, E_n_eV, E_n_cm);
  if n == 0
    printf('  [zero-point energy -- bond never rests!]');
  end
  printf('\n');
end
printf('  Characteristic length alpha = %.5f Ang\n', alpha_q);
printf('  Classical turning point (n=0): r_turn = %.5f Ang\n', alpha_q*sqrt(2));
printf('  Quantum uncertainty Δr = alpha = %.5f Ang = %.1f%% of r0\n\n', ...
       alpha_q, 100*alpha_q/r0_OH);

% QHO wavefunctions on a fine grid
xi_grid = linspace(-5*alpha_q, 5*alpha_q, 800);   % displacement from equilibrium
psi_n   = zeros(5, numel(xi_grid));                 % wavefunctions n=0..4
E_n_eV  = zeros(5, 1);
V_harm  = 0.5 * k_r * xi_grid.^2 * C_EV;           % potential [eV]

for n = 0:4
  psi_n(n+1,:) = qho_psi(n, xi_grid, alpha_q);
  E_n_eV(n+1)  = (n + 0.5) * hbar * om_str * C_EV;
end


% ==============================================================================
%  PART F  --  LCAO COVALENT BOND  (electron density along O-H axis)
%
%  The covalent O-H bond forms because the electron wavefunction is a
%  QUANTUM SUPERPOSITION of atomic orbitals:
%
%      psi_bond = c_O * phi_O_2p  +  c_H * phi_H_1s    [LCAO MO]
%      rho_bond = |psi_bond|^2                           [electron density]
%
%  The bond density rho_bond has a MAXIMUM between the two atoms.
%  This charge concentration is what holds the molecule together.
%
%  Atomic orbitals (simplified Slater-type, 1D along bond axis):
%    phi_H  : H 1s orbital centered on H nucleus
%    phi_O  : O 2p orbital centered on O nucleus, pointing toward H
% ==============================================================================

printf('PART F: LCAO Covalent Bond Electron Density\n');
printf('--------------------------------------------------------------\n');

% Bond axis: O at 0, H at r0_OH = 0.9572 Ang
x_bond = linspace(-0.8, r0_OH + 0.8, 1200);

% H 1s orbital (Slater-type, 1D):  phi_H ~ exp(-|x - r0|/a0)
a_H   = a0;                              % H effective Bohr radius
phi_H = exp(-abs(x_bond - r0_OH) / a_H);

% O 2p_x orbital (simplified Gaussian x * exp(-x^2/(2*s^2))):
Z_eff_O = 4.55;                          % effective nuclear charge for O 2p
s_O     = 2 * a0 / Z_eff_O;             % Gaussian sigma for O 2p [Ang]
phi_O   = x_bond .* exp(-x_bond.^2 / (2*s_O^2));
% Flip sign so O 2p points toward H (positive amplitude between O and H)
phi_O   = sign(r0_OH) * phi_O;

% Normalize each orbital (numerical integration)
dx      = x_bond(2) - x_bond(1);
N_H     = sqrt(sum(phi_H.^2) * dx);
N_O     = sqrt(sum(phi_O.^2) * dx);
phi_H   = phi_H / N_H;
phi_O   = phi_O / N_O;

% LCAO bonding MO  (equal mixing for display)
psi_bond     = phi_O + phi_H;
psi_antibond = phi_O - phi_H;
N_bond       = sqrt(sum(psi_bond.^2)     * dx);
N_anti       = sqrt(sum(psi_antibond.^2) * dx);
psi_bond     = psi_bond     / N_bond;
psi_antibond = psi_antibond / N_anti;

% Electron densities
rho_H     = phi_H.^2;
rho_O     = phi_O.^2;
rho_bond  = psi_bond.^2;
rho_anti  = psi_antibond.^2;
rho_atoms = rho_H + rho_O;     % non-interacting sum (no bond)

% Bond enhancement: ratio of bond density to atomic sum, between atoms
mid = (x_bond > 0.05) & (x_bond < r0_OH - 0.05);
bond_enhance = sum(rho_bond(mid)) / max(sum(rho_atoms(mid)), 1e-10);
printf('  H 1s orbital size:   a_H = %.4f Ang\n', a_H);
printf('  O 2p orbital sigma:  s_O = %.4f Ang  (Z_eff=%.2f)\n', s_O, Z_eff_O);
printf('  Bond enhancement factor between atoms: %.2fx\n', bond_enhance);
printf('  (Charge density between O and H is %.2fx greater when bonded)\n\n', bond_enhance);


% ==============================================================================
%  FIGURE 1  --  MOLECULAR GEOMETRY
% ==============================================================================

printf('Plotting figures...\n');

figA = figure(1);
set(figA, 'visible', 'off', 'color', [0.05 0.05 0.12], 'position', [50 50 900 700]);

ax = axes('color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
          'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
          'gridalpha', 0.45, 'fontsize', 10);
hold(ax, 'on');

% Bond lines
plot(ax, [x_O x_H1], [y_O y_H1], '-', 'color', [0.70 0.70 0.70], 'linewidth', 3.0);
plot(ax, [x_O x_H2], [y_O y_H2], '-', 'color', [0.70 0.70 0.70], 'linewidth', 3.0);

% Electron density shading (covalent bond = charge between atoms)
bond_shade = linspace(0, 1, 50);
for ib = 1:49
  f1 = bond_shade(ib); f2 = bond_shade(ib+1);
  xb1=[x_O*f1+x_H1*(1-f1), x_O*f2+x_H1*(1-f2)];
  yb1=[y_O*f1+y_H1*(1-f1), y_O*f2+y_H1*(1-f2)];
  xb2=[x_O*f1+x_H2*(1-f1), x_O*f2+x_H2*(1-f2)];
  yb2=[y_O*f1+y_H2*(1-f1), y_O*f2+y_H2*(1-f2)];
  % color fades from O-blue to H-cyan along bond
  bcol = [0.15+0.50*(1-f1), 0.35+0.40*(1-f1), 0.85];
  plot(ax, xb1, yb1, '-', 'color', bcol, 'linewidth', 8);
  plot(ax, xb2, yb2, '-', 'color', bcol, 'linewidth', 8);
end
% Redraw bond lines on top
plot(ax, [x_O x_H1], [y_O y_H1], '-', 'color', [0.65 0.65 0.70], 'linewidth', 1.5);
plot(ax, [x_O x_H2], [y_O y_H2], '-', 'color', [0.65 0.65 0.70], 'linewidth', 1.5);

% Oxygen atom (large, red-ish)
t_circ = linspace(0, 2*pi, 80);
R_O = 0.18;   % display radius [Ang]
fill(ax, x_O + R_O*cos(t_circ), y_O + R_O*sin(t_circ), [0.90 0.30 0.25], ...
     'edgecolor', [0.95 0.65 0.60], 'linewidth', 1.5);

% Hydrogen atoms (small, cyan)
R_H = 0.09;
fill(ax, x_H1 + R_H*cos(t_circ), y_H1 + R_H*sin(t_circ), [0.35 0.70 0.98], ...
     'edgecolor', [0.70 0.90 1.00], 'linewidth', 1.2);
fill(ax, x_H2 + R_H*cos(t_circ), y_H2 + R_H*sin(t_circ), [0.35 0.70 0.98], ...
     'edgecolor', [0.70 0.90 1.00], 'linewidth', 1.2);

% Lone pair electrons (conceptual -- 2 pairs on O)
lp_ang  = [145, 35] * pi/180;   % above O
for lp = lp_ang
  lp_x = x_O + 0.26*cos(lp);
  lp_y = y_O + 0.26*sin(lp);
  plot(ax, lp_x, lp_y, '.', 'color', [0.95 0.90 0.30], 'markersize', 10);
  plot(ax, lp_x + 0.06, lp_y, '.', 'color', [0.95 0.90 0.30], 'markersize', 10);
end

% Bond length annotations
mid1 = [(x_O+x_H1)/2 - 0.15, (y_O+y_H1)/2];
mid2 = [(x_O+x_H2)/2 + 0.15, (y_O+y_H2)/2];
text(ax, mid1(1), mid1(2), sprintf('%.4f A', r0_OH), ...
     'color', [0.85 0.85 0.85], 'fontsize', 9, 'interpreter', 'none');
text(ax, mid2(1), mid2(2), sprintf('%.4f A', r0_OH), ...
     'color', [0.85 0.85 0.85], 'fontsize', 9, 'interpreter', 'none');

% Bond angle arc
ang_start = atan2(y_H1-y_O, x_H1-x_O);
ang_end   = atan2(y_H2-y_O, x_H2-x_O);
r_arc     = 0.35;
t_arc     = linspace(ang_start, ang_end, 50);
plot(ax, x_O + r_arc*cos(t_arc), y_O + r_arc*sin(t_arc), '-', ...
     'color', [0.85 0.75 0.25], 'linewidth', 1.8);
text(ax, x_O - 0.05, y_O - r_arc - 0.10, sprintf('%.1f deg', theta0*180/pi), ...
     'color', [0.90 0.80 0.35], 'fontsize', 10, 'fontweight', 'bold', ...
     'horizontalalignment', 'center', 'interpreter', 'none');

% Dipole moment arrow (O is delta-, HH side is delta+)
% Dipole points from positive to negative: from HH midpoint toward O
dp_scale = 0.4;
plot(ax, [0, 0], [0.22, 0.22+dp_scale], '->', ...
     'color', [0.45 0.95 0.55], 'linewidth', 2.5, 'markersize', 10);
text(ax, 0.12, 0.22+dp_scale*0.5, 'μ = 1.85 D', ...
     'color', [0.55 0.95 0.65], 'fontsize', 9, 'interpreter', 'none');

% Atom labels
text(ax, x_O + 0.24, y_O, 'O', 'color', [1.00 0.55 0.50], ...
     'fontsize', 14, 'fontweight', 'bold');
text(ax, x_H1 - 0.24, y_H1 + 0.10, 'H', 'color', [0.60 0.85 1.00], ...
     'fontsize', 14, 'fontweight', 'bold');
text(ax, x_H2 + 0.10, y_H2 + 0.10, 'H', 'color', [0.60 0.85 1.00], ...
     'fontsize', 14, 'fontweight', 'bold');

% Lone pair label
text(ax, -0.45, 0.38, 'lone', 'color', [0.95 0.90 0.30], 'fontsize', 8);
text(ax, -0.45, 0.25, 'pairs', 'color', [0.95 0.90 0.30], 'fontsize', 8);

% Gradient shading legend
text(ax, -1.20, -0.82, 'bond shading = shared electron density (covalent bond)', ...
     'color', [0.65 0.65 0.80], 'fontsize', 8, 'interpreter', 'none');

hold(ax, 'off');
grid(ax, 'on');
axis(ax, 'equal');
xlim(ax, [-1.35 1.35]); ylim(ax, [-1.0 1.0]);
title(ax, 'H_2O Molecular Geometry  --  Covalent Three-Body System', ...
      'color', [0.95 0.95 0.95], 'fontsize', 13, 'fontweight', 'bold');
xlabel(ax, 'x  (Angstrom)', 'color', [0.80 0.80 0.80], 'fontsize', 11);
ylabel(ax, 'y  (Angstrom)', 'color', [0.80 0.80 0.80], 'fontsize', 11);

print(figA, 'h2o_geometry.png', '-dpng', '-r150');
printf('  Output: h2o_geometry.png\n');


% ==============================================================================
%  FIGURE 2  --  NORMAL MODE DISPLACEMENT PATTERNS
% ==============================================================================

figB = figure(2);
set(figB, 'visible', 'off', 'color', [0.05 0.05 0.12], 'position', [50 50 1100 500]);

mode_cols = {[0.85 0.45 0.95], [0.35 0.70 1.00], [1.00 0.55 0.20]};   % violet, blue, orange

for k = 1:3
  subplot(1, 3, k);
  set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
           'ycolor', [0.75 0.75 0.75], 'fontsize', 9);
  hold on;

  % Draw equilibrium geometry
  plot([x_O x_H1], [y_O y_H1], '-', 'color', [0.50 0.50 0.60], 'linewidth', 2.0);
  plot([x_O x_H2], [y_O y_H2], '-', 'color', [0.50 0.50 0.60], 'linewidth', 2.0);
  plot(x_O, y_O, 'o', 'markersize', 14, ...
       'markerfacecolor', [0.90 0.30 0.25], 'markeredgecolor', 'w', 'linewidth', 1.2);
  plot(x_H1, y_H1, 'o', 'markersize', 8, ...
       'markerfacecolor', [0.35 0.70 0.98], 'markeredgecolor', 'w', 'linewidth', 1.0);
  plot(x_H2, y_H2, 'o', 'markersize', 8, ...
       'markerfacecolor', [0.35 0.70 0.98], 'markeredgecolor', 'w', 'linewidth', 1.0);

  % Displacement arrows (scaled by 0.35 Ang for visibility)
  arr_scale = 0.35;
  mcol = mode_cols{k};

  % Oxygen arrow
  quiver(x_O, y_O, arr_scale*displ(1,k), arr_scale*displ(2,k), 0, ...
         'color', mcol, 'linewidth', 2.0, 'maxheadsize', 0.5);
  % H1 arrow
  quiver(x_H1, y_H1, arr_scale*displ(3,k), arr_scale*displ(4,k), 0, ...
         'color', mcol, 'linewidth', 2.0, 'maxheadsize', 0.5);
  % H2 arrow
  quiver(x_H2, y_H2, arr_scale*displ(5,k), arr_scale*displ(6,k), 0, ...
         'color', mcol, 'linewidth', 2.0, 'maxheadsize', 0.5);

  hold off;
  axis equal; grid on;
  xlim([-1.6 1.6]); ylim([-1.4 0.9]);
  title(sprintf('Mode %d:  %s\n%.0f cm^{-1}  (exp: %d)', ...
                k, mode_names{k}, nu_calc(k), nu_exp(k)), ...
        'color', mcol, 'fontsize', 10, 'fontweight', 'bold');
  xlabel('x  (A)', 'color', [0.75 0.75 0.75], 'fontsize', 9, 'interpreter', 'none');
  if k == 1; ylabel('y  (A)', 'color', [0.75 0.75 0.75], 'fontsize', 9, 'interpreter', 'none'); end
end

print(figB, 'h2o_modes.png', '-dpng', '-r150');
printf('  Output: h2o_modes.png\n');


% ==============================================================================
%  FIGURE 3  --  MOLECULAR DYNAMICS & FFT SPECTRUM
% ==============================================================================

figC = figure(3);
set(figC, 'visible', 'off', 'color', [0.05 0.05 0.12], 'position', [50 50 1100 700]);

% Panel 1: Bond lengths -- symmetric stretch IC
subplot(2, 2, 1);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.50, 'fontsize', 9);
hold on;
plot(t_uni, (rOH1_s - r0_OH)*1000, '-', 'color', [0.35 0.70 1.00], 'linewidth', 1.6);
plot(t_uni, (rOH2_s - r0_OH)*1000, '--', 'color', [1.00 0.55 0.20], 'linewidth', 1.4);
hold off; grid on;
title('MD: Symmetric Stretch IC', 'color', [0.92 0.92 0.92], 'fontsize', 10, 'fontweight', 'bold');
xlabel('time (fs)', 'color', [0.75 0.75 0.75]);
ylabel('\Delta r_{OH}  (mA)', 'color', [0.75 0.75 0.75], 'interpreter', 'none');
lgc1 = legend({'r_{OH1} - r_0', 'r_{OH2} - r_0'}, 'location', 'northeast', 'fontsize', 8);
set(lgc1, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

% Panel 2: Bond angle -- bending IC
subplot(2, 2, 2);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.50, 'fontsize', 9);
hold on;
plot(t_uni, (theta_b - theta0)*180/pi, '-', 'color', [0.85 0.45 0.95], 'linewidth', 1.8);
hold off; grid on;
title('MD: Bending IC', 'color', [0.92 0.92 0.92], 'fontsize', 10, 'fontweight', 'bold');
xlabel('time (fs)', 'color', [0.75 0.75 0.75]);
ylabel('\Delta\theta  (degrees)', 'color', [0.75 0.75 0.75], 'interpreter', 'none');
lgc2 = legend({'theta - theta_0'}, 'location', 'northeast', 'fontsize', 8);
set(lgc2, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);
text(2, max((theta_b-theta0)*180/pi)*0.85, ...
     sprintf('T_{bend} ~ %.1f fs', 1/(nu_calc(1)/C_WN)/(2*pi)*2*pi), ...
     'color', [0.85 0.65 0.35], 'fontsize', 8, 'interpreter', 'none');

% Panel 3: FFT spectrum (combined IC)
subplot(2, 2, [3 4]);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.50, 'fontsize', 10);
hold on;

% Plot FFT spectrum
plot_mask = nu_fft < 5000;
plot(nu_fft(plot_mask), fft_amp(plot_mask), '-', ...
     'color', [0.40 0.85 0.55], 'linewidth', 1.6);

% Mark experimental frequencies
for k = 1:3
  plot([nu_exp(k) nu_exp(k)], [0, max(fft_amp(plot_mask))*1.10], ':', ...
       'color', [0.90 0.75 0.20], 'linewidth', 1.5);
  text(nu_exp(k) + 30, max(fft_amp(plot_mask))*1.05, ...
       sprintf('  nu_%d exp\n  %d cm^{-1}', k, nu_exp(k)), ...
       'color', [0.90 0.80 0.30], 'fontsize', 8, 'interpreter', 'none');
end

hold off; grid on;
title('FFT Vibrational Spectrum from Combined MD Run  (all 3 modes excited)', ...
      'color', [0.95 0.95 0.95], 'fontsize', 11, 'fontweight', 'bold');
xlabel('wavenumber (cm^{-1})', 'color', [0.80 0.80 0.80], 'fontsize', 11, 'interpreter', 'none');
ylabel('|FFT| amplitude', 'color', [0.80 0.80 0.80], 'fontsize', 11);
lgc3 = legend({'MD FFT (r_{OH1})', 'Experimental frequencies'}, ...
              'location', 'northeast', 'fontsize', 9);
set(lgc3, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

print(figC, 'h2o_dynamics.png', '-dpng', '-r150');
printf('  Output: h2o_dynamics.png\n');


% ==============================================================================
%  FIGURE 4  --  QUANTUM HO WAVEFUNCTIONS  +  LCAO BONDING
% ==============================================================================

figD = figure(4);
set(figD, 'visible', 'off', 'color', [0.05 0.05 0.12], 'position', [50 50 1100 750]);

psi_colors = {[0.35 0.70 1.00], [0.90 0.40 0.20], [0.30 0.92 0.48], ...
              [0.90 0.75 0.20], [0.80 0.40 0.90]};

% Panel A: QHO potential + energy levels
subplot(2, 3, 1);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.45, 'fontsize', 9);
hold on;
V_plot = min(V_harm, E_n_eV(5) * 1.3);
plot(xi_grid * 1000 + r0_OH*1000, V_harm, '-', 'color', [0.70 0.70 0.70], 'linewidth', 2.0);
% Energy levels as horizontal lines
for n = 0:4
  xi_turn = sqrt(2*E_n_eV(n+1)/k_r/C_EV) * 1000;  % mAng
  r_c = r0_OH * 1000;   % center in mAng
  plot([r_c-xi_turn r_c+xi_turn], [E_n_eV(n+1) E_n_eV(n+1)], '-', ...
       'color', psi_colors{n+1}, 'linewidth', 1.5);
  text(r_c + xi_turn + 5, E_n_eV(n+1), sprintf('n=%d', n), ...
       'color', psi_colors{n+1}, 'fontsize', 8);
end
hold off; grid on;
xlim([r0_OH*1000 - 300, r0_OH*1000 + 300]);
ylim([-0.05, E_n_eV(5)*1.25]);
title('QHO: Potential + Energy Levels', 'color', [0.92 0.92 0.92], ...
      'fontsize', 10, 'fontweight', 'bold');
xlabel('r_{OH}  (mA)', 'color', [0.75 0.75 0.75], 'interpreter', 'none');
ylabel('Energy (eV)', 'color', [0.75 0.75 0.75]);
text(r0_OH*1000 - 280, E_n_eV(1)*0.45, ...
     sprintf('ZPE = %.3f eV', E_n_eV(1)), ...
     'color', psi_colors{1}, 'fontsize', 8, 'interpreter', 'none');

% Panel B: Wavefunctions psi_n
subplot(2, 3, 2);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.45, 'fontsize', 9);
hold on;
offset = 0.45;  % vertical offset between wavefunctions [eV scale]
for n = 0:4
  psi_scaled = psi_n(n+1,:) * 0.20;   % scale for display
  plot(xi_grid*1000 + r0_OH*1000, psi_scaled + E_n_eV(n+1), '-', ...
       'color', psi_colors{n+1}, 'linewidth', 1.6);
  % Zero-line for each level
  plot([xi_grid(1)*1000+r0_OH*1000, xi_grid(end)*1000+r0_OH*1000], ...
       [E_n_eV(n+1) E_n_eV(n+1)], ':', 'color', psi_colors{n+1}*0.6, 'linewidth', 0.8);
end
% Potential outline
plot(xi_grid*1000 + r0_OH*1000, min(V_harm, E_n_eV(5)*1.3), '-', ...
     'color', [0.60 0.60 0.65], 'linewidth', 1.5);
hold off; grid on;
xlim([r0_OH*1000 - 300, r0_OH*1000 + 300]);
ylim([-0.05, E_n_eV(5)*1.25]);
title('Wavefunctions psi_n(r)', 'color', [0.92 0.92 0.92], ...
      'fontsize', 10, 'fontweight', 'bold');
xlabel('r_{OH}  (mA)', 'color', [0.75 0.75 0.75], 'interpreter', 'none');
ylabel('psi_n  +  E_n  (eV)', 'color', [0.75 0.75 0.75], 'interpreter', 'none');

% Panel C: Probability densities |psi_n|^2
subplot(2, 3, 3);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.45, 'fontsize', 9);
hold on;
for n = 0:4
  rho_n = psi_n(n+1,:).^2;
  plot(xi_grid*1000 + r0_OH*1000, rho_n + E_n_eV(n+1), '-', ...
       'color', psi_colors{n+1}, 'linewidth', 1.6);
  plot([xi_grid(1)*1000+r0_OH*1000, xi_grid(end)*1000+r0_OH*1000], ...
       [E_n_eV(n+1) E_n_eV(n+1)], ':', 'color', psi_colors{n+1}*0.6, 'linewidth', 0.8);
end
plot(xi_grid*1000+r0_OH*1000, min(V_harm,E_n_eV(5)*1.3), '-', ...
     'color', [0.60 0.60 0.65], 'linewidth', 1.5);
hold off; grid on;
xlim([r0_OH*1000-300, r0_OH*1000+300]);
ylim([-0.05, E_n_eV(5)*1.25]);
title('Probability Densities |psi_n|^2', 'color', [0.92 0.92 0.92], ...
      'fontsize', 10, 'fontweight', 'bold');
xlabel('r_{OH}  (mA)', 'color', [0.75 0.75 0.75], 'interpreter', 'none');
ylabel('|psi_n|^2 + E_n', 'color', [0.75 0.75 0.75], 'interpreter', 'none');

% Panel D: LCAO -- atomic orbitals separately
subplot(2, 3, 4);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.45, 'fontsize', 9);
hold on;
plot(x_bond, rho_H, '-', 'color', [0.35 0.70 1.00], 'linewidth', 1.8);
plot(x_bond, rho_O, '-', 'color', [0.90 0.30 0.25], 'linewidth', 1.8);
% Vertical lines for nuclei
ax_y = ylim();
plot([0 0], [0 max([rho_H rho_O])*1.1], ':', 'color', [0.90 0.30 0.25], 'linewidth', 1.2);
plot([r0_OH r0_OH], [0 max([rho_H rho_O])*1.1], ':', 'color', [0.35 0.70 1.00], 'linewidth', 1.2);
text(0.03, max(rho_O)*0.95, 'O', 'color', [0.90 0.30 0.25], 'fontsize', 11, 'fontweight', 'bold');
text(r0_OH+0.03, max(rho_H)*0.95, 'H', 'color', [0.35 0.70 1.00], 'fontsize', 11, 'fontweight', 'bold');
hold off; grid on;
title('Isolated Atomic Orbitals', 'color', [0.92 0.92 0.92], ...
      'fontsize', 10, 'fontweight', 'bold');
xlabel('x along bond  (A)', 'color', [0.75 0.75 0.75], 'interpreter', 'none');
ylabel('electron density', 'color', [0.75 0.75 0.75]);
lge1 = legend({'O 2p orbital', 'H 1s orbital'}, 'location', 'northeast', 'fontsize', 8);
set(lge1, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

% Panel E: LCAO bonding vs non-bonding density
subplot(2, 3, 5);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.45, 'fontsize', 9);
hold on;
plot(x_bond, rho_atoms,    '--', 'color', [0.65 0.65 0.65], 'linewidth', 1.4);
plot(x_bond, rho_bond,     '-',  'color', [0.30 0.92 0.48], 'linewidth', 2.2);
plot(x_bond, rho_anti,     '-',  'color', [1.00 0.45 0.18], 'linewidth', 1.6);
% Shade the bond region
xlim_bond = [0.05, r0_OH-0.05];
x_shade = x_bond(x_bond>=xlim_bond(1) & x_bond<=xlim_bond(2));
rho_b_s = rho_bond(x_bond>=xlim_bond(1) & x_bond<=xlim_bond(2));
rho_a_s = rho_atoms(x_bond>=xlim_bond(1) & x_bond<=xlim_bond(2));
fill([x_shade, fliplr(x_shade)], [rho_b_s, fliplr(rho_a_s)], ...
     [0.20 0.60 0.30], 'facealpha', 0.30, 'edgecolor', 'none');
plot([0 0], [0 max(rho_bond)*1.1], ':', 'color', [0.90 0.30 0.25], 'linewidth', 1.2);
plot([r0_OH r0_OH], [0 max(rho_bond)*1.1], ':', 'color', [0.35 0.70 1.00], 'linewidth', 1.2);
text(r0_OH/2, max(rho_bond)*0.65, sprintf('bond\n%.1fx', bond_enhance), ...
     'color', [0.45 0.95 0.60], 'fontsize', 8, 'horizontalalignment', 'center', ...
     'interpreter', 'none');
hold off; grid on;
title('LCAO Bonding Electron Density', 'color', [0.92 0.92 0.92], ...
      'fontsize', 10, 'fontweight', 'bold');
xlabel('x along bond  (A)', 'color', [0.75 0.75 0.75], 'interpreter', 'none');
ylabel('electron density', 'color', [0.75 0.75 0.75]);
lge2 = legend({'atomic sum (no bond)', 'bonding MO: |psi_bond|^2', ...
               'antibonding MO: |psi_anti|^2'}, ...
              'location', 'northeast', 'fontsize', 7);
set(lge2, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

% Panel F: Summary comparison table (text in axes)
subplot(2, 3, 6);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', 'none', 'ycolor', 'none', ...
         'xtick', [], 'ytick', [], 'fontsize', 8);
hold on;
% Background box
fill([0 1 1 0 0], [0 0 1 1 0], [0.08 0.08 0.18], 'edgecolor', [0.35 0.35 0.50]);

% Table content
rows = { ...
  'Parameter',           'Value',          'Significance'; ...
  '',                    '',               ''; ...
  'r_{OH}',              '0.9572 A',       'covalent bond'; ...
  'theta_{HOH}',         '104.52 deg',     'lone pair effect'; ...
  'dipole mu',           '1.85 D',         'polar solvent'; ...
  'nu_1 bend',           '1595 cm^{-1}',   '20.9 fs period'; ...
  'nu_2 sym str',        '3657 cm^{-1}',   '9.1 fs period'; ...
  'nu_3 asym str',       '3756 cm^{-1}',   '8.9 fs period'; ...
  'ZPE (str)',           '0.23 eV',        'quantum jitter'; ...
  'Delta r (n=0)',       '0.069 A',        '7.2% of r_0'; ...
  'Bond enhance',        sprintf('%.1fx', bond_enhance), 'covalent glue'; ...
};

ncols = 3; nrows = size(rows,1);
dy = 0.085;
y0_t = 0.95;
col_x = [0.02, 0.42, 0.68];
col_colors = {[0.85 0.85 0.85], [0.40 0.85 0.55], [0.65 0.75 0.95]};

for r = 1:nrows
  y_pos = y0_t - (r-1)*dy;
  if r == 1
    fc = [0.95 0.90 0.35];  % header color
  elseif r == 2
    continue;
  else
    fc = col_colors{1};
  end
  for c = 1:3
    if r > 1; fc = col_colors{c}; end
    text(col_x(c), y_pos, rows{r,c}, 'color', fc, 'fontsize', 7.5, ...
         'interpreter', 'none', 'units', 'normalized');
  end
end

hold off;
title('Summary: H2O Quantum Parameters', 'color', [0.92 0.92 0.92], ...
      'fontsize', 10, 'fontweight', 'bold');
axis([0 1 0 1]);

print(figD, 'h2o_quantum.png', '-dpng', '-r150');
printf('  Output: h2o_quantum.png\n\n');


% ==============================================================================
%  FINAL SUMMARY
% ==============================================================================

printf('==============================================================\n');
printf('  H2O Molecular Simulation Summary\n');
printf('==============================================================\n\n');
printf('  MOLECULAR GEOMETRY (experimental):\n');
printf('    r_OH   = %.4f A  (bond length)\n', r0_OH);
printf('    theta  = %.2f deg (bond angle -- bent, not linear)\n', theta0*180/pi);
printf('    dipole = 1.85 D  (bent geometry -> polar molecule)\n\n');
printf('  FORCE-FIELD NORMAL MODES:\n');
printf('    Mode 1 (bending):     computed %4.0f  cm^-1  | exp 1595 cm^-1\n', nu_calc(1));
printf('    Mode 2 (sym. str.):   computed %4.0f  cm^-1  | exp 3657 cm^-1\n', nu_calc(2));
printf('    Mode 3 (asym. str.):  computed %4.0f  cm^-1  | exp 3756 cm^-1\n', nu_calc(3));
printf('\n');
printf('  QUANTUM O-H BOND:\n');
printf('    Reduced mass mu_OH = %.5f amu\n', mu_OH);
printf('    omega = %.6f rad/fs  (%4.0f cm^-1)\n', om_str, nu_calc(2));
printf('    alpha = %.5f A  (quantum pos. uncertainty)\n', alpha_q);
printf('    ZPE   = %.4f eV  = %.0f cm^-1\n', E_n_eV(1), E_n_eV(1)*8065.6);
printf('    => The bond vibrates with amplitude ~%.0f mA at T=0!\n\n', alpha_q*1000);
printf('  LCAO COVALENT BOND:\n');
printf('    Bond electron density between O and H is %.1fx\n', bond_enhance);
printf('    the non-interacting sum of atomic densities.\n');
printf('    This charge accumulation IS the covalent bond:\n');
printf('    psi_bond = c_O * phi_O(2p) + c_H * phi_H(1s)\n\n');
printf('  THREE-BODY ANALOGY (gravity vs. H2O):\n');
printf('    Both solved by ode45 with 12 coupled first-order ODEs.\n');
printf('    Gravitational: F ~ 1/r^2  (long range, no equilibrium)\n');
printf('    Molecular:     F ~ (r-r0) (harmonic spring, equilibrium at r0)\n');
printf('    Gravity: deterministic chaos (Poincare 1887)\n');
printf('    H2O bond: quantum uncertainty (Heisenberg 1927)\n\n');
printf('  Output files:\n');
printf('    h2o_geometry.png\n');
printf('    h2o_modes.png\n');
printf('    h2o_dynamics.png\n');
printf('    h2o_quantum.png\n');
printf('\n');
printf('==============================================================\n');
printf('  Simulation complete.\n');
printf('==============================================================\n\n');


% ==============================================================================
%  SUBFUNCTIONS  (must appear after the main script body in GNU Octave)
% ==============================================================================

% ------------------------------------------------------------------------------
%  compute_forces  --  Force on each atom from harmonic bond + angle potentials
%
%  V = (1/2)*k_r*(r_OH1 - r0)^2 + (1/2)*k_r*(r_OH2 - r0)^2
%      + (1/2)*k_t*(theta - theta0)^2
%
%  Inputs:
%    q       -- position state [x_O; y_O; x_H1; y_H1; x_H2; y_H2]
%    k_r     -- bond stretch force constant [amu/fs^2]
%    k_t     -- angle bend force constant   [amu*Ang^2/fs^2/rad^2]
%    r0      -- equilibrium bond length [Ang]
%    t0      -- equilibrium bond angle  [rad]
%
%  Output:
%    F       -- force vector [F_xO; F_yO; F_xH1; F_yH1; F_xH2; F_yH2]
% ------------------------------------------------------------------------------
function F = compute_forces(q, k_r, k_t, r0, t0)
  rO  = q(1:2);   rH1 = q(3:4);   rH2 = q(5:6);

  d1 = rH1 - rO;   d2 = rH2 - rO;
  r1 = sqrt(d1'*d1);   r2 = sqrt(d2'*d2);
  u1 = d1 / r1;        u2 = d2 / r2;

  % Bond stretch forces: F = -k_r*(r - r0) * unit_vector
  fs_H1 = -k_r*(r1 - r0) * u1;
  fs_H2 = -k_r*(r2 - r0) * u2;
  fs_O  =  k_r*(r1 - r0) * u1 + k_r*(r2 - r0) * u2;

  % Angle bending forces
  ct    = max(-0.9999, min(0.9999, dot(u1, u2)));
  theta = acos(ct);
  st    = sin(theta);

  if st < 1e-10
    fb_H1 = [0;0];   fb_H2 = [0;0];   fb_O = [0;0];
  else
    fb_H1 =  k_t*(theta - t0) * (u2 - ct*u1) / (r1*st);
    fb_H2 =  k_t*(theta - t0) * (u1 - ct*u2) / (r2*st);
    fb_O  = -(fb_H1 + fb_H2);
  end

  F = [fs_O+fb_O; fs_H1+fb_H1; fs_H2+fb_H2];
endfunction


% ------------------------------------------------------------------------------
%  h2o_ode  --  ODE right-hand side for molecular dynamics (same structure
%               as the gravitational three_body_ode!)
%
%  State: y = [x_O, Y_O, x_H1, Y_H1, x_H2, Y_H2,
%              vx_O, vY_O, vx_H1, vY_H1, vx_H2, vY_H2]
% ------------------------------------------------------------------------------
function dydt = h2o_ode(t, y, k_r, k_t, m_H, m_O, r0, t0)
  q = y(1:6);   % positions
  v = y(7:12);  % velocities

  F = compute_forces(q, k_r, k_t, r0, t0);

  % Accelerations = F / mass  (mass vector: [m_O m_O m_H m_H m_H m_H])
  a = [F(1)/m_O; F(2)/m_O; F(3)/m_H; F(4)/m_H; F(5)/m_H; F(6)/m_H];

  dydt = [v; a];
endfunction


% ------------------------------------------------------------------------------
%  h2o_energy  --  Total energy  E = KE + V_stretch + V_bend
% ------------------------------------------------------------------------------
function E = h2o_energy(y, m_H, m_O, k_r, k_t, r0, t0)
  q = y(1:6); v = y(7:12);

  % Kinetic energy
  KE = 0.5*m_O*(v(1)^2+v(2)^2) + 0.5*m_H*(v(3)^2+v(4)^2) + 0.5*m_H*(v(5)^2+v(6)^2);

  % Potential energy
  rO=q(1:2); rH1=q(3:4); rH2=q(5:6);
  d1=rH1-rO; d2=rH2-rO;
  r1=sqrt(d1'*d1); r2=sqrt(d2'*d2);
  u1=d1/r1; u2=d2/r2;
  ct=max(-0.9999,min(0.9999,dot(u1,u2)));
  theta=acos(ct);
  V = 0.5*k_r*(r1-r0)^2 + 0.5*k_r*(r2-r0)^2 + 0.5*k_t*(theta-t0)^2;

  E = KE + V;
endfunction


% ------------------------------------------------------------------------------
%  bond_observables  --  Extract r_OH1, r_OH2, theta from trajectory matrix
% ------------------------------------------------------------------------------
function [rOH1, rOH2, theta] = bond_observables(Y)
  n = size(Y, 1);
  rOH1  = zeros(n,1);
  rOH2  = zeros(n,1);
  theta = zeros(n,1);

  for k = 1:n
    xO=Y(k,1); yO=Y(k,2); xH1=Y(k,3); yH1=Y(k,4); xH2=Y(k,5); yH2=Y(k,6);
    d1 = [xH1-xO; yH1-yO];
    d2 = [xH2-xO; yH2-yO];
    r1 = sqrt(d1'*d1); r2 = sqrt(d2'*d2);
    rOH1(k) = r1; rOH2(k) = r2;
    ct = max(-0.9999, min(0.9999, dot(d1,d2)/(r1*r2)));
    theta(k) = acos(ct);
  end
endfunction


% ------------------------------------------------------------------------------
%  qho_psi  --  Quantum harmonic oscillator wavefunction (1D)
%
%  psi_n(xi) = N_n * H_n(xi/alpha) * exp(-xi^2 / (2*alpha^2))
%  N_n = 1 / sqrt(2^n * n! * sqrt(pi) * alpha)
%
%  Uses physicist's Hermite polynomials H_n via 3-term recurrence.
% ------------------------------------------------------------------------------
function psi = qho_psi(n, xi, alpha)
  x   = xi / alpha;          % dimensionless coordinate
  Hn  = hermite_poly(n, x);  % H_n(x)
  Nn  = 1 / sqrt(2^n * factorial(n) * sqrt(pi) * alpha);
  psi = Nn * Hn .* exp(-x.^2 / 2);
endfunction


% ------------------------------------------------------------------------------
%  hermite_poly  --  Physicist's Hermite polynomial H_n(x) via recurrence
%
%  H_0(x) = 1
%  H_1(x) = 2x
%  H_n(x) = 2x*H_{n-1}(x) - 2*(n-1)*H_{n-2}(x)
% ------------------------------------------------------------------------------
function H = hermite_poly(n, x)
  if n == 0
    H = ones(size(x));
  elseif n == 1
    H = 2 * x;
  else
    H_prev2 = ones(size(x));
    H_prev1 = 2 * x;
    for k = 2:n
      H = 2*x .* H_prev1 - 2*(k-1) * H_prev2;
      H_prev2 = H_prev1;
      H_prev1 = H;
    end
  end
endfunction
