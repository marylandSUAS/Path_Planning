function final_wps = DropMission(drop_point,last_wp,bounds,obstacles,wind,dir)

    drop_alt = 35;
    cruise_speed = 16;
    
%     calculate drop distance away
    
    
    
    calc_dist = 20;
    
    drop_dir = 0;
    drop_dist1 = 80+calc_dist;
    drop_dist2 = 0+calc_dist;
    drop_dist3 = -50+calc_dist;
    
    
    cmd = 'v';
    while cmd ~= 'n'
        
        wp1 = drop_point+[drop_dist1*cosd(drop_dir) drop_dist1*sind(drop_dir) drop_alt];
        wp2 = drop_point+[drop_dist2*cosd(drop_dir) drop_dist2*sind(drop_dir) drop_alt];
        wp3 = drop_point+[drop_dist3*cosd(drop_dir) drop_dist3*sind(drop_dir) drop_alt];
        
        temp_wps = [last_wp; wp1; wp2; wp3];
        hold off
        plot(temp_wps(:,1),temp_wps(:,2),'b')
        hold on
        scatter(temp_wps(:,1),temp_wps(:,2),'b')
        scatter(temp_wps(2,1),temp_wps(2,2),'g','filled')
        text(temp_wps(1:2,1),temp_wps(1:2,2),string(round(temp_wps(1:2,3))))
        
        plot(bounds(:,1),bounds(:,2),'r--')
        plot_obs(obstacles)
 
        midpoint = wp1;
        maxdist = 300;
       
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])
%         axis equal
            



        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            drop_dir = drop_dir+5;
            if drop_dir > 359
                drop_dir = drop_dir-360;
            end
        end

        if cmd == 'd'
            drop_dir = drop_dir-5;
            if drop_dir <= 0
                drop_dir = drop_dir+360;
            end
        end

        if cmd == 'n'

        end

    end
    
    
    temp_points = [];

    cmd = 'v';
    wp_miss = [last_wp; wp1; wp3];
    while cmd ~= 'n'
        
        hold off
        plot(wp_miss(:,1),wp_miss(:,2),'b')
        hold on
        scatter(wp_miss(2,1),wp_miss(2,2),'b')
        text(wp_miss(1:2,1),wp_miss(1:2,2),string(round(wp_miss(1:2,3))))
        scatter(wp_miss(2,1),wp_miss(2,2),'g','filled')

        plot(bounds(:,1),bounds(:,2),'r--')
        plot_obs(obstacles)
        if ~isempty(temp_points)
            scatter(temp_points(:,1),temp_points(:,2),'b')
            text(temp_points(:,1),temp_points(:,2),string(round(temp_points(:,3))))
            temp = [last_wp; temp_points; wp1];
            plot(temp(:,1),temp(:,2),'r')
        end
        
        midpoint = (last_wp(1:2)+wp1(1:2))/2;
        maxdist = norm(last_wp(1:2)-wp1(1:2))*.75;
        
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])
%         axis equal
            

        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            add_point = ginput(1);
            height_mean = norm(add_point-last_wp(1:2))/(norm(add_point-last_wp(1:2))+norm(wp1(1:2)-add_point));
            temp_points = [temp_points; add_point last_wp(3)+(wp1(3)-last_wp(3))*height_mean];
        end

        if cmd == 'r'
            temp_points = [];
        end

        if cmd == 'n'

        end
    end
    
    ReleaseWP = WP(183,9,2100,0,0,0,0,0);

    wp_list = [];
    for k = 1:size(temp_points,1)
        wp_list = [wp_list; WP(16,0,0,0,0,temp_points(k,1),temp_points(k,2),temp_points(k,3))];
    end
    wp_list = [wp_list; 
        WP(16,0,0,0,0,wp1(1),wp1(2),wp1(3));
        WP(16,0,0,0,0,wp2(1),wp2(2),wp2(3));
        ReleaseWP
        WP(16,0,0,0,0,wp3(1),wp3(2),wp3(3))];
    final_wps = wp_list;
end

