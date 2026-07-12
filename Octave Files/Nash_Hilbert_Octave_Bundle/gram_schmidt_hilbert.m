function Q=gram_schmidt_hilbert(A)
% GRAM_SCHMIDT_HILBERT Modified Gram-Schmidt, orthonormal basis of Hilbert space R^n
% A m x n, returns Q with Q'*Q ~ I
[m,n]=size(A); Q=zeros(m,n); R=zeros(n,n);
for j=1:n
 v=A(:,j);
 for i=1:j-1, R(i,j)=Q(:,i)'*v; v=v-R(i,j)*Q(:,i); end
 R(j,j)=norm(v); Q(:,j)=v/R(j,j);
end
fprintf('orth error ||Q''*Q-I||=%.2e\n',norm(Q'*Q-eye(n)));
end
