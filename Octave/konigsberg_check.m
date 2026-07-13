% KONIGSBERG_CHECK Eulerian trail condition
% degrees for classic Konigsberg: 4 nodes, degrees [3 3 3 1]
deg = [3 3 3 1]; % change to test your graph
odd = sum(mod(deg,2)==1);
fprintf('degrees: '); disp(deg);
fprintf('odd-degree nodes = %d\n', odd);
if odd==0
  disp('Eulerian circuit exists (can start/end same node)');
elseif odd==2
  disp('Eulerian trail exists (must start at one odd node, end at other)');
else
  disp('No Eulerian trail - more than 2 odd nodes');
end
% V - E + F = 2 for connected planar graph
V=4; E=7; F=E-V+2; fprintf('Euler characteristic check: V-E+F=%d (should be 2)\n', V-E+F);
