function final_wps = Landing(last_wp,miss,bounds,obstacles)
%LANDING takes in landing point(x/y) and last_wp(x/y)
    % returns landing waypoints(WP)
    
    
    landing_gps = [38.1446910 -76.4279902,0];
    landing_case = 1;
    land_dir = [-52 128 24 -156;];
    
%     land_temp = miss.landing_point;
    
    landWP = WP(21,0,0,0,0,miss.landing_point(1),miss.landing_point(2),0);
%     landWP_final = WP(21,0,0,0,0,landing_gps(1),landing_gps(2),0);
%     landWP.state = 1;
%     landWP.toMeters(miss.dropPoint_gps);
    
%     land_point = [-landWP.lat, landWP.lng, 0];
    land_point = [miss.landing_point(1),miss.landing_point(2),0];
    temp_points = [];
    
    land_dist1 = 300;
    land_dist2 = 200;
    land_slope = 15;
    
    cmd = 'v';
    while cmd ~= 'n'
        
        wp1 = land_point+[land_dist1*cosd(land_dir(landing_case)) land_dist1*sind(land_dir(landing_case)) land_dist1*sind(land_slope)];
        wp2 = land_point+[land_dist2*cosd(land_dir(landing_case)) land_dist2*sind(land_dir(landing_case)) land_dist2*sind(land_slope)];
        
        landing_wps = [last_wp; wp1; wp2; land_point];
        
        hold off
        plot(landing_wps(:,1),landing_wps(:,2),'b')
        hold on
        scatter(landing_wps(:,1),landing_wps(:,2),'b')
        text(landing_wps(1:2,1),landing_wps(1:2,2),string(round(landing_wps(1:2,3))))
        plot(bounds(:,1),bounds(:,2),'r--')
        plot_obs(obstacles)
        
 
        midpoint = land_point;
        maxdist = 300;
        
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])
        axis equal
            



        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            landing_case = landing_case-1;
            if landing_case <= 0
                landing_case = 4;
            end
        end

        if cmd == 'd'
            landing_case = landing_case+1;
            if landing_case > 4
                landing_case = 1;
            end
        end

%         if cmd == 'n'
%             
%         end

    end
    
    
    
    wp_miss = [last_wp; wp1; land_point];
    
    cmd = 'v';
    while cmd ~= 'n'
        
        hold off
        plot(wp_miss(:,1),wp_miss(:,2),'b')
        hold on
        scatter(wp_miss(2,1),wp_miss(2,2),'b')
        text(landing_wps(1:2,1),landing_wps(1:2,2),string(round(landing_wps(1:2,3))))
        
        plot(bounds(:,1),bounds(:,2),'r--')
        plot_obs(obstacles)
        
        if ~isempty(temp_points)
            scatter(temp_points(:,1),temp_points(:,2),'b')
            temp = [last_wp; temp_points; wp1];
            plot(temp(:,1),temp(:,2),'r')
            text(temp(:,1),temp(:,2),string(round(temp(:,3))))
        end
        
        midpoint = (last_wp(1:2)+wp1(1:2))/2;
        maxdist = norm(last_wp(1:2)-wp1(1:2));
        
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])
%         axis equal
            

        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            add_point = ginput(1);
            height_mean = norm(add_point-last_wp(1:2))/(norm(add_point-last_wp(1:2))+norm(land_point(1:2)-add_point));
            temp_points = [temp_points; add_point last_wp(3)+(wp1(3)-last_wp(3))*height_mean];
        end

        if cmd == 'r'
            temp_points = [];
        end

        if cmd == 'n'

        end
    end
    
    
    
    wp_list = [];
    for k = 1:size(temp_points,1)
        wp_list = [wp_list; WP(16,0,0,0,0,temp_points(k,1),temp_points(k,2),temp_points(k,3))];
    end
    
    landWP2 = WP(16,0,0,0,0,wp2(1),wp2(2),wp2(3));
    landWP1 = WP(16,0,0,0,0,wp1(1),wp1(2),wp1(3));
    wp_list = [wp_list; landWP1; landWP2; landWP];
    
    final_wps = wp_list;
end

