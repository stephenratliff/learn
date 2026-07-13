% ── Euler's Identity: e^(i*pi) + 1 = 0 ──────────────────────────────────
% Compute e^(i*pi) using Octave's built-in exp() and the imaginary unit 1i

result = exp(1i * pi);   % complex exponential: should equal -1

fprintf('e^(i*pi) = %.15f + %.15fi\n', real(result), imag(result));
fprintf('e^(i*pi) + 1 = %.2e  (machine epsilon = %.2e)\n', ...
        abs(result + 1), eps);

% ── Direct component check ────────────────────────────────────────────────
theta = pi;
using_formula = cos(theta) + 1i * sin(theta);   % Euler's formula
using_exp     = exp(1i * theta);                 % exponential form

fprintf('\nEuler formula result:  %+.10f %+.10fi\n', ...
        real(using_formula), imag(using_formula));
fprintf('exp(i*theta) result:   %+.10f %+.10fi\n', ...
        real(using_exp), imag(using_exp));
fprintf('Difference: %.2e\n', abs(using_formula - using_exp));

% ── Explore e^(i*theta) for several values ────────────────────────────────
fprintf('\n  θ/π     |  cos(θ)     |  sin(θ)     |  e^(iθ)\n');
fprintf('%s\n', repmat('-', 1, 55));
for k = 0:8
  t = k * pi / 4;
  z = exp(1i * t);
  fprintf('  %4.2f    |  %+.6f  |  %+.6f  |  %+.4f%+.4fi\n', ...
          k/4, cos(t), sin(t), real(z), imag(z));
end

% ── Unit Circle and Wave Projections ─────────────────────────────────────
theta = linspace(0, 2*pi, 360);
z     = exp(1i * theta);          % unit circle as complex exponential
x     = real(z);                   % cos(θ)
y     = imag(z);                   % sin(θ)

figure('Name', 'Euler Formula: Unit Circle', 'Color', 'w');
subplot(1, 3, 1);
  plot(x, y, 'b-', 'LineWidth', 2);  hold on;
  plot(1, 0, 'ro', 0, 1, 'go', -1, 0, 'ko', 0, -1, 'mo', 'MarkerSize', 8);
  axis equal; grid on; axis([-1.4 1.4 -1.4 1.4]);
  title('Unit Circle: e^{i	heta}');
  xlabel('Re(z) = cos	heta'); ylabel('Im(z) = sin	heta');
  legend({'e^{i	heta}','	heta=0','	heta=\pi/2','	heta=\pi','	heta=3\pi/2'}, ...
         'Location', 'SouthEast');

subplot(1, 3, 2);
  plot(theta/pi, x, 'b-', 'LineWidth', 2);
  grid on; xlabel('	heta / \pi'); ylabel('cos	heta = Re(e^{i	heta})');
  title('Real Part: Cosine Wave');
  xticks(0:0.5:2); xticklabels({'0','\pi/2','\pi','3\pi/2','2\pi'});

subplot(1, 3, 3);
  plot(theta/pi, y, 'r-', 'LineWidth', 2);
  grid on; xlabel('	heta / \pi'); ylabel('sin	heta = Im(e^{i	heta})');
  title('Imaginary Part: Sine Wave');
  xticks(0:0.5:2); xticklabels({'0','\pi/2','\pi','3\pi/2','2\pi'});

sgtitle('Euler\'s Formula: e^{i	heta} = cos	heta + i sin	heta', 'FontSize', 14);
