function best_response_plot(A,B)
% BEST_RESPONSE_PLOT Plot expected payoffs vs mixed strategies
p=linspace(0,1,400); q=linspace(0,1,400);
% Row payoff given q: U1 = q*A11+(1-q)*A12 for Up, etc.
A11=A(1,1);A12=A(1,2);A21=A(2,1);A22=A(2,2);
Uup = q*A11+(1-q)*A12; Udown = q*A21+(1-q)*A22;
figure; plot(q,Uup,q,Udown); legend('Up','Down'); grid on;
title('Row best response vs q'); xlabel('q=Prob Col Left');
end
