% Fit a parabola through three observed points -------------------
% (the shape of every projectile, and of Ceres' apparent path)
P = [1 4;  2 3;  4 7];            % (x, y) observations
A = [P(:,1).^2, P(:,1), ones(3,1)];
b = P(:,2);

coef = A \ b                      % Gaussian elimination inside

[L, U, Pm] = lu(A);               % see the elimination explicitly
L, U                              % A = P'LU: the row-reduction record

xs = linspace(0, 5, 100);
plot(P(:,1), P(:,2), 'o', xs, polyval(coef, xs), '-');
title('Three points, one parabola: A\\b');
% Historical footnote: "Gaussian" elimination appears in the
% Chinese "Nine Chapters" ~2000 years earlier; Gauss systematized
% it for least-squares normal equations, and the name stuck.
