function [pure,mix]=nash_2x2(A,B)
% NASH_2X2 Pure and mixed Nash for 2x2 bimatrix game
% A,B 2x2 payoffs for Row, Column. pure = list [i j], mix.p,q
pure=[];
for i=1:2
 for j=1:2
  if A(i,j)==max(A(:,j)) && B(i,j)==max(B(i,:))
    pure=[pure; i j];
  end
 end
end
a=A(1,1); b=A(1,2); c=A(2,1); d=A(2,2);
e=B(1,1); f=B(1,2); g=B(2,1); h=B(2,2);
denA=a-b-c+d; denB=e-f-g+h;
if abs(denA)>1e-12, p=(d-b)/denA; else p=0.5; end
if abs(denB)>1e-12, q=(h-f)/denB; else q=0.5; end
mix.p=min(max(p,0),1); mix.q=min(max(q,0),1);
fprintf('pure: '); disp(pure); fprintf('mixed p=%.3f q=%.3f\n',mix.p,mix.q);
end
