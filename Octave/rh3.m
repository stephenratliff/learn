% =========================================================================
% RIEMANN HYPOTHESIS - Overview & Numerical Exploration
% GNU Octave Script
%
% Run with:  >> riemann_hypothesis
%
% The Riemann Hypothesis is one of the most famous unsolved problems in
% mathematics. Proposed by Bernhard Riemann in 1859, it concerns the
% distribution of the non-trivial zeros of the Riemann Zeta Function.
%
% STATEMENT OF THE HYPOTHESIS:
%   All non-trivial zeros of the Riemann Zeta Function zeta(s) have
%   real part equal to 1/2. That is, they lie on the "critical line"
%   Re(s) = 1/2 in the complex plane.
% =========================================================================

function riemann_hypothesis()

  % -----------------------------------------------------------------------
  % BACKGROUND (see comments throughout for theory)
  % -----------------------------------------------------------------------
  %
  % THE RIEMANN ZETA FUNCTION
  %   For Re(s) > 1:  zeta(s) = sum_{n=1}^{inf} 1/n^s
  %   Extended to all of C (except s=1) by analytic continuation.
  %
  % EULER PRODUCT (ties zeta to prime numbers):
  %   zeta(s) = prod_{p prime} 1 / (1 - p^{-s})
  %
  % ZEROS:
  %   Trivial zeros:     s = -2, -4, -6, ...
  %   Non-trivial zeros: all lie in the critical strip 0 < Re(s) < 1.
  %   RH claims every non-trivial zero satisfies Re(s) = 1/2.
  %
  % DIRICHLET ETA (for evaluation inside the critical strip):
  %   eta(s) = sum_{n=1}^{inf} (-1)^{n+1} / n^s = (1 - 2^{1-s}) * zeta(s)
  %   => zeta(s) = eta(s) / (1 - 2^{1-s})
  %
  % FIRST KNOWN NON-TRIVIAL ZEROS  s = 1/2 + i*t :
  %   t ~ 14.1347,  21.0220,  25.0109,  30.4249,  32.9351

  N = 150;   % number of eta-series terms (higher = more accurate)

  % -----------------------------------------------------------------------
  % FIGURE 1 : |zeta(1/2 + it)| along the critical line
  % -----------------------------------------------------------------------
  t_vec  = linspace(0, 50, 2000);
  s_vec  = 0.5 + 1i * t_vec;
  mag    = arrayfun(@(s) abs(zeta_via_eta(s, N)), s_vec);

  zero_t = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351];

  figure(1);
  plot(t_vec, mag, 'b-', 'LineWidth', 1.2);
  hold on;
  plot(zero_t, zeros(1, numel(zero_t)), 'ro', ...
       'MarkerSize', 8, 'MarkerFaceColor', 'r');
  xlabel('t  (imaginary part)');
  ylabel('|zeta(1/2 + it)|');
  title({'|zeta(s)| on the Critical Line  Re(s) = 1/2', ...
         'Red dots mark the first five non-trivial zeros'});
  legend('|zeta(1/2 + it)|', 'Known zeros', 'Location', 'northwest');
  grid on;
  hold off;

  % -----------------------------------------------------------------------
  % FIGURE 2 : cross-section of |zeta(sigma + 25.01i)| across the strip
  % -----------------------------------------------------------------------
  % The minimum sits at sigma = 1/2, confirming the zero lies on the
  % critical line for this value of t.

  sigma_vec = linspace(0.01, 0.99, 500);
  s_row     = sigma_vec + 1i * 25.0109;
  mag_row   = arrayfun(@(s) abs(zeta_via_eta(s, N)), s_row);

  figure(2);
  plot(sigma_vec, mag_row, 'm-', 'LineWidth', 1.5);
  xline(0.5, 'k--', 'Critical line  \sigma = 1/2', 'LineWidth', 1.2);
  xlabel('Re(s) = \sigma');
  ylabel('|zeta(\sigma + 25.01i)|');
  title('Cross-section of |zeta(s)| at Im(s) ~ 25.01  (3rd zero)');
  grid on;

  % -----------------------------------------------------------------------
  % FIGURE 3 : prime counting  --  connection to RH
  % -----------------------------------------------------------------------
  %
  % PRIME NUMBER THEOREM (proved 1896):
  %   pi(x) ~ x / ln(x)
  %
  % If RH is true, Riemann's explicit formula gives the tightest bound:
  %   pi(x) = Li(x) + O( sqrt(x) * ln(x) )
  % where Li(x) = integral_2^x dt/ln(t)  (logarithmic integral).
  %
  % A false RH would permit a much larger error, meaning primes could
  % be far more irregularly distributed than believed.

  x_max = 200;
  primes_list = prime_sieve(x_max);
  x     = 1:x_max;
  pi_x  = arrayfun(@(xi) sum(primes_list <= xi), x);
  li_x  = arrayfun(@(xi) quadl(@(tt) 1 ./ log(tt), 2, xi), x(2:end));

  figure(3);
  plot(x, pi_x, 'b-', 'LineWidth', 1.2, 'DisplayName', '\pi(x) exact');
  hold on;
  plot(x(2:end), li_x,              'r--', 'LineWidth', 1.2, ...
       'DisplayName', 'Li(x)');
  plot(x(2:end), x(2:end) ./ log(x(2:end)), 'g:', 'LineWidth', 1.2, ...
       'DisplayName', 'x / ln(x)');
  xlabel('x');
  ylabel('Prime count');
  title({'Prime Counting Function \pi(x)', ...
         'RH implies Li(x) is the best possible approximation'});
  legend('Location', 'northwest');
  grid on;
  hold off;

  % -----------------------------------------------------------------------
  % SIGNIFICANCE & STATUS
  % -----------------------------------------------------------------------
  %
  % IF PROVEN TRUE:
  %   1. Primes are distributed as regularly as possible.
  %   2. Validates security proofs for primality tests (e.g. Miller-Rabin).
  %   3. Generalised RH has sweeping consequences in algebraic number theory.
  %   4. Zero spacings match GUE random-matrix statistics, linking RH to
  %      quantum chaos.
  %
  % IF PROVEN FALSE:
  %   Parts of analytic number theory and cryptographic security analysis
  %   would require rebuilding.
  %
  % CURRENT STATUS (2025):
  %   - Still UNPROVEN.
  %   - Clay Millennium Prize Problem -- USD $1,000,000 reward.
  %   - Verified numerically for the first ~10^13 non-trivial zeros.
  %   - No counterexample has ever been found.

  disp('Riemann Hypothesis exploration complete. See figures 1-3.');

end % riemann_hypothesis

% =========================================================================
% SUBFUNCTIONS
% =========================================================================

function z = zeta_via_eta(s, N)
  % Approximate zeta(s) via the Dirichlet eta function.
  % Works inside the critical strip  0 < Re(s) < 1.
  %   eta(s) = sum_{n=1}^{N} (-1)^{n+1} / n^s
  %   zeta(s) = eta(s) / (1 - 2^{1-s})
  n   = 1:N;
  eta = sum( ((-1) .^ (n + 1)) ./ (n .^ s) );
  z   = eta / (1 - 2^(1 - s));
end

function z = zeta_approx(s, N)
  % Approximate zeta(s) via the Dirichlet series.
  % Converges only for  Re(s) > 1.
  n = 1:N;
  z = sum(1 ./ (n .^ s));
end

function primes_list = prime_sieve(n)
  % Sieve of Eratosthenes: return all primes up to n.
  is_prime    = true(1, n);
  is_prime(1) = false;
  for k = 2:floor(sqrt(n))
    if is_prime(k)
      is_prime(k*k : k : n) = false;
    end
  end
  primes_list = find(is_prime);
end
