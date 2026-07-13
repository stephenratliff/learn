% crypto_gauss.m — totient, modular, RSA, DH — GNU Octave
function g = egcd(a,b)
  if b==0, g=a; else g=egcd(b, mod(a,b)); end
end
function [g,x,y]=extgcd(a,b)
  if b==0, g=a; x=1; y=0; return; end
  [g,x1,y1]=extgcd(b, mod(a,b));
  x=y1; y=x1 - floor(a/b)*y1;
end
function inv=modinv(a,m)
  [g,x,~]=extgcd(a,m); if g!=1, error("no inv"); end
  inv=mod(x,m);
end
function r=modpow(a,e,m)
  r=1; a=mod(a,m);
  while e>0
    if mod(e,2)==1, r=mod(r*a,m); end
    a=mod(a*a,m); e=floor(e/2);
  end
end
function p=phi_n(n)
  p=n; tmp=n;
  for q=2:sqrt(tmp)
    if mod(tmp,q)==0
      while mod(tmp,q)==0, tmp/=q; end
      p=p*(1-1/q);
    end
  end
  if tmp>1, p=p*(1-1/tmp); end
end

% RSA toy
p=61; q=53; N=p*q; ph=(p-1)*(q-1);
e=17; d=modinv(e,ph);
M=42; C=modpow(M,e,N); M2=modpow(C,d,N);
printf("N=%d phi=%d e=%d d=%d M=%d C=%d dec=%d\n",N,ph,e,d,M,C,M2);

% Diffie-Hellman toy
g=5; P=23; a=6; b=15;
A=modpow(g,a,P); B=modpow(g,b,P);
s1=modpow(B,a,P); s2=modpow(A,b,P);
printf("DH shared %d == %d\n",s1,s2);

