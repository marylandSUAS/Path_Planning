function bounded = is_bounded(theta1,theta2,angle)
theta2 = bound_rad(theta2);
theta1 = bound_rad(theta1);
angle = bound_rad(angle);
if (theta2 < theta1)
    theta2 = theta2+2*pi;
end
if (theta2 < theta1)
    theta2 = theta2+2*pi;
end
if angle > theta1 && angle < theta2
    bounded = 1;
else
    bounded = 0;
end
end

