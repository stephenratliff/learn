function s=nash_bargaining(S,d)
% NASH_BARGAINING Maximize (u1-d1)*(u2-d2) over convex polygon S
% S Nx2 vertices, d 1x2 disagreement
if nargin<2, S=[0 0;10 0;7 7;0 10]; d=[1 1]; end
obj=@(u) -sum(log(max(u-d,1e-9)));
pen=@(u) obj(u) + 1e5*(~inpolygon(u(1),u(2),S(:,1),S(:,2)));
u0=mean(S,1); s=fminsearch(pen,u0);
fprintf('Nash bargaining solution s=(%.4f,%.4f)\n',s(1),s(2));
plot([S(:,1);S(1,1)],[S(:,2);S(1,2)],'k-'); hold on;
plot(d(1),d(2),'ro','MarkerFaceColor','r'); plot(s(1),s(2),'go','MarkerFaceColor','g'); hold off;
end
