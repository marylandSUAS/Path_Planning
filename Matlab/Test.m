% clear all
% temp = mission(' ');
% temp.visualize()
clc

% wps = temp.launch_wps(2,:)
% wps = [wps; temp.waypoints]

bounds = [-250 250;-250 250];
safety_radius = 10;
% wps = [-500 500;
%     600 500;
%     500 -500;
%     -500 -500;
%     -500 500];
% 
% obstacles = [0 0 100;
%             520 0 50;
%             460 -530 20];
renew = 1;
if (renew)
    obstacles = [];
    for k = 1:10
        obstacles = [obstacles; bounds(1,1) + (bounds(1,2)-bounds(1,1))*rand() bounds(2,1) + (bounds(2,2)-bounds(2,1))*rand() 20+80*rand()];
    end
    
    wps = [];
    while(size(wps,1) < 5)
        temp_point = [bounds(1,1) + (bounds(1,2)-bounds(1,1))*rand() bounds(2,1) + (bounds(2,2)-bounds(2,1))*rand()];
        add = 1;
        for k = 1:size(obstacles,1)
            if hypot(temp_point(1)-obstacles(k,1),temp_point(2)-obstacles(k,2)) < obstacles(k,3)
                add = 0;
            end
        end
        if add
            wps = [wps; temp_point];
        end
    end
end

turning_radius = 35;
hold on
collision_overshoot = [];
for i = 2:length(wps)-1
    theta1 = bound_rad(atan2((wps(i,2)-wps(i-1,2)),(wps(i,1)-wps(i-1,1))));
    theta2 = bound_rad(atan2((wps(i+1,2)-wps(i,2)),(wps(i+1,1)-wps(i,1))));
    
    dtheta = bound_rad(theta2-theta1);
    
    turn_pnt = wps(i,:) + turning_radius*[cos(theta1+sign(dtheta)*pi/2) sin(theta1+sign(dtheta)*pi/2)];
    
    t = theta1-sign(dtheta)*pi/2:sign(dtheta)*.1:theta1-sign(dtheta)*pi/2 + dtheta*2;
%     b = sqrt((2*turning_radius)^2+(turning_radius-turning_radius*sin(pi/2-dtheta))^2)
    
    for k = 1:size(obstacles,1)
        dist = hypot(turn_pnt(1)-obstacles(k,1),turn_pnt(2)-obstacles(k,2));
        if (dist < obstacles(k,3)+turning_radius)
            thetaO = bound_rad(atan2((obstacles(k,2)-turn_pnt(2)),(obstacles(k,1)-turn_pnt(1))));
            
            theta_bounds = [t(1) t(end)];
            
            if (sign(dtheta) > 0)
                if (is_bounded(theta_bounds(1),theta_bounds(2),thetaO)) 
                    collision_overshoot  = [collision_overshoot; i k];
                    scatter(turn_pnt(1)+turning_radius*cos(thetaO),turn_pnt(2)+turning_radius*sin(thetaO),'r','filled')
                end
            else
                if (is_bounded(theta_bounds(2),theta_bounds(1),thetaO))
                    collision_overshoot  = [collision_overshoot; i k];
                    scatter(turn_pnt(1)+turning_radius*cos(thetaO),turn_pnt(2)+turning_radius*sin(thetaO),'r','filled')
                end
            end
            
            
        end
    end
    scatter(turn_pnt(1),turn_pnt(2),'g')
    x = turn_pnt(1)+turning_radius*cos(t);
    y = turn_pnt(2)+turning_radius*sin(t);
    plot(x,y,'g')
    
end

collision_path = [];
for i = 2:length(wps)
    for k = 1:size(obstacles,1)
        [pnt,t] = dist_line(wps(i-1,:),wps(i,:),obstacles(k,1:2));
        if (norm(pnt-obstacles(k,1:2)) < obstacles(k,3) && t > 0 && t < 1)
            collision_path  = [collision_path; i-1 k];
            scatter(pnt(1),pnt(2),'r','filled')
        end        
    end
end


collision_overshoot
collision_path


for k = 1:length(collision_overshoot)
    
end

for l = 1:length(collision_path)
    
end















plot(wps(:,1),wps(:,2),'b')
scatter(wps(:,1),wps(:,2),'b')
scatter(wps(1,1),wps(1,2),'g','filled')
t = -.1:.1:2*pi;
for i = 1:size(obstacles,1)
    x = obstacles(i,1)+obstacles(i,3)*cos(t);
    y = obstacles(i,2)+obstacles(i,3)*sin(t);
    plot(x,y,'r')
    scatter(obstacles(i,1),obstacles(i,2),'r')
end
% axis([400 550 -580 -460])

