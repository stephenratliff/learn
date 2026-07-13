% ==============================================================================
%  three_body_schrodinger.m
%
%  Schrodinger's Cat and the Three-Body Problem
%  -- The Middle Body: Present or Absent?
% ==============================================================================
%
%  CONCEPT
%  -------
%  Three gravitating bodies: 1 (left), 3 (middle), 2 (right).
%  Body 3 -- the "Schrodinger body" -- sits between bodies 1 and 2.
%  In classical physics, it is either PRESENT or ABSENT.
%  In quantum mechanics, it is in SUPERPOSITION of both until observed.
%
%  This mirrors Schrodinger's Cat (1935) precisely:
%    Body 3 present  <-->  Cat alive
%    Body 3 absent   <-->  Cat dead
%    Superposition   <-->  Cat alive AND dead simultaneously
%    Measurement     <-->  Opening the box (wavefunction collapse)
%
%  CRUCIAL PHYSICS: THE MIDDLE BODY AS GRAVITATIONAL GLUE
%  -------------------------------------------------------
%  Initial conditions: Euler's Collinear Three-Body Solution (1767).
%  Three equal masses on a rotating line: -L ... 0 ... +L
%  Bodies 1 and 2 orbit around the stationary middle body (body 3)
%  at exactly the angular velocity that maintains a rigid collinear rotation:
%
%      omega^2 = G * m * 5 / (4 * L^3)
%
%  With these initial velocities:
%    Universe 1 (body 3 PRESENT):  the system is BOUND (E < 0).
%                                   Bodies 1 and 2 orbit; body 3 stays at center.
%
%    Universe 2 (body 3 ABSENT):   bodies 1 and 2 ESCAPE each other! (E > 0)
%                                   The orbital speed is above escape velocity
%                                   for a two-body system without body 3.
%
%  Body 3 is the gravitational glue holding the universe together.
%  Remove the middle body (open the box; cat dead) and the universe flies apart.
%
%  QUANTUM MECHANICS (Schrodinger Equation, 1926)
%  -----------------------------------------------
%  Before measurement, the quantum state of the system is entangled:
%
%      |PSI(t)> = alpha(t)|Universe_1> + beta(t)|Universe_2>
%
%  where |alpha|^2 = P_present(t), |beta|^2 = 1 - P_present(t).
%
%  Rabi oscillations: the cat oscillates between alive and dead.
%      P_present(t) = cos^2(Omega_Q * t)                 [pure quantum]
%
%  Decoherence (environmental coupling causes phase loss):
%      P_present(t) = e^(-gamma*t) * cos^2(Omega_Q*t)    [decohering]
%                   + (1 - e^(-gamma*t)) * 0.5
%
%  Quantum EXPECTED position of body 1 (entangled with body 3's state):
%      <r1(t)> = P(t) * r1_3body(t) + (1-P(t)) * r1_2body(t)
%
%  Since r1_3body is a bounded orbit and r1_2body escapes to infinity,
%  the expected trajectory of body 1 ALSO escapes -- proportional to
%  the probability of finding body 3 absent.
%
%  DEMONSTRATIONS
%  --------------
%  A  --  Two Classical Universes  (alive vs. dead; bound vs. escaping)
%  B  --  Quantum Superposition    (expected trajectory + Rabi oscillations)
%  C  --  Wavefunction Collapse    (Monte Carlo ensemble of observers)
%  D  --  Decoherence              (quantum coherence fading to classical mix)
%
%  USAGE:  octave three_body_schrodinger.m
%
%  OUTPUT:
%    schrodinger_universes.png     -- two classical universes
%    schrodinger_superposition.png -- quantum expected trajectory
%    schrodinger_collapse.png      -- collapse ensemble
%    schrodinger_decoherence.png   -- decoherence and P(t)
% ==============================================================================

clear all; close all; clc;

printf('\n');
printf('==============================================================\n');
printf('  Schrodinger''s Cat and the Three-Body Problem\n');
printf('  The Middle Body: Present or Absent?\n');
printf('  GNU Octave Simulation\n');
printf('==============================================================\n\n');


% ==============================================================================
%  PARAMETERS
% ==============================================================================

G         = 1.0;    % Gravitational constant (natural units)
Omega_Q   = 0.75;   % Rabi frequency: P_present(t) oscillates at this rate
gamma_dec = 0.22;   % Decoherence rate: coherence decays as exp(-gamma*t)
N_obs     = 35;     % Number of observers for collapse ensemble
N_grid    = 4000;   % Time-grid resolution for quantum calculations

opts = odeset('RelTol', 1e-10, 'AbsTol', 1e-12);


% ==============================================================================
%  INITIAL CONDITIONS: Euler Collinear Three-Body Solution (1767)
%
%  Three equal masses on a rotating line:
%      r1 = (-L, 0),   r3 = (0, 0),   r2 = (+L, 0)
%
%  For rigid collinear rotation, Newton's 2nd Law on body 1:
%    Gravitational forces from body 2 and body 3 both pull in +x direction.
%    Force from body 2: G*m^2 / (2L)^2 = G*m^2 / (4L^2)
%    Force from body 3: G*m^2 / L^2
%    Total inward force: G*m^2 * (1/L^2 + 1/(4L^2)) = 5*G*m^2 / (4L^2)
%
%    Centripetal requirement: m * omega^2 * L = 5*G*m^2 / (4L^2)
%    => omega^2 = 5*G*m / (4*L^3)
%
%  Velocities: rigid rotation v_i = omega * perpendicular(r_i)
%    v1 = omega*L * (0, +1)  [body 1 at left, moves upward]
%    v3 = 0                  [body 3 at origin, stationary]
%    v2 = omega*L * (0, -1)  [body 2 at right, moves downward]
%
%  ENERGY BALANCE:
%    With body 3 PRESENT:  E = -5*G*m^2/(4*L) < 0  --> BOUND
%    With body 3 ABSENT:   E = +3*G*m^2/(4*L) > 0  --> ESCAPING
%    (body 3 is the gravitational glue holding the system together)
% ==============================================================================

m  = [1.0; 1.0; 1.0];   % equal unit masses
L  = 1.0;                % half-separation between bodies 1 and 2

omega = sqrt(5.0 * G * m(1) / (4.0 * L^3));   % Euler collinear omega
T_orb = 2.0 * pi / omega;                       % orbital period

% Initial positions: collinear  r1 = -L,  r3 = 0,  r2 = +L
% Initial velocities: rigid rotation
y0 = [-L;    0.0;      % r1
       +L;    0.0;      % r2
        0.0;  0.0;      % r3  (middle body, the "cat")
        0.0;  omega*L;  % v1  (moves in +y)
        0.0; -omega*L;  % v2  (moves in -y)
        0.0;  0.0];     % v3  (stationary at origin)

m_present = [1.0; 1.0; 1.0];   % body 3 present  (cat alive)
m_absent  = [1.0; 1.0; 0.0];   % body 3 absent   (cat dead)

printf('System parameters:\n');
printf('  L = %.2f,  m = %.2f,  G = %.2f\n', L, m(1), G);
printf('  Euler collinear omega  = %.6f\n', omega);
printf('  Orbital period T_orb   = %.4f\n', T_orb);
printf('  Rabi frequency Omega_Q = %.4f\n', Omega_Q);
printf('  Decoherence rate gamma = %.4f  (tau_deco = %.2f)\n', ...
       gamma_dec, 1/gamma_dec);
printf('\n');

% Energy analysis
KE0     = 0.5*m(1)*(omega*L)^2 + 0.5*m(2)*(omega*L)^2;   % body 3 has v=0
E_pres  = KE0 - G*(m(1)*m(2)/(2*L) + m(1)*m(3)/L + m(2)*m(3)/L);
E_abs   = KE0 - G*(m(1)*m(2)/(2*L));
printf('Energy analysis:\n');
printf('  KE_0 (bodies 1&2)      = %+.4f\n', KE0);
printf('  Total E with body 3    = %+.4f  (BOUND: E < 0)\n', E_pres);
printf('  Total E without body 3 = %+.4f  (ESCAPING: E > 0)\n', E_abs);
printf('  => Body 3 is the gravitational glue.\n\n');


% ==============================================================================
%  INTEGRATE BOTH CLASSICAL UNIVERSES
% ==============================================================================

t_end  = 2.5 * T_orb;
tspan  = [0.0, t_end];

printf('Integrating Universe 1: body 3 PRESENT (cat alive, bound)...\n');
tic;
[t3B, Y3B] = ode45(@(t,y) three_body_ode(t, y, m_present, G), tspan, y0, opts);
printf('  Done: %.3f s  |  %d steps\n', toc, numel(t3B));

printf('Integrating Universe 2: body 3 ABSENT  (cat dead, escaping)...\n');
tic;
[t2B, Y2B] = ode45(@(t,y) three_body_ode(t, y, m_absent,  G), tspan, y0, opts);
printf('  Done: %.3f s  |  %d steps\n', toc, numel(t2B));

printf('\n');
printf('  3-body |dE/E| = %.2e\n', ...
       abs(total_energy(Y3B(end,:)', m_present, G) - E_pres) / abs(E_pres));
printf('  2-body |dE/E| = %.2e\n', ...
       abs(total_energy(Y2B(end,:)', m_absent,  G) - E_abs)  / abs(E_abs));

% Maximum radius reached by bodies 1&2 in the escaping universe
r1_2B_max = max(sqrt(Y2B(:,1).^2 + Y2B(:,2).^2));
printf('  Max |r1| in escaping 2B universe: %.2f\n\n', r1_2B_max);


% ==============================================================================
%  QUANTUM CALCULATIONS ON COMMON TIME GRID
% ==============================================================================

t_grid = linspace(0, t_end, N_grid)';

% Interpolate both universes onto common grid
Y3i = interp1(t3B, Y3B, t_grid);
Y2i = interp1(t2B, Y2B, t_grid);

% Coherence envelope and quantum probabilities
%   Pure quantum:  P(t) = cos^2(Omega_Q * t)
%   Decohering:    P(t) = e^(-gamma*t)*cos^2(Omega_Q*t) + (1-e^(-gamma*t))*0.5
%   Classical:     P = 0.5  (equal mixture, no interference)
coh      = exp(-gamma_dec * t_grid);
P_pure   = cos(Omega_Q * t_grid).^2;
P_deco   = coh .* P_pure + (1 - coh) * 0.5;
P_class  = 0.5 * ones(N_grid, 1);

% Quantum expected positions of body 1
%   <r1(t)> = P(t)*r1_3body(t) + (1-P(t))*r1_2body(t)
r1x_pure = P_pure  .* Y3i(:,1) + (1 - P_pure)  .* Y2i(:,1);
r1y_pure = P_pure  .* Y3i(:,2) + (1 - P_pure)  .* Y2i(:,2);
r1x_deco = P_deco  .* Y3i(:,1) + (1 - P_deco)  .* Y2i(:,1);
r1y_deco = P_deco  .* Y3i(:,2) + (1 - P_deco)  .* Y2i(:,2);
r1x_cl   = P_class .* Y3i(:,1) + (1 - P_class) .* Y2i(:,1);
r1y_cl   = P_class .* Y3i(:,2) + (1 - P_class) .* Y2i(:,2);

% Quantum expected position of body 2
r2x_deco = P_deco .* Y3i(:,3) + (1 - P_deco) .* Y2i(:,3);
r2y_deco = P_deco .* Y3i(:,4) + (1 - P_deco) .* Y2i(:,4);

% "Ghost" body 3: its position weighted by P_present
% When P=1 it appears fully; when P=0 it is invisible (absent)
r3x_ghost = P_deco .* Y3i(:,5);
r3y_ghost = P_deco .* Y3i(:,6);


% ==============================================================================
%  PART A  --  TWO CLASSICAL UNIVERSES
%
%  Universe 1 (cat alive): Bodies 1 and 2 orbit the stationary body 3.
%                           A beautiful, stable collinear rotation.
%  Universe 2 (cat dead):  Body 3 is absent. Bodies 1 and 2, with velocities
%                           set for the 3-body orbit, now have enough energy to
%                           ESCAPE each other's gravity. They fly apart forever.
% ==============================================================================

printf('PART A: Two Classical Universes\n');
printf('--------------------------------------------------------------\n');

figA = figure(1);
set(figA, 'visible', 'off', 'color', [0.05 0.05 0.12], 'position', [50 50 1100 600]);

% -- Left: Universe 1 (3-body, bound) ----------------------------------------
subplot(1,2,1);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 10);
hold on;

c1 = [0.30 0.60 1.00];   % cobalt  -- body 1
c2 = [1.00 0.45 0.18];   % ember   -- body 2
c3 = [0.25 0.95 0.50];   % emerald -- body 3 (the cat)

plot(Y3B(:,1), Y3B(:,2), '-', 'color', c1, 'linewidth', 1.8);
plot(Y3B(:,3), Y3B(:,4), '-', 'color', c2, 'linewidth', 1.8);
plot(Y3B(:,5), Y3B(:,6), 'o', 'color', c3, 'markersize', 14, ...
     'markerfacecolor', c3, 'markeredgecolor', [0.9 0.9 0.9], 'linewidth', 1.2);

% Start markers
plot(Y3B(1,1), Y3B(1,2), 's', 'markersize', 10, ...
     'markerfacecolor', c1, 'markeredgecolor', 'w', 'linewidth', 1.2);
plot(Y3B(1,3), Y3B(1,4), 's', 'markersize', 10, ...
     'markerfacecolor', c2, 'markeredgecolor', 'w', 'linewidth', 1.2);

% Arrow direction indicators along orbit
n3 = size(Y3B, 1);
i_arr = round(n3 * 0.18);
quiver(Y3B(i_arr,1), Y3B(i_arr,2), ...
       Y3B(i_arr+3,1)-Y3B(i_arr,1), Y3B(i_arr+3,2)-Y3B(i_arr,2), ...
       3.0, 'color', c1, 'linewidth', 1.5, 'maxheadsize', 3);
quiver(Y3B(i_arr,3), Y3B(i_arr,4), ...
       Y3B(i_arr+3,3)-Y3B(i_arr,3), Y3B(i_arr+3,4)-Y3B(i_arr,4), ...
       3.0, 'color', c2, 'linewidth', 1.5, 'maxheadsize', 3);

hold off;
axis equal; grid on;
xlim([-2.2 2.2]); ylim([-2.2 2.2]);
title({'UNIVERSE 1:  Cat Alive  (body 3 PRESENT)', ...
       'System is BOUND  |  E = -1.25'}, ...
      'color', [0.95 0.95 0.95], 'fontsize', 11, 'fontweight', 'bold');
xlabel('x  (natural units)', 'color', [0.80 0.80 0.80], 'fontsize', 10);
ylabel('y  (natural units)', 'color', [0.80 0.80 0.80], 'fontsize', 10);
lga = legend({'Body 1  (left)',  'Body 2  (right)', 'Body 3  (cat / middle)'}, ...
             'location', 'southeast', 'fontsize', 8);
set(lga, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);
% Label the stationary cat
text(0.12, 0.18, 'Cat', 'color', c3, 'fontsize', 9, 'fontweight', 'bold');
text(0.12, -0.22, 'stationary', 'color', c3*0.85, 'fontsize', 7);

% -- Right: Universe 2 (2-body, unbound / escaping) ---------------------------
subplot(1,2,2);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 10);
hold on;

plot(Y2B(:,1), Y2B(:,2), '-', 'color', c1, 'linewidth', 1.8);
plot(Y2B(:,3), Y2B(:,4), '-', 'color', c2, 'linewidth', 1.8);

% Mark starting positions
plot(Y2B(1,1), Y2B(1,2), 's', 'markersize', 10, ...
     'markerfacecolor', c1, 'markeredgecolor', 'w', 'linewidth', 1.2);
plot(Y2B(1,3), Y2B(1,4), 's', 'markersize', 10, ...
     'markerfacecolor', c2, 'markeredgecolor', 'w', 'linewidth', 1.2);

% Mark origin: where the cat WAS
plot(0, 0, 'x', 'color', [0.50 0.50 0.55], 'markersize', 18, 'linewidth', 2.0);
text(0.5, 0.5, '← cat absent', 'color', [0.55 0.55 0.60], ...
     'fontsize', 9, 'interpreter', 'none');

% Arrows showing escape direction
n2 = size(Y2B, 1);
i_esc = round(n2 * 0.60);
quiver(Y2B(i_esc,1), Y2B(i_esc,2), ...
       Y2B(min(i_esc+4,n2),1)-Y2B(i_esc,1), ...
       Y2B(min(i_esc+4,n2),2)-Y2B(i_esc,2), ...
       2.5, 'color', c1, 'linewidth', 1.5, 'maxheadsize', 2);
quiver(Y2B(i_esc,3), Y2B(i_esc,4), ...
       Y2B(min(i_esc+4,n2),3)-Y2B(i_esc,3), ...
       Y2B(min(i_esc+4,n2),4)-Y2B(i_esc,4), ...
       2.5, 'color', c2, 'linewidth', 1.5, 'maxheadsize', 2);

hold off;
grid on;
ax2_lim = max(abs([Y2B(:,1); Y2B(:,2); Y2B(:,3); Y2B(:,4)])) * 1.05;
ax2_lim = min(ax2_lim, 15);
axis equal;
xlim([-ax2_lim ax2_lim]); ylim([-ax2_lim ax2_lim]);

title({'UNIVERSE 2:  Cat Dead  (body 3 ABSENT)', ...
       'System is UNBOUND  |  E = +0.75  -->  bodies escape!'}, ...
      'color', [0.95 0.95 0.95], 'fontsize', 11, 'fontweight', 'bold');
xlabel('x  (natural units)', 'color', [0.80 0.80 0.80], 'fontsize', 10);
ylabel('y  (natural units)', 'color', [0.80 0.80 0.80], 'fontsize', 10);
lgb = legend({'Body 1  (escaping)', 'Body 2  (escaping)'}, ...
             'location', 'southeast', 'fontsize', 8);
set(lgb, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

print(figA, 'schrodinger_universes.png', '-dpng', '-r150');
printf('  Output: schrodinger_universes.png\n\n');


% ==============================================================================
%  PART B  --  QUANTUM SUPERPOSITION
%
%  Before we open the box and look, the system is in superposition:
%    |PSI> = alpha|Universe_1> + beta|Universe_2>
%
%  Body 1's position is NOT definite. Quantum mechanics predicts only:
%    <r1(t)> = P(t)*r1_3B(t) + (1-P(t))*r1_2B(t)
%
%  Because r1_3B is a bounded orbit and r1_2B escapes to infinity,
%  <r1(t)> also drifts -- proportional to how much of the "cat dead"
%  state is mixed in.  The Rabi oscillation makes body 1 periodically
%  "remember" each universe.
%
%  We show:
%    -- x(t) and y(t) of body 1 under pure quantum, decohering, classical
%    -- The spatial expected trajectory (body 1) for each regime
% ==============================================================================

printf('PART B: Quantum Superposition\n');
printf('--------------------------------------------------------------\n');

figB = figure(2);
set(figB, 'visible', 'off', 'color', [0.05 0.05 0.12], 'position', [50 50 1100 700]);

% Color scheme for quantum regimes
cPure = [0.95 0.90 0.20];   % gold    -- pure quantum
cDeco = [0.85 0.45 0.95];   % violet  -- decohering
cClas = [0.65 0.65 0.65];   % grey    -- classical mixture

% Clip time to a window where the divergence is visible but not extreme
n_clip = min(N_grid, round(0.95*N_grid));

% -- Top row: time-series x(t) ------------------------------------------------
subplot(2,2,1);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 9);
hold on;
plot(t_grid(1:n_clip), Y3i(1:n_clip,1), '-', 'color', c1, 'linewidth', 1.0);
plot(t_grid(1:n_clip), Y2i(1:n_clip,1), '-', 'color', c2, 'linewidth', 1.0);
plot(t_grid(1:n_clip), r1x_pure(1:n_clip), '-', 'color', cPure, 'linewidth', 2.2);
plot(t_grid(1:n_clip), r1x_deco(1:n_clip), '-', 'color', cDeco, 'linewidth', 2.0);
plot(t_grid(1:n_clip), r1x_cl(1:n_clip),   '--','color', cClas, 'linewidth', 1.4);
hold off; grid on;
title('Body 1:  x(t)  --  Classical vs Quantum Expected', ...
      'color', [0.92 0.92 0.92], 'fontsize', 10, 'fontweight', 'bold');
xlabel('time', 'color', [0.75 0.75 0.75]);
ylabel('x_1(t)', 'color', [0.75 0.75 0.75]);
lg1 = legend({'3B classical (bound)', '2B classical (escape)', ...
              'Quantum pure', 'Quantum decohering', 'Classical P=0.5'}, ...
             'location', 'northwest', 'fontsize', 7);
set(lg1, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

% -- Top right: time-series y(t) ----------------------------------------------
subplot(2,2,2);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 9);
hold on;
plot(t_grid(1:n_clip), Y3i(1:n_clip,2), '-', 'color', c1, 'linewidth', 1.0);
plot(t_grid(1:n_clip), Y2i(1:n_clip,2), '-', 'color', c2, 'linewidth', 1.0);
plot(t_grid(1:n_clip), r1y_pure(1:n_clip), '-', 'color', cPure, 'linewidth', 2.2);
plot(t_grid(1:n_clip), r1y_deco(1:n_clip), '-', 'color', cDeco, 'linewidth', 2.0);
plot(t_grid(1:n_clip), r1y_cl(1:n_clip),   '--','color', cClas, 'linewidth', 1.4);
hold off; grid on;
title('Body 1:  y(t)  --  Classical vs Quantum Expected', ...
      'color', [0.92 0.92 0.92], 'fontsize', 10, 'fontweight', 'bold');
xlabel('time', 'color', [0.75 0.75 0.75]);
ylabel('y_1(t)', 'color', [0.75 0.75 0.75]);

% -- Bottom left: spatial trajectory (quantum, early time) --------------------
n_early = round(N_grid * 0.40);   % show first 40% of simulation

subplot(2,2,3);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 9);
hold on;
plot(Y3i(1:n_early,1), Y3i(1:n_early,2), '-', 'color', c1*0.7, 'linewidth', 0.8);
plot(Y2i(1:n_early,1), Y2i(1:n_early,2), '-', 'color', c2*0.7, 'linewidth', 0.8);
plot(r1x_pure(1:n_early), r1y_pure(1:n_early), '-', 'color', cPure, 'linewidth', 2.5);
plot(r1x_deco(1:n_early), r1y_deco(1:n_early), '-', 'color', cDeco, 'linewidth', 2.0);
% Start markers
plot(Y3i(1,1), Y3i(1,2), 'o', 'markersize', 9, 'markerfacecolor', c1, 'markeredgecolor', 'w');
plot(Y2i(1,1), Y2i(1,2), 'o', 'markersize', 9, 'markerfacecolor', c2, 'markeredgecolor', 'w');
hold off;
grid on; axis equal;
title('Spatial Path of Body 1 (early time)', ...
      'color', [0.92 0.92 0.92], 'fontsize', 10, 'fontweight', 'bold');
xlabel('x', 'color', [0.75 0.75 0.75]);
ylabel('y', 'color', [0.75 0.75 0.75]);
lg2 = legend({'3B classical', '2B classical', '<r1> pure quantum', '<r1> decohering'}, ...
             'location', 'best', 'fontsize', 7);
set(lg2, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

% -- Bottom right: P_present(t) -----------------------------------------------
subplot(2,2,4);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 9);
hold on;
plot(t_grid, P_pure,  '-', 'color', cPure, 'linewidth', 2.2);
plot(t_grid, P_deco,  '-', 'color', cDeco, 'linewidth', 2.0);
plot(t_grid, P_class, '--','color', cClas, 'linewidth', 1.2);
% Coherence envelope
plot(t_grid, 0.5 + 0.5*coh, ':', 'color', [0.45 0.85 0.60], 'linewidth', 1.2);
plot(t_grid, 0.5 - 0.5*coh, ':', 'color', [0.45 0.85 0.60], 'linewidth', 1.2);
hold off; grid on;
ylim([-0.05 1.10]);
title('P_{present}(t): Schrodinger''s Cat Alive Probability', ...
      'color', [0.92 0.92 0.92], 'fontsize', 10, 'fontweight', 'bold');
xlabel('time', 'color', [0.75 0.75 0.75]);
ylabel('P_{present}(t)', 'color', [0.75 0.75 0.75]);
lg3 = legend({'Pure quantum  cos^2(Omega*t)', ...
              sprintf('Decohering   gamma=%.2f', gamma_dec), ...
              'Classical mixture  P=0.5', ...
              'Decoherence envelope'}, ...
             'location', 'east', 'fontsize', 7);
set(lg3, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);
% Mark decoherence time
ax4 = axis();
hold on;
plot([1/gamma_dec 1/gamma_dec], [ax4(3) ax4(4)], ':', ...
     'color', [0.85 0.60 0.20], 'linewidth', 1.5);
text(1/gamma_dec + 0.2, 0.92, ...
     sprintf('tau_{deco}=%.1f', 1/gamma_dec), ...
     'color', [0.85 0.65 0.35], 'fontsize', 8, 'interpreter', 'none');
hold off;

print(figB, 'schrodinger_superposition.png', '-dpng', '-r150');
printf('  Output: schrodinger_superposition.png\n\n');


% ==============================================================================
%  PART C  --  WAVEFUNCTION COLLAPSE ENSEMBLE
%
%  N_obs observers each "open the box" (make a measurement) at a random time.
%  At measurement time t_m, the quantum probability determines the outcome:
%
%    P(t_m) = e^(-gamma*t_m) * cos^2(Omega*t_m) + (1-e^(-gamma*t_m)) * 0.5
%
%  With probability    P(t_m): body 3 IS present -> system was in Universe 1
%  With probability 1-P(t_m): body 3 IS absent  -> system was in Universe 2
%
%  After collapse:
%    Universe 1 collapse: body 1 continues the bounded orbit trajectory
%    Universe 2 collapse: body 1 continues the escaping trajectory
%
%  Visualization: we plot the body 1 path up to t_measure (quantum expected),
%  then a short trail showing the post-collapse classical trajectory.
% ==============================================================================

printf('PART C: Wavefunction Collapse Ensemble  (N=%d observers)\n', N_obs);
printf('--------------------------------------------------------------\n');

rand('state', 98765);   % reproducible seed

t_measure    = t_end * 0.85 * rand(N_obs, 1);   % random measurement times
u_outcome    = rand(N_obs, 1);                    % uniform [0,1] for outcome
collapse_to3B = false(N_obs, 1);

for j = 1:N_obs
  tm      = t_measure(j);
  coh_m   = exp(-gamma_dec * tm);
  Pm      = coh_m * cos(Omega_Q * tm)^2 + (1 - coh_m) * 0.5;
  collapse_to3B(j) = (u_outcome(j) < Pm);
end

n3B_c = sum(collapse_to3B);
n2B_c = sum(~collapse_to3B);

printf('  Outcomes: body 3 PRESENT (bound orbit):  %d of %d  (%.0f%%)\n', ...
       n3B_c, N_obs, 100*n3B_c/N_obs);
printf('  Outcomes: body 3 ABSENT  (escape):       %d of %d  (%.0f%%)\n\n', ...
       n2B_c, N_obs, 100*n2B_c/N_obs);

figC = figure(3);
set(figC, 'visible', 'off', 'color', [0.05 0.05 0.12], 'position', [50 50 1100 600]);

subplot(1,2,1);   % Left: spatial view
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 10);
hold on;

% Background: quantum expected path of body 1 (full simulation)
plot(r1x_deco, r1y_deco, '-', 'color', [0.70 0.70 0.20], 'linewidth', 0.9);

% For each observer: mark collapse event and draw brief post-collapse trail
trail_steps = round(0.12 * N_grid);   % trail length (~12% of total simulation)

for j = 1:N_obs
  tm  = t_measure(j);
  im  = max(1, round(tm / t_end * N_grid));
  
  if collapse_to3B(j)
    col_trail = [0.20 0.50 0.90] + 0.35*(1-[0.20 0.50 0.90]);
    col_mark  = [0.50 0.80 1.00];
    tx = Y3i(:,1);  ty = Y3i(:,2);
  else
    col_trail = [0.90 0.40 0.18] + 0.30*(1-[0.90 0.40 0.18]);
    col_mark  = [1.00 0.72 0.50];
    tx = Y2i(:,1);  ty = Y2i(:,2);
  end
  
  i_end_trail = min(im + trail_steps, N_grid);
  
  % Post-collapse trail
  if i_end_trail > im
    plot(tx(im:i_end_trail), ty(im:i_end_trail), '-', ...
         'color', col_trail, 'linewidth', 1.1);
  end
  
  % Collapse event marker (circle on the quantum expected path)
  xm = interp1(t_grid, r1x_deco, tm, 'linear');
  ym = interp1(t_grid, r1y_deco, tm, 'linear');
  plot(xm, ym, 'o', 'markersize', 5, ...
       'markerfacecolor', col_mark, 'markeredgecolor', 'w', 'linewidth', 0.8);
end

% Dummy plots for legend
h3B = plot(NaN, NaN, '-', 'color', [0.55 0.75 1.00], 'linewidth', 2.0);
h2B = plot(NaN, NaN, '-', 'color', [1.00 0.65 0.50], 'linewidth', 2.0);
hQ  = plot(NaN, NaN, '-', 'color', [0.70 0.70 0.20], 'linewidth', 1.5);

hold off; grid on; axis equal;
title({'Wavefunction Collapse: Body 1 Trajectory', ...
       'Dots = measurement event; trails = post-collapse classical path'}, ...
      'color', [0.95 0.95 0.95], 'fontsize', 11, 'fontweight', 'bold');
xlabel('x', 'color', [0.80 0.80 0.80], 'fontsize', 11);
ylabel('y', 'color', [0.80 0.80 0.80], 'fontsize', 11);
lgc = legend([h3B h2B hQ], ...
             {sprintf('Collapsed -> bound orbit  (%d obs.)', n3B_c), ...
              sprintf('Collapsed -> escape       (%d obs.)', n2B_c), ...
              '<r1> quantum (pre-collapse)'}, ...
             'location', 'best', 'fontsize', 8);
set(lgc, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

subplot(1,2,2);   % Right: measurement time histogram + probability
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 10);
hold on;

% Overlay P(t) curve
plot(t_grid, P_deco, '-', 'color', cDeco, 'linewidth', 2.5);
plot([0 t_end], [0.5 0.5], '--', 'color', [0.55 0.55 0.55], 'linewidth', 1.0);

% Mark each observer's measurement time and outcome
for j = 1:N_obs
  tm    = t_measure(j);
  coh_m = exp(-gamma_dec * tm);
  Pm    = coh_m * cos(Omega_Q * tm)^2 + (1 - coh_m) * 0.5;
  if collapse_to3B(j)
    plot(tm, Pm, '^', 'markersize', 7, ...
         'markerfacecolor', [0.50 0.80 1.00], 'markeredgecolor', 'w', 'linewidth', 0.8);
  else
    plot(tm, 1-Pm, 'v', 'markersize', 7, ...
         'markerfacecolor', [1.00 0.65 0.50], 'markeredgecolor', 'w', 'linewidth', 0.8);
  end
end

hold off; grid on;
ylim([-0.05 1.15]);
title({'Observer Outcomes vs P_{present}(t)', ...
       'Blue^: cat alive  |  Orange v: cat dead'}, ...
      'color', [0.95 0.95 0.95], 'fontsize', 11, 'fontweight', 'bold');
xlabel('measurement time', 'color', [0.80 0.80 0.80], 'fontsize', 11);
ylabel('P_{present}(t)', 'color', [0.80 0.80 0.80], 'fontsize', 11);
lge = legend({'P_{present}(t) [decohering]', 'P = 0.5 [classical limit]'}, ...
             'location', 'northeast', 'fontsize', 8);
set(lge, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

print(figC, 'schrodinger_collapse.png', '-dpng', '-r150');
printf('  Output: schrodinger_collapse.png\n\n');


% ==============================================================================
%  PART D  --  DECOHERENCE: QUANTUM TO CLASSICAL
%
%  In a real quantum system, interaction with the environment (photons,
%  thermal fluctuations, detector apparatus) destroys quantum coherence.
%  The density matrix off-diagonal terms (interference) decay at rate gamma:
%
%    rho(t) = | cos^2(theta)         e^(-gamma*t)*cos(theta)*sin(theta) |
%             | e^(-gamma*t)*...     sin^2(theta)                       |
%
%  As t -> inf, the off-diagonal terms vanish. The quantum superposition
%  becomes a classical probability mixture -- no more interference fringes.
%
%  Body 1's trajectory reflects this:
%    t << tau_deco:  body 1 path shimmers between the two universes
%    t >> tau_deco:  body 1 settles to P_0 * orbit + (1-P_0) * escape  (frozen)
%
%  This figure shows the transition from quantum shimmer to classical drift.
% ==============================================================================

printf('PART D: Decoherence -- Quantum to Classical\n');
printf('--------------------------------------------------------------\n');

% Sample energy of the 3-body run for energy conservation check
n_E    = 200;
idx_E  = round(linspace(1, numel(t3B), n_E));
E_samp = arrayfun(@(k) total_energy(Y3B(k,:)', m_present, G), idx_E);
t_Esamp = t3B(idx_E);
E_drift = max(abs(E_samp - E_samp(1))) / abs(E_samp(1));
printf('  3-body energy drift: %.2e\n', E_drift);

figD = figure(4);
set(figD, 'visible', 'off', 'color', [0.05 0.05 0.12], 'position', [50 50 1050 750]);

% -- Top: P(t) and coherence envelope -----------------------------------------
subplot(3,1,1);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 10);
hold on;
% Shade region between decoherence envelope
fill([t_grid; flipud(t_grid)], ...
     [0.5+0.5*coh; flipud(0.5-0.5*coh)], ...
     [0.20 0.50 0.30], 'facealpha', 0.18, 'edgecolor', 'none');
plot(t_grid, P_pure,  '-', 'color', cPure, 'linewidth', 2.0);
plot(t_grid, P_deco,  '-', 'color', cDeco, 'linewidth', 2.2);
plot(t_grid, P_class, '--','color', cClas, 'linewidth', 1.2);
plot(t_grid, 0.5 + 0.5*coh, ':', 'color', [0.45 0.85 0.60], 'linewidth', 1.5);
plot(t_grid, 0.5 - 0.5*coh, ':', 'color', [0.45 0.85 0.60], 'linewidth', 1.5);
% Decoherence time vertical line
axt = axis();
plot([1/gamma_dec 1/gamma_dec], [axt(3) 1.12], ':', ...
     'color', [0.85 0.60 0.20], 'linewidth', 1.8);
text(1/gamma_dec + 0.3, 1.04, ...
     sprintf('tau_{deco} = 1/gamma = %.1f', 1/gamma_dec), ...
     'color', [0.85 0.65 0.35], 'fontsize', 9, 'interpreter', 'none');
hold off; grid on;
ylim([-0.05 1.18]);
title('Quantum Probability P_{present}(t) and Decoherence Envelope', ...
      'color', [0.95 0.95 0.95], 'fontsize', 11, 'fontweight', 'bold');
ylabel('P_{present}(t)', 'color', [0.80 0.80 0.80]);
lgd1 = legend({'coherent window', 'Pure quantum', 'Decohering', ...
               'Classical P=0.5', 'Envelope 0.5 +/- 0.5*e^{-gamma*t}'}, ...
              'location', 'east', 'fontsize', 8);
set(lgd1, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

% -- Middle: x-coordinate of body 1 under each regime ------------------------
subplot(3,1,2);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 10);
hold on;
plot(t_grid, Y3i(:,1), '-', 'color', c1*0.7, 'linewidth', 0.8);
plot(t_grid, Y2i(:,1), '-', 'color', c2*0.7, 'linewidth', 0.8);
plot(t_grid, r1x_pure, '-', 'color', cPure, 'linewidth', 2.2);
plot(t_grid, r1x_deco, '-', 'color', cDeco, 'linewidth', 2.2);
plot(t_grid, r1x_cl,   '--','color', cClas, 'linewidth', 1.4);
hold off; grid on;
title('<x_1(t)>: Body 1 x-Position -- Quantum "Shimmer" Decaying to Classical Drift', ...
      'color', [0.95 0.95 0.95], 'fontsize', 11, 'fontweight', 'bold');
ylabel('x_1(t)', 'color', [0.80 0.80 0.80]);
lgd2 = legend({'3B classical (bound orbit)', '2B classical (escaping)', ...
               '<x_1> pure quantum', '<x_1> decohering', '<x_1> classical P=0.5'}, ...
              'location', 'northwest', 'fontsize', 8);
set(lgd2, 'color', [0.08 0.08 0.20], 'edgecolor', [0.40 0.40 0.55]);

% -- Bottom: energy conservation of 3-body run --------------------------------
subplot(3,1,3);
set(gca, 'color', [0.05 0.05 0.12], 'xcolor', [0.75 0.75 0.75], ...
         'ycolor', [0.75 0.75 0.75], 'gridcolor', [0.25 0.25 0.38], ...
         'gridalpha', 0.55, 'fontsize', 10);
hold on;
plot(t_Esamp, E_samp - E_samp(1), '-', 'color', [0.60 0.92 0.60], 'linewidth', 1.8);
plot([t_Esamp(1) t_Esamp(end)], [0 0], '--', 'color', [0.60 0.60 0.60], 'linewidth', 0.9);
hold off; grid on;
title(sprintf('Energy Residual dE(t) = E(t)-E_0  (3-body run, max |dE|/|E_0| = %.1e)', ...
              E_drift), ...
      'color', [0.95 0.95 0.95], 'fontsize', 11, 'fontweight', 'bold');
xlabel('time  (natural units)', 'color', [0.80 0.80 0.80]);
ylabel('dE(t)', 'color', [0.80 0.80 0.80]);

print(figD, 'schrodinger_decoherence.png', '-dpng', '-r150');
printf('  Output: schrodinger_decoherence.png\n\n');


% ==============================================================================
%  FINAL SUMMARY
% ==============================================================================

printf('==============================================================\n');
printf('  Schrodinger''s Cat -- Three-Body Summary\n');
printf('==============================================================\n\n');
printf('  INITIAL CONDITIONS (Euler Collinear, 1767):\n');
printf('    L = %.2f  |  omega = %.4f  |  T_orb = %.4f\n', L, omega, T_orb);
printf('\n');
printf('  ENERGIES:\n');
printf('    E (body 3 present, cat alive) = %+.4f  [BOUND]\n', E_pres);
printf('    E (body 3 absent,  cat dead)  = %+.4f  [ESCAPING]\n', E_abs);
printf('    => The middle body is gravitational glue.\n');
printf('       Remove it and the universe flies apart.\n');
printf('\n');
printf('  QUANTUM PARAMETERS:\n');
printf('    Rabi frequency   Omega_Q = %.4f\n', Omega_Q);
printf('    Decoherence rate gamma   = %.4f\n', gamma_dec);
printf('    Decoherence time tau     = %.4f\n', 1/gamma_dec);
printf('\n');
printf('  COLLAPSE ENSEMBLE (N=%d observers):\n', N_obs);
printf('    Body 3 found PRESENT (cat alive, bound):  %d  (%.0f%%)\n', ...
       n3B_c, 100*n3B_c/N_obs);
printf('    Body 3 found ABSENT  (cat dead, escape):  %d  (%.0f%%)\n', ...
       n2B_c, 100*n2B_c/N_obs);
printf('\n');
printf('  PHYSICS DEMONSTRATED:\n');
printf('    A. Two Classical Universes\n');
printf('       Alive  ->  bodies orbit beautifully, cat at center\n');
printf('       Dead   ->  bodies escape to infinity forever\n');
printf('    B. Quantum Superposition\n');
printf('       Before observation: body 1 shimmers between both paths\n');
printf('       P(t) oscillates with Rabi frequency Omega_Q\n');
printf('    C. Wavefunction Collapse\n');
printf('       Each observer collapses the system to one universe\n');
printf('       Outcome is probabilistic; determined by P(t_measure)\n');
printf('    D. Decoherence\n');
printf('       Quantum shimmer fades at rate gamma\n');
printf('       Classical behavior emerges: fixed weighted average path\n');
printf('\n');
printf('  Output files:\n');
printf('    schrodinger_universes.png\n');
printf('    schrodinger_superposition.png\n');
printf('    schrodinger_collapse.png\n');
printf('    schrodinger_decoherence.png\n');
printf('\n');
printf('==============================================================\n');
printf('  Simulation complete.\n');
printf('==============================================================\n\n');


% ==============================================================================
%  SUBFUNCTIONS  (must follow main script body in GNU Octave)
% ==============================================================================

% ------------------------------------------------------------------------------
%  three_body_ode
%  Newton''s equations of motion for three gravitating point masses.
%  If m(3) = 0: bodies 1 and 2 interact only (exact two-body problem).
%               Body 3 still follows a test-particle trajectory (no mass).
%
%  State: y = [x1 y1 x2 y2 x3 y3  vx1 vy1 vx2 vy2 vx3 vy3]^T
%  Note: x2,y2 are at indices 3,4 (body 2), x3,y3 at 5,6 (body 3 / the cat)
% ------------------------------------------------------------------------------
function dydt = three_body_ode(t, y, m, G)
  eps_s = 1e-5;   % softening to prevent 1/0 at close approach

  x1=y(1);  Y1=y(2);   % body 1 (left)
  x2=y(3);  Y2=y(4);   % body 2 (right)
  x3=y(5);  Y3=y(6);   % body 3 (middle / the cat)

  vx1=y(7);  vy1=y(8);
  vx2=y(9);  vy2=y(10);
  vx3=y(11); vy3=y(12);

  r12 = sqrt((x2-x1)^2 + (Y2-Y1)^2 + eps_s^2);
  r13 = sqrt((x3-x1)^2 + (Y3-Y1)^2 + eps_s^2);
  r23 = sqrt((x3-x2)^2 + (Y3-Y2)^2 + eps_s^2);

  % d^2r_i/dt^2 = G * sum_{j!=i} m_j*(r_j - r_i) / |r_j - r_i|^3
  ax1 = G * (m(2)*(x2-x1)/r12^3 + m(3)*(x3-x1)/r13^3);
  ay1 = G * (m(2)*(Y2-Y1)/r12^3 + m(3)*(Y3-Y1)/r13^3);

  ax2 = G * (m(1)*(x1-x2)/r12^3 + m(3)*(x3-x2)/r23^3);
  ay2 = G * (m(1)*(Y1-Y2)/r12^3 + m(3)*(Y3-Y2)/r23^3);

  ax3 = G * (m(1)*(x1-x3)/r13^3 + m(2)*(x2-x3)/r23^3);
  ay3 = G * (m(1)*(Y1-Y3)/r13^3 + m(2)*(Y2-Y3)/r23^3);

  dydt = [vx1; vy1; vx2; vy2; vx3; vy3;
          ax1; ay1; ax2; ay2; ax3; ay3];
endfunction


% ------------------------------------------------------------------------------
%  total_energy
%  E = KE + PE  =  (1/2)*sum m_i*v_i^2  -  G*sum_{i<j} m_i*m_j/r_ij
%  Handles the m3=0 case (two-body) gracefully.
% ------------------------------------------------------------------------------
function E = total_energy(y, m, G)
  x1=y(1); Y1=y(2); x2=y(3); Y2=y(4); x3=y(5); Y3=y(6);
  vx1=y(7); vy1=y(8); vx2=y(9); vy2=y(10); vx3=y(11); vy3=y(12);

  KE = 0.5*m(1)*(vx1^2+vy1^2) ...
     + 0.5*m(2)*(vx2^2+vy2^2) ...
     + 0.5*m(3)*(vx3^2+vy3^2);

  r12 = sqrt((x2-x1)^2 + (Y2-Y1)^2);
  PE  = -G * m(1)*m(2) / r12;

  if m(3) > 0
    r13 = sqrt((x3-x1)^2 + (Y3-Y1)^2);
    r23 = sqrt((x3-x2)^2 + (Y3-Y2)^2);
    PE  = PE - G*(m(1)*m(3)/r13 + m(2)*m(3)/r23);
  end

  E = KE + PE;
endfunction
