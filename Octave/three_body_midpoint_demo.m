% three_body_midpoint_demo.m
% GNU Octave demonstration
% Shows two linked ideas:
% 1) Midpoint Riemann sum for sin(x) - the "unit circle above and below"
% 2) Using the same midpoint idea to integrate Newton's three-body equations
%
% Run in Octave: three_body_midpoint_demo

function three_body_midpoint_demo()
  printf('Part 1: Midpoint Riemann sum for sin(x) from 0 to 2*pi\n');
  demo_sine_midpoint();

  printf('\nPart 2: Three-body problem integrated with leapfrog (midpoint) method\n');
  demo_three_body();
endfunction

function demo_sine_midpoint()
  % Exact integral of sin is zero over full period, 2 over half period
  a = 0; b = 2*pi;
  n = 100;
  dx = (b-a)/n;
  mids = a + dx/2 : dx : b - dx/2;
  heights = sin(mids); % sin = y-coordinate on unit circle
  M = sum(heights)*dx;

  printf('  n = %d, midpoint sum = %.8f (exact 0)\n', n, M);

  % Plot to visualize "above and below"
  figure(1); clf;
  x = linspace(a,b,1000);
  plot(x, sin(x), 'b', 'linewidth', 2); hold on;
  plot(x, zeros(size(x)), 'k--');
  % draw a few midpoint rectangles
  for i = 1:10:n
    xm = mids(i);
    ym = heights(i);
    rectangle('Position',[xm-dx/2, 0, dx, ym], 'EdgeColor','r', 'FaceAlpha',0.1);
  endfor
  title('Midpoint Riemann sum for sin(x) - positive = above, negative = below');
  xlabel('x'); ylabel('sin(x) = y on unit circle');
  axis tight; grid on;
endfunction

function demo_three_body()
  % Simple planar Newtonian three-body, equal masses, G=1
  % Uses leapfrog integrator, which is a midpoint method:
  %   v_{n+1/2} = v_n + a_n*dt/2
  %   r_{n+1}   = r_n + v_{n+1/2}*dt
  % This is exactly "take the slope at the middle of the interval"

  G = 1.0;
  m = [1.0, 1.0, 1.0];

  % Figure-eight initial conditions (Chenciner-Montgomery)
  r = zeros(3,2);
  v = zeros(3,2);
  r(1,:) = [-0.97000436,  0.24308753];
  r(2,:) = [ 0.97000436, -0.24308753];
  r(3,:) = [ 0, 0];
  v(1,:) = [ 0.466203685,  0.43236573];
  v(2,:) = [ 0.466203685,  0.43236573];
  v(3,:) = [-0.93240737,  -0.86473146];

  dt = 0.005;
  tmax = 10;
  steps = floor(tmax/dt);

  % storage for plotting
  traj = zeros(steps+1, 3, 2);
  traj(1,:,:) = r;

  % initial half-step velocity
  a = accelerations(r, m, G);
  v_half = v + 0.5*dt*a;

  for k = 1:steps
    % midpoint position update
    r = r + dt*v_half;
    % new acceleration at midpoint-evolved position
    a = accelerations(r, m, G);
    % midpoint velocity update
    v_half = v_half + dt*a;
    traj(k+1,:,:) = r;
  endfor

  figure(2); clf; hold on;
  colors = ['r','g','b'];
  for i = 1:3
    xi = squeeze(traj(:,i,1));
    yi = squeeze(traj(:,i,2));
    plot(xi, yi, colors(i), 'linewidth', 1.5);
    plot(xi(1), yi(1), [colors(i) 'o'], 'markersize',8, 'markerfacecolor',colors(i));
  endfor
  title('Three-body figure-eight integrated with midpoint (leapfrog) method');
  xlabel('x'); ylabel('y');
  axis equal; grid on;
  legend('Body1','start1','Body2','start2','Body3','start3','location','best');
  printf('  Simulation complete: %d steps, dt=%.4f\n', steps, dt);
  printf('  Energy drift is small because leapfrog is symplectic (midpoint-based).\n');
endfunction

function a = accelerations(r, m, G)
  % Newtonian gravity: a_i = sum_{j!=i} G m_j (r_j - r_i)/|r_j - r_i|^3
  n = size(r,1);
  a = zeros(n,2);
  for i = 1:n
    ai = [0,0];
    for j = 1:n
      if j==i, continue; endif
      dr = r(j,:) - r(i,:);
      dist3 = (sqrt(sum(dr.^2)))^3 + 1e-10; % avoid singularity
      ai = ai + G*m(j)*dr/dist3;
    endfor
    a(i,:) = ai;
  endfor
endfunction

% auto-run if file is executed directly
if (nargin == 0 && nargout == 0 && strcmp(mfilename, 'three_body_midpoint_demo'))
  three_body_midpoint_demo();
endif
