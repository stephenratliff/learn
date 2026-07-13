% Königsberg as an adjacency matrix (multigraph: entries count bridges)
% order: N (north bank), I (island), S (south bank), E (east spit)
A = [0 2 0 1;
     2 0 2 1;
     0 2 0 1;
     1 1 1 0];

deg = sum(A, 2).'            % degree of each landmass -> [3 5 3 3]
odd_vertices = sum(mod(deg, 2) == 1)

if odd_vertices == 0
  disp('Euler CIRCUIT exists (return to start).')
elseif odd_vertices == 2
  disp('Euler PATH exists (start and end differ).')
else
  disp('No Euler path: Königsberg walk is impossible.')
end

% Repair the city: remove one bridge between N and I ...
B = A;  B(1,2) = 1;  B(2,1) = 1;
degB = sum(B,2).'
printf('odd vertices after demolition: %d -> walk possible!\n', ...
       sum(mod(degB,2)==1));
