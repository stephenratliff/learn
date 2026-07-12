function zeta_basel()
% ZETA_BASEL Basel problem, Euler product, zeta regularization -> strings & Casimir
N=1e6; basel=sum(1./(1:5000).^2); err=pi^2/6-basel;
fprintf('Basel partial N=5000 sum=%.10f pi^2/6=%.10f err=%.2e\n',basel,pi^2/6,err);

% Euler product for zeta(2)
pr=primes(200); prod_est=prod(1./(1-pr.^-2));
fprintf('Euler product over primes <=200 for zeta(2)=%.8f true=%.8f\n',prod_est,pi^2/6);

% Zeta values used in physics
fprintf('zeta(2)=pi^2/6=%.8f, zeta(4)=pi^4/90=%.8f\n',pi^2/6,pi^4/90);
fprintf('zeta(-1)=-1/12=%.8f regularization of 1+2+3+...\n',-1/12);
fprintf('zeta(-3)=1/120=%.8f appears in Casimir and bosonic string D=26\n',1/120);

% Casimir force ~ -pi^2/240 * hbar c / d^4 from zeta(4)
d=1e-6; hbar=1.0545718e-34; c=3e8;
F=-pi^2/240*hbar*c/d^4; fprintf('Casimir pressure at d=1um ~%.2e Pa\n',F);

% Prime number theorem connection
x=1000; pi_x=length(primes(x)); approx=x/log(x);
fprintf('pi(%d)=%d approx x/log x=%.1f\n',x,pi_x,approx);
end
