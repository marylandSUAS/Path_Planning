function [closest_point_on_line,t] = dist_line(ln1,ln2,pnt)
v2 = ln2(1:2)-ln1(1:2);
v3 = ln2-ln1;
t = dot(v2,pnt-ln1(1:2))/(norm(v2)^2);

closest_point_on_line = ln1+t*v3;

end

