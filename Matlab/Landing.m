function final_wps = Landing(land_point,last_wp,bounds,obstacles)
%LANDING takes in landing point(x/y) and last_wp(x/y)
    % returns landing waypoints(WP)
    
    land_dir = 0;
    
    land_dist1 = 130;
    land_dist2 = 50;

    land_slope = 100;
    
    landWP = WP(21,0,0,0,0,land_point(1),land_point(2),0);
    
    temp_points = [];
    
    cmd = 'v';
    while cmd ~= 'n'
        
        wp1 = land_point+[land_dist1*cosd(land_dir) land_dist1*sind(land_dir) land_dist1*sind(land_slope)];
        wp2 = land_point+[land_dist2*cosd(land_dir) land_dist2*sind(land_dir) land_dist2*sind(land_slope)];
        
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




        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            land_dir = land_dir+5;
            if land_dir > 359
                land_dir = land_dir-360;
            end
        end

        if cmd == 'd'
            land_dir = land_dir-5;
            if land_dir <= 0
                land_dir = land_dir+360;
            end
        end

        if cmd == 'n'

        end

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
%             total_wps = [wps(1,:); temp_points; wp1; wp2; wp3];
        end
    end
    
    
    
    
    wp_list = [];
    for k = 1:length(temp_points)
        wp_list = [wp_list; WP(16,0,0,0,0,temp_points(k,1),temp_points(k,2),temp_points(k,3))];
    end
    
    landWP2 = WP(16,0,0,0,0,wp2(1),wp2(2),wp2(3));
    landWP1 = WP(16,0,0,0,0,wp1(1),wp1(2),wp1(3));
    wp_list = [wp_list; landWP1; landWP2; landWP];
    
    final_wps = wp_list;
end

