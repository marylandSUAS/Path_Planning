function value = bound_rad(angle)
    if angle > pi
        value = angle - 2*pi;
    elseif angle < -pi
        value = angle + 2*pi;
    else
        value = angle;
    end
    