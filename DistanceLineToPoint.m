function dist = DistanceLineToPoint(st,gl,ob)
% st = [0 0 0];
% gl = [100 0 0];
% ob = [150 50 0];
    lin = [gl(1)-st(1) gl(2)-st(2) gl(3)-st(3)];
    ln = lin/sqrt(lin(1)^2+lin(2)^2+lin(3)^2);
    t = (((ob(1)-st(1))*ln(1))+((ob(2)-st(2))*ln(2))+(ln(3)*(ob(3)-st(3))))/(ln(1)^2+ln(2)^2+ln(3)^2);
    if(t<0)
        t=0;4
    elseif(t>sqrt((st(1)-gl(1))^2+(st(2)-gl(2))^2+(st(3)-gl(3))^2))
        t = sqrt((gl(1)-st(1))^2+(gl(2)-st(2))^2+(gl(3)-st(3))^2);
    end
    cp = [st(1)+ln(1)*t st(2)+ln(2)*t st(3)+ln(3)*t];
    d = sqrt((ob(1)-cp(1))^2+(ob(2)-cp(2))^2+(ob(3)-cp(3))^2);
dist = d;
% hold on
% 
% plot3([st(1) gl(1)],[st(2) gl(2)],[st(3) gl(3)])
% scatter3(ob(1),ob(2),ob(3))
% plot3([cp(1) ob(1)],[cp(2) ob(2)],[cp(3) ob(3)])
% clear all