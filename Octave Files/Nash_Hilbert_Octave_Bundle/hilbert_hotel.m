function hilbert_hotel()
% HILBERT_HOTEL Bijections for infinite hotel
fprintf('n -> n+1 shift:\n'); disp([1:10; 2:11]');
fprintf('n -> 2n frees odds:\n'); disp([1:5; 2:2:10]');
cantor=@(p,q) (p+q)*(p+q+1)/2+q;
fprintf('Cantor pairing (2,3)=%d\n',cantor(2,3));
fprintf('|N x N| = |N| via dovetail enumeration\n');
end
