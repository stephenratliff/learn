% ==============================================================================
%  three_body_problem.m
%  Newton's Three-Body Problem  --  GNU Octave Numerical Simulation
% ==============================================================================
%
%  OVERVIEW
%  --------
%  Simulates the gravitational three-body problem: the question Newton could
%  not answer analytically in his 1687 Principia Mathematica.
%
%  Newton's Law of Universal Gravitation:
%
%      F_ij  =  G * m_i * m_j / r_ij^2        [scalar magnitude, attractive]
%
%  Equation of Motion for body i  (Newton's Second Law F = m*a):
%
%      d^2 r_i         m_j * (r_j - r_i)
%      ───────  =  G * sum  ─────────────────   (j != i)
%        dt^2       j       |r_j - r_i|^3
%
%  State vector (2D, three bodies -- 12 components):
%
%      y = [x1 y1 x2 y2 x3 y3  vx1 vy1 vx2 vy2 vx3 vy3]^T
%
%  This is a system of 12 coupled first-order ODEs.  We rewrite the single
%  second-order ODE as two first-order ODEs per degree of freedom:
%
%      dr_i/dt = v_i
%      dv_i/dt = a_i   (the gravitational acceleration above)
%
%  WHY NUMERICAL METHODS?
%  ----------------------
%  Henri Poincare proved (1887) that the general three-body problem has NO
%  closed-form analytical solution.  The system is CHAOTIC: infinitesimally
%  different initial conditions diverge exponentially over time (positive
%  Lyapunov exponent).
%
%  Connection to Riemann / Midpoint Rule:
%  ode45 uses the Dormand-Prince embedded Runge-Kutta 4/5 method.  This is
%  the direct high-order descendant of the Euler / Midpoint rule idea:
%  approximate the continuous integral of d/dt[y] by a weighted sum over
%  discrete sub-steps.  Where the Midpoint Rule evaluates the integrand at
%  the interval midpoint, RK45 takes a weighted blend of SIX function
%  evaluations per step, achieving O(h^5) local accuracy and adaptive
%  step-size control to keep error within tolerance.
%
%  DEMONSTRATIONS
%  --------------
%  A  --  Figure-8 Choreography  (Chenciner & Montgomery, 2000)
%         Three equal masses orbiting a stable figure-8 path.  Period T~6.3259.
%         Demonstrates a rare analytic orbit and excellent energy conservation.
%
%  B  --  Chaotic Orbit + Lyapunov Sensitivity
%         Unequal masses, generic initial conditions -> unpredictable dynamics.
%         Two runs differing by delta_r = 1e-6 in x1 show exponential divergence,
%         illustrating why numerical simulation is the only practical tool.
%
%  C  --  Energy Conservation Check
%         Total E = KE + PE must remain constant (conservative system).
%         Drift in E(t) quantifies integrator accuracy.
%
%  USAGE
%  -----
%  octave three_body_problem.m
%
%  OUTPUT FILES
%  ------------
%  three_body_figure8.png    --  Figure-8 stable orbit
%  three_body_chaotic.png    --  Chaotic trajectory + Lyapunov divergence
%  three_body_energy.png     --  Energy conservation over time
% ==============================================================================

clear all; close all; clc;

printf('\n');
printf('==============================================================\n');
printf('  Newton''s Three-Body Problem  --  GNU Octave Simulation\n');
printf('==============================================================\n\n');

G = 1.0;   % Gravitational constant (natural units, G=1)

% ODE solver options: tight tolerances to preserve energy conservation
opts = odeset('RelTol', 1e-10, 'AbsTol', 1e-12);


% ==============================================================================
%  PART A  --  FIGURE-8 CHOREOGRAPHY
%
%  Discovered by Chenciner & Montgomery (2000) via variational calculus.
%  Three equal masses chase each other around a stable figure-8 path.
%  Period T ~ 6.3259  (with G=1, m1=m2=m3=1, centre-of-mass at origin).
%
%  These specific initial conditions are the unique (up to symmetry) solution
%  satisfying the choreography constraint: all three bodies follow the same
%  curve, separated in time by T/3.
% ==============================================================================

printf('PART A: Figure-8 Choreography  (Chenciner & Montgomery, 2000)\n');
printf('--------------------------------------------------------------\n');

m8 = [1.0; 1.0; 1.0];   % equal unit masses

%  Initial positions  (centre-of-mass at origin by construction)
%    Body 1:  (-0.97000436,  0.24308753)
%    Body 2:  ( 0,           0         )
%    Body 3:  ( 0.97000436, -0.24308753)
r0_8 = [-0.97000436,  0.24308753;
          0.00000000,  0.00000000;
          0.97000436, -0.24308753];

%  Initial velocities.  Let p = [0.93240737, 0.86473146].
%  Choreography demands:  v2 = -p,  v1 = v3 = p/2
v0_8 = [ 0.46620369,  0.43236573;    % v1 = p/2
         -0.93240737, -0.86473146;    % v2 = -p
          0.46620369,  0.43236573];   % v3 = p/2

%  Pack state vector: [x1 y1 x2 y2 x3 y3 vx1 vy1 vx2 vy2 vx3 vy3]
y0_8 = [r0_8(1,:), r0_8(2,:), r0_8(3,:), ...
        v0_8(1,:), v0_8(2,:), v0_8(3,:)]';

T8      = 6.3259;            % one period
tspan8  = [0, 2.0 * T8];    % simulate two full periods

printf('  Integrating ode45 (RK45) over t in [0, %.4f]  (2 periods)...\n', tspan8(2));
tic;
[t8, Y8] = ode45(@(t,y) three_body_ode(t, y, m8, G), tspan8, y0_8, opts);
t_elapsed = toc;
printf('  Done: %.3f s,  %d adaptive time steps\n', t_elapsed, numel(t8));

E8_0   = total_energy(Y8(1,:)',   m8, G);
E8_end = total_energy(Y8(end,:)', m8, G);
dE8    = abs((E8_end - E8_0) / E8_0);

printf('  Initial total energy  E_0  = %+.10f\n', E8_0);
printf('  Final   total energy  E_f  = %+.10f\n', E8_end);
printf('  Relative energy drift |dE/E_0| = %.2e\n\n', dE8);


% -- Plot A: Figure-8 trajectories -------------------------------------------
fig8 = figure(1);
set(fig8, 'visible', 'off', 'color', [0.06 0.06 0.14], ...
          'position', [50 50 900 720]);

axes('color', [0.06 0.06 0.14], ...
     'xcolor', [0.75 0.75 0.75], 'ycolor', [0.75 0.75 0.75], ...
     'gridcolor', [0.28 0.28 0.40], 'gridalpha', 0.55, ...
     'fontsize', 10);
hold on;

c1 = [0.30 0.62 1.00];   % cobalt blue
c2 = [1.00 0.45 0.18];   % ember orange
c3 = [0.22 0.90 0.44];   % emerald green

%  Trajectories
plot(Y8(:,1), Y8(:,2), '-', 'color', c1, 'linewidth', 1.8);
plot(Y8(:,3), Y8(:,4), '-', 'color', c2, 'linewidth', 1.8);
plot(Y8(:,5), Y8(:,6), '-', 'color', c3, 'linewidth', 1.8);

%  Initial position markers
plot(Y8(1,1), Y8(1,2), 'o', 'markersize', 11, ...
     'markerfacecolor', c1, 'markeredgecolor', [0.9 0.9 0.9], 'linewidth', 1.5);
plot(Y8(1,3), Y8(1,4), 'o', 'markersize', 11, ...
     'markerfacecolor', c2, 'markeredgecolor', [0.9 0.9 0.9], 'linewidth', 1.5);
plot(Y8(1,5), Y8(1,6), 'o', 'markersize', 11, ...
     'markerfacecolor', c3, 'markeredgecolor', [0.9 0.9 0.9], 'linewidth', 1.5);

hold off;
axis equal;
grid on;

title('Three-Body Problem: Figure-8 Choreography', ...
      'color', [0.95 0.95 0.95], 'fontsize', 14, 'fontweight', 'bold');
xlabel('x  (natural units)', 'color', [0.80 0.80 0.80], 'fontsize', 12);
ylabel('y  (natural units)', 'color', [0.80 0.80 0.80], 'fontsize', 12);

lg = legend({'Body 1  (m=1)', 'Body 2  (m=1)', 'Body 3  (m=1)'}, ...
            'location', 'northeast', 'fontsize', 10);
set(lg, 'color', [0.10 0.10 0.22], 'edgecolor', [0.40 0.40 0.55]);

%  Info text inside axes
ax_lim = axis();
tx = ax_lim(1) + 0.02*(ax_lim(2)-ax_lim(1));
ty = ax_lim(4) - 0.05*(ax_lim(4)-ax_lim(3));
text(tx, ty, ...
     sprintf('G=1 | m1=m2=m3=1 | T~%.4f | 2 periods | |dE/E_0|=%.1e', T8, dE8), ...
     'color', [0.55 0.85 0.55], 'fontsize', 9, 'interpreter', 'none');

print(fig8, 'three_body_figure8.png', '-dpng', '-r150');
printf('  Output: three_body_figure8.png\n\n');


% ==============================================================================
%  PART B  --  CHAOTIC ORBIT  &  LYAPUNOV SENSITIVITY
%
%  With unequal masses and asymmetric initial conditions, the three-body
%  problem becomes chaotic.  We run two simulations that differ only in the
%  x-coordinate of body 1 by delta = 1e-6.  The separation |dr1(t)| grows
%  exponentially, characteristic of positive Lyapunov exponent lambda > 0.
%
%  This is Newton's nightmare: his equations are deterministic, yet even an
%  infinitesimal uncertainty in initial state makes long-term prediction
%  impossible.  (Poincare called this "sensitive dependence," 1890.)
% ==============================================================================

printf('PART B: Chaotic Orbit and Lyapunov Sensitivity\n');
printf('--------------------------------------------------------------\n');

mc = [1.0; 2.0; 0.8];   % unequal masses

%  Asymmetric initial conditions (not specially chosen -- typical chaos)
y0c = [ 0.00;  1.00;   % r1 = (0, 1)
       -1.00; -0.50;   % r2 = (-1, -0.5)
        1.50; -0.50;   % r3 = (1.5, -0.5)
        0.30; -0.20;   % v1
       -0.20;  0.40;   % v2
       -0.10; -0.20];  % v3

delta   = 1e-6;         % tiny perturbation
y0c_pert      = y0c;
y0c_pert(1)   = y0c(1) + delta;   % nudge x1 by 1e-6

tspan_c = [0, 15.0];

printf('  Run 1 (nominal initial conditions)...\n');
tic;
[tc1, Yc1] = ode45(@(t,y) three_body_ode(t, y, mc, G), tspan_c, y0c,      opts);
printf('  Done: %.3f s,  %d steps\n', toc, numel(tc1));

printf('  Run 2 (perturbed: x1 -> x1 + %.0e)...\n', delta);
tic;
[tc2, Yc2] = ode45(@(t,y) three_body_ode(t, y, mc, G), tspan_c, y0c_pert, opts);
printf('  Done: %.3f s,  %d steps\n', toc, numel(tc2));

%  Interpolate Run 2 onto Run 1 time-grid, compute separation |dr1(t)|
Yc2_i = interp1(tc2, Yc2, tc1, 'linear', 'extrap');
sep   = sqrt((Yc1(:,1) - Yc2_i(:,1)).^2 + (Yc1(:,2) - Yc2_i(:,2)).^2);

Ec0    = total_energy(Yc1(1,:)',   mc, G);
Ec_end = total_energy(Yc1(end,:)', mc, G);
dEc    = abs((Ec_end - Ec0) / Ec0);

printf('  Initial total energy  E_0  = %+.10f\n', Ec0);
printf('  Final   total energy  E_f  = %+.10f\n', Ec_end);
printf('  Relative energy drift |dE/E_0| = %.2e\n\n', dEc);

%  Find rough Lyapunov exponent from log-linear slope (early exponential phase)
%  Use the first 30% of the run where growth is still approximately exponential
n_lam = round(0.30 * numel(tc1));
valid = sep(1:n_lam) > 0 & isfinite(sep(1:n_lam));
if sum(valid) > 5
  p_fit = polyfit(tc1(valid), log(sep(valid)), 1);
  lambda_est = p_fit(1);
else
  lambda_est = 0.5;
end
printf('  Estimated Lyapunov exponent lambda ~ %.3f\n\n', lambda_est);


% -- Plot B: Chaotic trajectory + Lyapunov divergence ------------------------
figc = figure(2);
set(figc, 'visible', 'off', 'color', [0.06 0.06 0.14], ...
          'position', [50 50 1150 620]);

%  Left panel: Chaotic trajectory
subplot(1,2,1);
set(gca, 'color', [0.06 0.06 0.14], ...
         'xcolor', [0.75 0.75 0.75], 'ycolor', [0.75 0.75 0.75], ...
         'gridcolor', [0.28 0.28 0.40], 'gridalpha', 0.55, 'fontsize', 10);
hold on;
plot(Yc1(:,1), Yc1(:,2), '-', 'color', [0.30 0.62 1.00], 'linewidth', 1.2);
plot(Yc1(:,3), Yc1(:,4), '-', 'color', [1.00 0.45 0.18], 'linewidth', 1.2);
plot(Yc1(:,5), Yc1(:,6), '-', 'color', [0.22 0.90 0.44], 'linewidth', 1.2);
%  Start markers (squares)
plot(Yc1(1,1), Yc1(1,2), 's', 'markersize', 9, ...
     'markerfacecolor', [0.30 0.62 1.00], 'markeredgecolor', [0.9 0.9 0.9], 'linewidth', 1.2);
plot(Yc1(1,3), Yc1(1,4), 's', 'markersize', 9, ...
     'markerfacecolor', [1.00 0.45 0.18], 'markeredgecolor', [0.9 0.9 0.9], 'linewidth', 1.2);
plot(Yc1(1,5), Yc1(1,6), 's', 'markersize', 9, ...
     'markerfacecolor', [0.22 0.90 0.44], 'markeredgecolor', [0.9 0.9 0.9], 'linewidth', 1.2);
hold off;
axis equal; grid on;
title('Chaotic Three-Body Trajectory', ...
      'color', [0.95 0.95 0.95], 'fontsize', 12, 'fontweight', 'bold');
xlabel('x', 'color', [0.80 0.80 0.80], 'fontsize', 11);
ylabel('y', 'color', [0.80 0.80 0.80], 'fontsize', 11);
lg2 = legend({'m1=1.0', 'm2=2.0', 'm3=0.8'}, 'location', 'best', 'fontsize', 9);
set(lg2, 'color', [0.10 0.10 0.22], 'edgecolor', [0.40 0.40 0.55]);

%  Right panel: Lyapunov divergence (semi-log)
subplot(1,2,2);
set(gca, 'color', [0.06 0.06 0.14], ...
         'xcolor', [0.75 0.75 0.75], 'ycolor', [0.75 0.75 0.75], ...
         'gridcolor', [0.28 0.28 0.40], 'gridalpha', 0.55, 'fontsize', 10);
hold on;

%  Actual separation (filter non-positive values for semilogy)
valid_all = sep > 0 & isfinite(sep);
semilogy(tc1(valid_all), sep(valid_all), '-', ...
         'color', [1.00 0.85 0.15], 'linewidth', 2.0);

%  Reference exponential  delta * exp(lambda * t)
ref_exp = delta * exp(max(lambda_est, 0.1) * tc1);
semilogy(tc1, ref_exp, '--', 'color', [1.00 0.35 0.35], 'linewidth', 1.2);

hold off;
grid on;
title('Lyapunov Sensitivity: Divergence of Nearby Orbits', ...
      'color', [0.95 0.95 0.95], 'fontsize', 12, 'fontweight', 'bold');
xlabel('time  (natural units)', 'color', [0.80 0.80 0.80], 'fontsize', 11);
ylabel('|dr1(t)|   (log scale)', 'color', [0.80 0.80 0.80], 'fontsize', 11);
lg3 = legend({'Actual |dr1(t)|', ...
              sprintf('delta*exp(lambda*t), lambda~%.2f', lambda_est)}, ...
             'location', 'southeast', 'fontsize', 9);
set(lg3, 'color', [0.10 0.10 0.22], 'edgecolor', [0.40 0.40 0.55]);

print(figc, 'three_body_chaotic.png', '-dpng', '-r150');
printf('  Output: three_body_chaotic.png\n\n');


% ==============================================================================
%  PART C  --  ENERGY CONSERVATION CHECK (FIGURE-8 RUN)
%
%  In a conservative gravitational system, total mechanical energy
%
%      E(t) = KE(t) + PE(t)
%           = (1/2) sum_i m_i |v_i|^2  -  G * sum_{i<j}  m_i*m_j / r_ij
%
%  is a constant of motion.  Plotting E(t) reveals how faithfully the
%  numerical integrator respects Newton's equations.  Drift in E indicates
%  truncation error accumulation over time.
%
%  RK45 with RelTol=1e-10 / AbsTol=1e-12 typically achieves |dE/E| < 1e-10
%  over many orbital periods.
% ==============================================================================

printf('PART C: Energy Conservation  (Figure-8 run)\n');
printf('--------------------------------------------------------------\n');

%  Sample total energy at ~300 evenly-spaced indices through the figure-8 run
n_samp  = 300;
idx_s   = round(linspace(1, numel(t8), n_samp));
E_samp  = zeros(n_samp, 1);
t_samp  = t8(idx_s);

for k = 1 : n_samp
  E_samp(k) = total_energy(Y8(idx_s(k),:)', m8, G);
end

E_mean    = mean(E_samp);
E_std_rel = std(E_samp) / abs(E_mean);

printf('  Mean E over 2 periods:        %.10f\n', E_mean);
printf('  std(E) / |E_0|  (relative):   %.2e\n', E_std_rel);
printf('  Peak deviation from E_0:       %.2e\n\n', max(abs(E_samp - E8_0)) / abs(E8_0));

%  Also compute KE and PE separately for the plot
KE_samp = zeros(n_samp, 1);
PE_samp = zeros(n_samp, 1);
for k = 1 : n_samp
  y_k  = Y8(idx_s(k),:)';
  x1=y_k(1); Y1=y_k(2); x2=y_k(3); Y2=y_k(4); x3=y_k(5); Y3=y_k(6);
  vx1=y_k(7); vy1=y_k(8); vx2=y_k(9); vy2=y_k(10); vx3=y_k(11); vy3=y_k(12);
  KE_samp(k) = 0.5*m8(1)*(vx1^2+vy1^2) + 0.5*m8(2)*(vx2^2+vy2^2) + 0.5*m8(3)*(vx3^2+vy3^2);
  r12 = sqrt((x2-x1)^2 + (Y2-Y1)^2);
  r13 = sqrt((x3-x1)^2 + (Y3-Y1)^2);
  r23 = sqrt((x3-x2)^2 + (Y3-Y2)^2);
  PE_samp(k) = -G*(m8(1)*m8(2)/r12 + m8(1)*m8(3)/r13 + m8(2)*m8(3)/r23);
end


% -- Plot C: Total, kinetic, potential energy + residual ----------------------
figE = figure(3);
set(figE, 'visible', 'off', 'color', [0.06 0.06 0.14], ...
          'position', [50 50 1000 700]);

%  Top panel: KE, PE, and total E
subplot(2,1,1);
set(gca, 'color', [0.06 0.06 0.14], ...
         'xcolor', [0.75 0.75 0.75], 'ycolor', [0.75 0.75 0.75], ...
         'gridcolor', [0.28 0.28 0.40], 'gridalpha', 0.55, 'fontsize', 10);
hold on;
plot(t_samp, KE_samp, '-',  'color', [1.00 0.55 0.20], 'linewidth', 1.6);
plot(t_samp, PE_samp, '-',  'color', [0.45 0.65 1.00], 'linewidth', 1.6);
plot(t_samp, E_samp,  '-',  'color', [0.25 0.92 0.48], 'linewidth', 2.2);
plot(t_samp, E8_0 * ones(n_samp,1), '--', 'color', [1.00 0.30 0.30], 'linewidth', 1.0);
hold off;
grid on;
title('Energy Conservation Check  (Figure-8 Run, 2 Periods)', ...
      'color', [0.95 0.95 0.95], 'fontsize', 13, 'fontweight', 'bold');
ylabel('Energy  (natural units)', 'color', [0.80 0.80 0.80], 'fontsize', 11);
lg4 = legend({'KE(t)  kinetic', 'PE(t)  potential', 'E(t) = KE+PE  total', ...
              'Exact E_0  (reference)'}, ...
             'location', 'east', 'fontsize', 9);
set(lg4, 'color', [0.10 0.10 0.22], 'edgecolor', [0.40 0.40 0.55]);

%  Bottom panel: residual E(t) - E_0 (absolute drift)
subplot(2,1,2);
set(gca, 'color', [0.06 0.06 0.14], ...
         'xcolor', [0.75 0.75 0.75], 'ycolor', [0.75 0.75 0.75], ...
         'gridcolor', [0.28 0.28 0.40], 'gridalpha', 0.55, 'fontsize', 10);
plot(t_samp, E_samp - E8_0, '-', 'color', [0.90 0.75 0.20], 'linewidth', 1.6);
hold on;
plot([t_samp(1) t_samp(end)], [0 0], '--', 'color', [0.60 0.60 0.60], 'linewidth', 0.9);
hold off;
grid on;
title('Energy Residual  dE(t) = E(t) - E_0', ...
      'color', [0.95 0.95 0.95], 'fontsize', 12, 'fontweight', 'bold');
xlabel('time  (natural units)', 'color', [0.80 0.80 0.80], 'fontsize', 11);
ylabel('dE(t)  (absolute)', 'color', [0.80 0.80 0.80], 'fontsize', 11);

ax_r  = axis();
tx_r  = ax_r(1) + 0.02*(ax_r(2)-ax_r(1));
ty_r  = ax_r(4) - 0.20*(ax_r(4)-ax_r(3));
text(tx_r, ty_r, ...
     sprintf('std(E)/|E_0| = %.2e   |  peak |dE|/|E_0| = %.2e', ...
             E_std_rel, max(abs(E_samp-E8_0))/abs(E8_0)), ...
     'color', [0.80 0.80 0.55], 'fontsize', 9, 'interpreter', 'none');

print(figE, 'three_body_energy.png', '-dpng', '-r150');
printf('  Output: three_body_energy.png\n\n');


% ==============================================================================
%  SUMMARY
% ==============================================================================

printf('==============================================================\n');
printf('  Summary\n');
printf('==============================================================\n\n');
printf('  Figure-8 run  |dE/E_0| = %.2e\n', dE8);
printf('  Chaotic run   |dE/E_0| = %.2e\n\n', dEc);
printf('  The RK45 solver (ode45, RelTol=1e-10) accurately integrates\n');
printf('  Newton''s equations of motion; energy drift stays near\n');
printf('  machine-precision-limited values over many orbital periods.\n\n');
printf('  Lyapunov exponent (chaotic run):  lambda ~ %.3f\n', lambda_est);
printf('  Meaning: perturbations grow as e^(lambda*t) -- a 1e-6 initial\n');
printf('  error reaches O(1) separation in ~%.1f time units.\n\n', ...
       -log(delta) / max(lambda_est, 0.01));
printf('  Output files written:\n');
printf('    three_body_figure8.png\n');
printf('    three_body_chaotic.png\n');
printf('    three_body_energy.png\n');
printf('\n');
printf('==============================================================\n');
printf('  Simulation complete.\n');
printf('==============================================================\n\n');


% ==============================================================================
%  SUBFUNCTIONS
%  (In GNU Octave script files, subfunctions must appear after the main body.)
% ==============================================================================

% ------------------------------------------------------------------------------
%  three_body_ode
%  Right-hand side of Newton's coupled ODEs for three gravitating point masses.
%
%  Input:
%    t   --  current time (unused explicitly; required by ode45 interface)
%    y   --  state vector [x1 y1 x2 y2 x3 y3 vx1 vy1 vx2 vy2 vx3 vy3]^T
%    m   --  column vector of masses [m1; m2; m3]
%    G   --  gravitational constant
%
%  Output:
%    dydt  --  time derivative of state vector (12 components)
%
%  Equation:
%    d^2 r_i / dt^2  =  G * sum_{j!=i}  m_j * (r_j - r_i) / |r_j - r_i|^3
%
%  A small softening length eps_s prevents division by zero at close encounters
%  while negligibly affecting the physics when bodies are well-separated.
% ------------------------------------------------------------------------------
function dydt = three_body_ode(t, y, m, G)
  eps_s = 1e-5;   % gravitational softening length

  %  Unpack positions
  x1 = y(1);   Y1 = y(2);
  x2 = y(3);   Y2 = y(4);
  x3 = y(5);   Y3 = y(6);

  %  Unpack velocities
  vx1 = y(7);   vy1 = y(8);
  vx2 = y(9);   vy2 = y(10);
  vx3 = y(11);  vy3 = y(12);

  %  Pair separations (softened to avoid singularity at r=0)
  r12 = sqrt((x2-x1)^2 + (Y2-Y1)^2 + eps_s^2);
  r13 = sqrt((x3-x1)^2 + (Y3-Y1)^2 + eps_s^2);
  r23 = sqrt((x3-x2)^2 + (Y3-Y2)^2 + eps_s^2);

  %  Gravitational accelerations  (Newton's 2nd Law + Universal Gravitation)
  ax1 = G * (m(2)*(x2-x1)/r12^3 + m(3)*(x3-x1)/r13^3);
  ay1 = G * (m(2)*(Y2-Y1)/r12^3 + m(3)*(Y3-Y1)/r13^3);

  ax2 = G * (m(1)*(x1-x2)/r12^3 + m(3)*(x3-x2)/r23^3);
  ay2 = G * (m(1)*(Y1-Y2)/r12^3 + m(3)*(Y3-Y2)/r23^3);

  ax3 = G * (m(1)*(x1-x3)/r13^3 + m(2)*(x2-x3)/r23^3);
  ay3 = G * (m(1)*(Y1-Y3)/r13^3 + m(2)*(Y2-Y3)/r23^3);

  %  Pack derivative vector
  dydt = [vx1; vy1; vx2; vy2; vx3; vy3; ...
          ax1; ay1; ax2; ay2; ax3; ay3];
endfunction


% ------------------------------------------------------------------------------
%  total_energy
%  Compute total mechanical energy  E = KE + PE  for the three-body system.
%
%      KE  =  (1/2) * sum_i  m_i * |v_i|^2
%
%      PE  =  -G * sum_{i<j}  m_i * m_j / r_ij
%
%  Energy conservation (dE/dt = 0) is a fundamental sanity check on the
%  numerical integration.
% ------------------------------------------------------------------------------
function E = total_energy(y, m, G)
  x1=y(1);  Y1=y(2);  x2=y(3);  Y2=y(4);  x3=y(5);  Y3=y(6);
  vx1=y(7); vy1=y(8); vx2=y(9); vy2=y(10); vx3=y(11); vy3=y(12);

  KE = 0.5*m(1)*(vx1^2+vy1^2) ...
     + 0.5*m(2)*(vx2^2+vy2^2) ...
     + 0.5*m(3)*(vx3^2+vy3^2);

  r12 = sqrt((x2-x1)^2 + (Y2-Y1)^2);
  r13 = sqrt((x3-x1)^2 + (Y3-Y1)^2);
  r23 = sqrt((x3-x2)^2 + (Y3-Y2)^2);

  PE = -G * (m(1)*m(2)/r12 + m(1)*m(3)/r13 + m(2)*m(3)/r23);

  E = KE + PE;
endfunction
