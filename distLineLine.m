wp1 = [0 0 0];
wp2 = [10 -5 0];

ob1 = [5 5 -5];
ob2 = [5 5 5];

radius = 2;

while(sqrt((ob2(1)-ob1(1))^2+(ob2(2)-ob1(2))^2+(ob2(3)-ob1(3))^2) > radius/1.5)
    ob15 = (ob1+ob2)/2;
    
    d1 = DistanceLineToPoint(wp1,wp2,ob1);
    d2 = DistanceLineToPoint(wp1,wp2,ob15);
    d3 = DistanceLineToPoint(wp1,wp2,ob2);

    if (d2 < d3)
        ob2 = ob15;
    else
        ob1 = ob15;
    end
    
end

finalDist = DistanceLineToPoint(wp1,wp2,ob2);
if (DistanceLineToPoint(wp1,wp2,ob1) < finalDist)
    finalDist = DistanceLineToPoint(wp1,wp2,ob1);
end

finalDist

% 
% co = [5 0 0];
% cw = [5 5 0];

% distance = sqrt((co(1)-cw(1))^2+(co(2)-cw(2))^2+(co(3)-cw(3))^2)

hold on
% plot3([co(1) cw(1)],[co(2) cw(2)],[co(3) cw(3)],'g')
% scatter3([co(1) cw(1)],[co(2) cw(2)],[co(3) cw(3)],'g')

plot3([ob1(1) ob2(1)],[ob1(2) ob2(2)],[ob1(3) ob2(3)],'r')
scatter3([ob1(1) ob2(1)],[ob1(2) ob2(2)],[ob1(3) ob2(3)],'r')
plot3([wp1(1) wp2(1)],[wp1(2) wp2(2)],[wp1(3) wp2(3)],'b')
scatter3([wp1(1) wp2(1)],[wp1(2) wp2(2)],[wp1(3) wp2(3)],'b')
view(-25,25)