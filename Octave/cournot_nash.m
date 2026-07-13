function [q1,q2]=cournot_nash(a,b,c1,c2)
% COURNOT_NASH Duopoly Nash quantities
% q1=(a-c1)/(2b)-q2/2, q2=(a-c2)/(2b)-q1/2
if nargin<4, a=20;b=1;c1=2;c2=3; end
A=[2*b b; b 2*b]; rhs=[a-c1; a-c2]; q=A\rhs; q1=q(1); q2=q(2);
p=a-b*(q1+q2); pi1=(p-c1)*q1; pi2=(p-c2)*q2;
fprintf('q1*=%.3f q2*=%.3f p=%.3f pi1=%.2f pi2=%.2f\n',q1,q2,p,pi1,pi2);
end
