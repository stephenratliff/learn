% ── Trig Identities via Euler's Formula ──────────────────────────────────
% cos(α+β) = cos α cos β - sin α sin β
% sin(α+β) = sin α cos β + cos α sin β
% Proof: e^{i(α+β)} = e^{iα} · e^{iβ}

alpha = 0.7; beta = 1.2;

lhs = exp(1i*(alpha+beta));
rhs = exp(1i*alpha) * exp(1i*beta);
fprintf('e^{i(a+b)} = %.6f %+.6fi\n', real(lhs), imag(lhs));
fprintf('e^{ia}*e^{ib}= %.6f %+.6fi  |error|=%.2e\n\n', real(rhs), imag(rhs), abs(lhs-rhs));

% Expanding: Real part gives cos addition, imaginary gives sin addition
cos_add_euler  = real(exp(1i*alpha) * exp(1i*beta));
cos_add_trig   = cos(alpha)*cos(beta) - sin(alpha)*sin(beta);
sin_add_euler  = imag(exp(1i*alpha) * exp(1i*beta));
sin_add_trig   = sin(alpha)*cos(beta) + cos(alpha)*sin(beta);
fprintf('cos(a+b): Euler=%.8f  Trig=%.8f\n', cos_add_euler, cos_add_trig);
fprintf('sin(a+b): Euler=%.8f  Trig=%.8f\n\n', sin_add_euler, sin_add_trig);

% ── Double angle formulas ─────────────────────────────────────────────────
% (e^{iθ})^2 = e^{2iθ}  →  expand (cosθ + i sinθ)^2
theta = 0.9;
z2 = (cos(theta) + 1i*sin(theta))^2;
fprintf('cos(2θ): Euler=%.8f  Direct=%.8f\n', real(z2), cos(2*theta));
fprintf('sin(2θ): Euler=%.8f  Direct=%.8f\n\n', imag(z2), sin(2*theta));

% ── Product-to-sum identities ─────────────────────────────────────────────
% cos α cos β = (1/2)[cos(α-β) + cos(α+β)]
% Proof: Re(e^{iα}) * Re(e^{iβ}) = (1/2)Re(e^{i(α-β)} + e^{i(α+β)})
lhs_prod = cos(alpha) * cos(beta);
rhs_prod = 0.5 * (cos(alpha-beta) + cos(alpha+beta));
fprintf('cos(a)cos(b):  Direct=%.8f  Product-to-sum=%.8f\n', lhs_prod, rhs_prod);

% ── Plot several trig identities verified numerically ─────────────────────
t = linspace(0, 4*pi, 1000);
figure('Name', 'Trig Identities via Euler');
subplot(2,1,1);
  euler_expr = real(exp(2i*t));            % Re(e^{2it}) = cos(2t)
  trig_expr  = cos(t).^2 - sin(t).^2;    % classical double angle
  plot(t, euler_expr, 'b-', t, trig_expr, 'r--', 'LineWidth', 2);
  legend({'Re(e^{2it})', 'cos^2(t)-sin^2(t)'}); grid on;
  title('Double angle: cos(2t) = cos^2(t) - sin^2(t)');
subplot(2,1,2);
  euler_expr2 = imag(exp(2i*t));     % Im(e^{2it}) = sin(2t)
  trig_expr2  = 2*cos(t).*sin(t);    % classical form
  plot(t, euler_expr2, 'b-', t, trig_expr2, 'r--', 'LineWidth', 2);
  legend({'Im(e^{2it})', '2cos(t)sin(t)'}); grid on;
  title('Double angle: sin(2t) = 2cos(t)sin(t)');
