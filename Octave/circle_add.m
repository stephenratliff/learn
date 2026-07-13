%% The Unit Circle as an Algebraic Group
%% Points: (cos θ, sin θ);  Law: add angles

function C = circle_add(A, B)
  % Group operation: (x1,y1) ★ (x2,y2) = (x1x2-y1y2, x1y2+x2y1)
  C = [A(1)*B(1) - A(2)*B(2),  A(1)*B(2) + A(2)*B(1)];
end
function A = circle_inv(P)
  A = [P(1), -P(2)];  % reflection in x-axis = angle negation
end
function R = circle_pow(P, n)
  % Scalar multiplication = repeated angle addition (n copies)
  R = [1,0];  % identity (angle 0)
  for k = 1:n
    R = circle_add(R, P);
  end
end

% Demo: A = 40°, B = 65° → A★B = 105°
A    = [cosd(40), sind(40)];
B    = [cosd(65), sind(65)];
C    = circle_add(A, B);
angle_C = atan2d(C(2), C(1));
printf('A★B angle = %.4f° (expect 105°)\n', angle_C);
printf('|A★B| = %.6f  (must be 1)\n', norm(C));

% n-th power = n·θ = angle multiplication
P  = [cosd(30), sind(30)];  % 30° point
P12= circle_pow(P, 12);      % 12×30° = 360° = identity
printf('12 × 30° point → (%.6f, %.6f)  ≈ (1,0)\n', P12(1), P12(2));

% The group axioms verified:
% Closure: |A★B| = 1  ✓
% Associativity: (A★B)★C = A★(B★C) ✓ (follows from angle addition)
% Identity: (1,0)  ✓
% Inverse: (x,-y)  ✓

