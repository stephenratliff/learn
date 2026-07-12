function crypto_gauss()
% CRYPTO_GAUSS Gauss totient, modular arithmetic foundation of RSA & DH
% Totient
phi=@(n) sum(gcd(1:n,n)==1);
fprintf('phi(36)=%d, formula 36*(1-1/2)*(1-1/3)=%d\n',phi(36),36*(1-1/2)*(1-1/3));
% Extended Euclid for modinv
function inv=modinv(a,m)
 [g,x,~]=gcd(a,m); if g~=1, inv=NaN; return; end; inv=mod(x,m);
end
% Fast modpow
function r=modpow(a,e,m), r=1; a=mod(a,m); while e>0, if mod(e,2)==1, r=mod(r*a,m); end; a=mod(a*a,m); e=floor(e/2); end; end

% RSA toy
p=61; q=53; N=p*q; ph=(p-1)*(q-1); e=17; d=modinv(e,ph);
M=42; C=modpow(M,e,N); M2=modpow(C,d,N);
fprintf('RSA p=%d q=%d N=%d phi=%d e=%d d=%d\n',p,q,N,ph,e,d);
fprintf('M=%d -> C=%d -> M2=%d (decrypt)\n',M,C,M2);

% Diffie-Hellman toy
g=5; pp=23; a=6; b=15; A=modpow(g,a,pp); B=modpow(g,b,pp);
s1=modpow(B,a,pp); s2=modpow(A,b,pp);
fprintf('DH g=%d p=%d A=g^a=%d B=g^b=%d shared=%d==%d\n',g,pp,A,B,s1,s2);
end
