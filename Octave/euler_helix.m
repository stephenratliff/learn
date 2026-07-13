% ── 3D Helix Visualization of e^{iθ} ─────────────────────────────────────
theta = linspace(0, 6*pi, 2000);
z = exp(1i * theta);
x = real(z);    % cos(θ)
y = imag(z);    % sin(θ)

figure('Name', 'e^{itheta} as a 3D Helix');
subplot(1,2,1);
  plot3(x, y, theta, 'b-', 'LineWidth', 2); hold on;
  % Project onto Re-Im plane (unit circle)
  plot3(x, y, zeros(size(theta)), 'k:', 'LineWidth', 1);
  % Project onto Re-θ plane (cosine wave)
  plot3(x, -ones(size(theta)), theta, 'r:', 'LineWidth', 1);
  % Project onto Im-θ plane (sine wave)
  plot3(ones(size(theta)), y, theta, 'g:', 'LineWidth', 1);
  xlabel('Re(e^{i	heta}) = cos	heta');
  ylabel('Im(e^{i	heta}) = sin	heta');
  zlabel('	heta (radians)');
  title('3D helix: e^{i	heta} with 3 projections');
  legend({'helix','unit circle (Re-Im)','cosine (Re-	heta)','sine (Im-	heta)'});
  grid on; view(35, 25);

subplot(1,2,2);
  % Growing spiral: r(θ) * e^{iθ} where r(θ) = e^{θ/10}
  r = exp(theta/10);           % growing amplitude
  z_spiral = r .* exp(1i*theta);
  plot3(real(z_spiral), imag(z_spiral), theta, 'm-', 'LineWidth', 2);
  xlabel('Re'); ylabel('Im'); zlabel('	heta');
  title('Growing spiral: e^{	heta/10} \cdot e^{i	heta}');
  grid on; view(35, 25);

sgtitle('The Complex Exponential in 3D');
