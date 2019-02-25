function final_wps = OffAxis(offAxis_point,last_wp,bounds,obstacles)

    temp_points = [];

    off_dir = 1;
    off_alt = 100;
    off_theta = 0;
    off_dist = 200;
    
    off_dist1 = 130;
    off_dist2 = 50;
    off_dist3 = 0;
    
    
    
    cmd = 'v';
    while cmd ~= 'n'
        off_point = offAxis_point + [off_dist*cosd(off_theta+(off_dir*90)) off_dist*sind(off_theta+(off_dir*90)) 0];
        wp1 = off_point+[off_dist1*cosd(off_theta) off_dist1*sind(off_theta) off_alt];
        wp2 = off_point+[off_dist2*cosd(off_theta) off_dist2*sind(off_theta) off_alt];
        wp3 = off_point+[off_dist3*cosd(off_theta) off_dist3*sind(off_theta) off_alt];
        
        mission_wps = [last_wp; wp1; wp2; wp3];
        hold off
        plot(mission_wps(:,1),mission_wps(:,2),'b')
        hold on
        scatter(mission_wps(:,1),mission_wps(:,2),'b')
        scatter(mission_wps(2,1),mission_wps(2,2),'g','filled')
        text(mission_wps(:,1),mission_wps(:,2),string(round(mission_wps(:,3))))

        plot(bounds(:,1),bounds(:,2),'r--')
        plot_obs(obstacles)
 
        midpoint = wp3;
        maxdist = 300;
        
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])


        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            off_theta = off_theta+5;
            if off_theta > 359
                off_theta = off_theta-360;
            end
        end

        if cmd == 'd'
            off_theta = off_theta-5;
            if off_theta <= 0
                off_theta = off_theta+360;
            end
        end
        if cmd == 'w'
            off_dist = off_dist+5;
        end
        if cmd == 's'
            off_dist = off_dist-5;
        end
        if cmd == 'f'
            off_dir = off_dir*-1;
        end
        if cmd == 'n'

        end

    end
    cmd = 'v';
    wp_miss = [last_wp; wp1; wp3];
    while cmd ~= 'n'
        
        hold off
        plot(wp_miss(:,1),wp_miss(:,2),'b')
        hold on
        scatter(wp_miss(2,1),wp_miss(2,2),'b')
        text(wp_miss(:,1),wp_miss(:,2),string(round(wp_miss(:,3))))

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
        
        
        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            add_point = ginput(1);
            height_mean = norm(add_point-last_wp(1:2))/(norm(add_point-last_wp(1:2))+norm(add_point-wp1(1:2)));
            temp_points = [temp_points; add_point last_wp(3)+(wp1(3)-last_wp(3))*height_mean];
        end
        
        if cmd == 'r'
            temp_points = [];
        end

        if cmd == 'n'

        end
    end

    angle = -off_dir*atan(off_dist/off_alt);
    MountControl1 = WP(205,0,angle,0,0,0,0,0);
    MountControl2 = WP(205,0,0,0,0,0,0,0);
    
    wp_list = [];
    for k = 1:size(temp_points,1)
        wp_list = [wp_list; WP(16,0,0,0,0,temp_points(k,1),temp_points(k,2),temp_points(k,3))];
    end
    
    wp_list = [wp_list; 
        WP(16,0,0,0,0,wp1(1),wp1(2),wp1(3));
        MountControl1; 
        WP(16,0,0,0,0,wp2(1),wp2(2),wp2(3));
        WP(16,0,0,0,0,wp3(1),wp3(2),wp3(3));
        MountControl2];
        
    final_wps = wp_list;
end

