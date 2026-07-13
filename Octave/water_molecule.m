% water_molecule.m
% GNU Octave demonstration of H2O as a covalent molecule
% Shows 3D geometry, bond angle ~104.5°, and animates the three normal modes
%
% Run: water_molecule

function water_molecule()
  printf('Water molecule H2O - covalent bonding demo\n');

  % ---- physical constants (in Angstroms) ----
  rOH = 0.9572;          % O-H bond length
  theta = 104.52 * pi/180; % H-O-H angle

  % Oxygen at origin
  O = [0, 0, 0];
  % Hydrogens in xz plane
  H1 = [ rOH*sin(theta/2), 0, rOH*cos(theta/2) ];
  H2 = [-rOH*sin(theta/2), 0, rOH*cos(theta/2) ];

  % ---- figure setup ----
  figure(1); clf; hold on; axis equal; grid on; view(35,20);
  xlabel('x (Å)'); ylabel('y (Å)'); zlabel('z (Å)');
  title('H2O - covalent bonds, lone pairs, and vibrations');

  % draw static molecule first
  draw_molecule(O, H1, H2);

  % ---- animate normal modes ----
  modes = {'symmetric stretch','bend','asymmetric stretch'};
  for m = 1:3
    printf('Animating %s...\n', modes{m});
    for t = linspace(0,2*pi,120)
      clf; hold on; axis equal; grid on; view(35,20);
      % small displacements
      dr = 0.08 * sin(t);
      dtheta = 5 * pi/180 * sin(t);

      if m==1 % symmetric stretch: both bonds lengthen together
        r1 = rOH + dr; r2 = rOH + dr; th = theta;
      elseif m==2 % bend: angle opens/closes
        r1 = rOH; r2 = rOH; th = theta + dtheta;
      else % asymmetric: one stretches, other compresses
        r1 = rOH + dr; r2 = rOH - dr; th = theta;
      endif

      H1t = [ r1*sin(th/2), 0, r1*cos(th/2) ];
      H2t = [-r2*sin(th/2), 0, r2*cos(th/2) ];
      draw_molecule(O, H1t, H2t);
      title(sprintf('H2O - %s', modes{m}));
      drawnow;
      pause(0.02);
    endfor
  endfor
endfunction

function draw_molecule(O, H1, H2)
  % draw atoms as spheres
  [sx,sy,sz] = sphere(20);
  % Oxygen (red, larger)
  surf(O(1)+0.4*sx, O(2)+0.4*sy, O(3)+0.4*sz, 'FaceColor','r','EdgeColor','none');
  % Hydrogens (white, smaller)
  surf(H1(1)+0.2*sx, H1(2)+0.2*sy, H1(3)+0.2*sz, 'FaceColor','w','EdgeColor','k');
  surf(H2(1)+0.2*sx, H2(2)+0.2*sy, H2(3)+0.2*sz, 'FaceColor','w','EdgeColor','k');

  % draw bonds as thick lines (covalent shared electrons)
  plot3([O(1) H1(1)],[O(2) H1(2)],[O(3) H1(3)],'k','linewidth',3);
  plot3([O(1) H2(1)],[O(2) H2(2)],[O(3) H2(3)],'k','linewidth',3);

  % draw lone pairs as translucent lobes (approximate sp3)
  lp1 = [0, 0.3, -0.3];
  lp2 = [0,-0.3, -0.3];
  surf(lp1(1)+0.25*sx, lp1(2)+0.25*sy, lp1(3)+0.25*sz, ...
       'FaceColor','b','FaceAlpha',0.2,'EdgeColor','none');
  surf(lp2(1)+0.25*sx, lp2(2)+0.25*sy, lp2(3)+0.25*sz, ...
       'FaceColor','b','FaceAlpha',0.2,'EdgeColor','none');

  % labels
  text(O(1),O(2),O(3)+0.6,'O','fontsize',14,'horizontalalignment','center');
  text(H1(1),H1(2),H1(3)+0.4,'H','fontsize',12,'horizontalalignment','center');
  text(H2(1),H2(2),H2(3)+0.4,'H','fontsize',12,'horizontalalignment','center');

  % show bond angle
  mid = (H1+H2)/2;
  text(mid(1),mid(2),mid(3)-0.2,sprintf('%.1f°',104.5),'color',[0 0.5 0]);

  xlim([-1.5 1.5]); ylim([-1.5 1.5]); zlim([-1 1.5]);
  lighting gouraud; camlight headlight; material dull;
endfunction

% auto-run
if (nargin==0 && nargout==0 && strcmp(mfilename,'water_molecule'))
  water_molecule();
endif
