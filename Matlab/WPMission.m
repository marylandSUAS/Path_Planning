function [final_wps] = WPMission(wps,bounds,obstacles)
%     temp = wps
    
    
%     bounds = [-250 250;-250 250];
%     safety_radius = 20;
% 
%     turning_radius = 65;
% 
%     hold on
%     collision_overshoot = [];
%     for i = 2:length(wps)-1
%         
%         theta1 = bound_rad(atan2((wps(i,2)-wps(i-1,2)),(wps(i,1)-wps(i-1,1))));
%         theta2 = bound_rad(atan2((wps(i+1,2)-wps(i,2)),(wps(i+1,1)-wps(i,1))));
%         
%         dtheta = bound_rad(theta2-theta1);
%         
%         turn_pnt = wps(i,:) + turning_radius*[cos(theta1+sign(dtheta)*pi/2) sin(theta1+sign(dtheta)*pi/2) 0];
% 
%         t = theta1-sign(dtheta)*pi/2:sign(dtheta)*.1:theta1-sign(dtheta)*pi/2 + dtheta*2;
%     %     b = sqrt((2*turning_radius)^2+(turning_radius-turning_radius*sin(pi/2-dtheta))^2)
% 
%         for k = 1:size(obstacles,1)
%             dist = hypot(turn_pnt(1)-obstacles(k,1),turn_pnt(2)-obstacles(k,2));
%             if (dist < obstacles(k,3)+turning_radius)
%                 thetaO = bound_rad(atan2((obstacles(k,2)-turn_pnt(2)),(obstacles(k,1)-turn_pnt(1))));
% 
%                 theta_bounds = [t(1) t(end)];
% 
%                 if (sign(dtheta) > 0)
%                     if (is_bounded(theta_bounds(1),theta_bounds(2),thetaO)) 
%                         collision_overshoot  = [collision_overshoot; i k];
%                         scatter(turn_pnt(1)+turning_radius*cos(thetaO),turn_pnt(2)+turning_radius*sin(thetaO),'r','filled')
%                     end
%                 else
%                     if (is_bounded(theta_bounds(2),theta_bounds(1),thetaO))
%                         collision_overshoot  = [collision_overshoot; i k];
%                         scatter(turn_pnt(1)+turning_radius*cos(thetaO),turn_pnt(2)+turning_radius*sin(thetaO),'r','filled')
%                     end
%                 end
% 
% 
%             end
%         end
%         scatter(turn_pnt(1),turn_pnt(2),'g')
%         x = turn_pnt(1)+turning_radius*cos(t);
%         y = turn_pnt(2)+turning_radius*sin(t);
%         plot(x,y,'g')
% 
%     end
% 
%     collision_path = [];
%     for i = 2:length(wps)
%         for k = 1:size(obstacles,1)
%             [pnt,t] = dist_line(wps(i-1,:),wps(i,:),obstacles(k,1:2));
%             if (norm(pnt(1:2)-obstacles(k,1:2)) < obstacles(k,3) && t > 0 && t < 1 && pnt(3) < obstacles(k,3))
%                 collision_path  = [collision_path; i-1 k];
%                 scatter(pnt(1),pnt(2),'r','filled')
%             end        
%         end
%     end


%     collision_overshoot
%     collision_path

    total_wps = wps(1,:);
    
    
    for k = 1:length(wps)-1
        
        temp_points = [];

        
        cmd = 'v';
        while cmd ~= 'n'
            en = min(k+2,length(wps));
            bg = max(1,k-1);
    %         plot the next two
            hold off
            plot(wps(bg:en,1),wps(bg:en,2),'b')
            hold on
            scatter(wps(bg:en,1),wps(bg:en,2),'b')
            scatter(wps(k,1),wps(k,2),'g','filled')
            
            if ~isempty(temp_points)
                scatter(temp_points(:,1),temp_points(:,2),'b')
                temp = [wps(k,1:3); temp_points; wps(k+1,1:3)];
                plot(temp(:,1),temp(:,2),'r')
            end
            
            midpoint = (wps(k,1:2)+wps(k+1,1:2))/2;
            maxdist = norm(wps(k,1:2)-wps(k+1,1:2));
            t = -.1:.1:2*pi;
            for i = 1:size(obstacles,1)
%                 if (norm(midpoint-obstacles(i,1:2)) < maxdist)
                x = obstacles(i,1)+obstacles(i,3)*cos(t);
                y = obstacles(i,2)+obstacles(i,3)*sin(t);
                plot(x,y,'r')
                scatter(obstacles(i,1),obstacles(i,2),'r')
%                 end
            end
            axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])

        
            
            
%             cmd = input('6:next, 5:add,');
            w = waitforbuttonpress;
            cmd = get(gcf, 'CurrentCharacter');
            
            if cmd == 'a'
                add_point = ginput(1);
                height_mean = norm(add_point-wps(k,1:2))/(norm(add_point-wps(k,1:2))+norm(wps(k+1,1:2)-add_point));
                temp_points = [temp_points; add_point wps(k,3)+(wps(k+1,3)-wps(k,3))*height_mean];
            end
            
            if cmd == 'r'
                temp_points = [];
            end
            
            if cmd == 'n'
                total_wps = [total_wps; temp_points; wps(k+1,:)];
            end
            
        end
        
    end
    final_wps = total_wps;
end

