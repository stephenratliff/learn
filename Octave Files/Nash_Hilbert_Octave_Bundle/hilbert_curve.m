function [x,y]=hilbert_curve(order)
% HILBERT_CURVE Space-filling curve [0,1]->[0,1]^2
if nargin<1, order=5; end
  function [x,y]=rec(o,x0,y0,xi,xj,yi,yj)
    if o<=0, x=x0+(xi+yi)/2; y=y0+(xj+yj)/2; return; end
    [x1,y1]=rec(o-1,x0,y0,yi/2,yj/2,xi/2,xj/2);
    [x2,y2]=rec(o-1,x0+xi/2,y0+xj/2,xi/2,xj/2,yi/2,yj/2);
    [x3,y3]=rec(o-1,x0+xi/2+yi/2,y0+xj/2+yj/2,xi/2,xj/2,yi/2,yj/2);
    [x4,y4]=rec(o-1,x0+xi+yi/2,y0+xj+yj/2,-yi/2,-yj/2,-xi/2,-xj/2);
    x=[x1 x2 x3 x4]; y=[y1 y2 y3 y4];
  end
[x,y]=rec(order,0,0,1,0,0,1); plot(x,y,'-'); axis equal off;
fprintf('Hilbert order %d points %d\n',order,length(x));
end
