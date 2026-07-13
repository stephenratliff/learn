% schrodinger_cat_middle.m
% GNU Octave demo: Schrödinger's cat as a wavepacket that is "sometimes in the middle"
% Solves 1D time-dependent Schrödinger equation with Crank-Nicolson
% (implicit midpoint method) - the quantum analog of the leapfrog we used for 3-body
%
% i ħ ∂ψ/∂t = -ħ²/(2m) ∂²ψ/∂x² + V ψ
%
% Run: schrodinger_cat_middle

function schrodinger_cat_middle()
  printf('Schrödinger cat - probability in the middle region\n');

  % ---- physical constants (set ħ=m=1 for simplicity) ----
  hbar = 1.0; m = 1.0;

  % ---- grid ----
  L = 10.0;           % box from -L/2 to L/2
  Nx = 400;
  x = linspace(-L/2, L/2, Nx)';
  dx = x(2)-x(1);

  % ---- time ----
  dt = 0.005;
  Nt = 2000;
  t = (0:Nt-1)*dt;

  % ---- potential: flat with soft walls (particle in a box) ----
  V = zeros(Nx,1);
  V(1:5) = 1e3; V(end-4:end) = 1e3; % hard walls

  % ---- initial wavefunction: Gaussian packet offset left, moving right ----
  x0 = -2.0; sigma = 0.5; k0 = 5.0; % momentum
  psi = exp(-(x-x0).^2/(2*sigma^2)) .* exp(1i*k0*x);
  psi = psi / sqrt(sum(abs(psi).^2)*dx); % normalize

  % ---- Crank-Nicolson matrices (implicit midpoint) ----
  % Second derivative via 3-point stencil
  e = ones(Nx,1);
  Lap = spdiags([e -2*e e], -1:1, Nx, Nx) / dx^2;
  % Hamiltonian
  H = - (hbar^2/(2*m)) * Lap + spdiags(V,0,Nx,Nx);

  I = speye(Nx);
  A = I + 1i*dt/(2*hbar) * H; % left side
  B = I - 1i*dt/(2*hbar) * H; % right side

  % ---- region "middle" = central 20% of box ----
  mid_mask = abs(x) < 0.2*L;
  Pmid = zeros(1,Nt);

  % ---- time evolution ----
  figure(1); clf;
  for n = 1:Nt
    % Crank-Nicolson step: A psi^{n+1} = B psi^n
    psi = A \ (B * psi);
    % renormalize (prevents drift)
    psi = psi / sqrt(sum(abs(psi).^2)*dx);

    prob = abs(psi).^2;
    Pmid(n) = sum(prob(mid_mask))*dx;

    if mod(n,20)==1
      clf; hold on;
      plot(x, prob, 'b', 'linewidth',2);
      area(x(mid_mask), prob(mid_mask), 'FaceColor',[1 0.8 0.8], 'EdgeColor','none');
      plot(x, V/max(V)*max(prob)*0.3, 'k--'); % show walls
      ylim([0 max(prob)*1.2]);
      title(sprintf('t=%.2f  P(middle)=%.3f  (cat "in the box center")', t(n), Pmid(n)));
      xlabel('x'); ylabel('|ψ|²');
      drawnow;
    endif
  endfor

  % ---- plot probability in middle vs time ----
  figure(2); clf;
  plot(t, Pmid, 'r', 'linewidth',2);
  xlabel('time'); ylabel('P(middle)');
  title('Schrödinger''s cat: probability of being in the middle oscillates');
  grid on;
  printf('Done. The red curve shows the cat is sometimes in the middle (high) and sometimes not (low).\n');
endfunction

% auto-run
if (nargin==0 && nargout==0 && strcmp(mfilename,'schrodinger_cat_middle'))
  schrodinger_cat_middle();
endif
