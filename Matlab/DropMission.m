function final_wps = DropMission(wps,bounds,obstacles,wind,dir)

    total_wps = wps(1,:);
        
    temp_points = [];

    drop_dir = 0;
    drop_dist1 = 130;
    drop_dist2 = 50;
    drop_dist3 = 0;
    drop_alt = 100;
    
    drop_point = wps(2,:);
    last_wp = wps(1,:);
    
    cmd = 'v';
    while cmd ~= 'n'
        
        wp1 = drop_point+[drop_dist1*cosd(drop_dir) drop_dist1*sind(drop_dir) drop_alt];
        wp2 = drop_point+[drop_dist2*cosd(drop_dir) drop_dist2*sind(drop_dir) drop_alt];
        wp3 = drop_point+[drop_dist3*cosd(drop_dir) drop_dist3*sind(drop_dir) drop_alt];
        
        temp_wps = [last_wp; wp1; wp2; wp3];
        hold off
        plot(temp_wps(:,1),temp_wps(:,2),'b')
        hold on
        scatter(wps(:,1),wps(:,2),'b')
        scatter(temp_wps(2:end,1),temp_wps(2:end,2),'g','filled')
        plot(bounds(:,1),bounds(:,2),'r--')

 
        midpoint = wp1;
        maxdist = 300;
        t = -.1:.1:2*pi;
        for i = 1:size(obstacles,1)
            x = obstacles(i,1)+obstacles(i,3)*cos(t);
            y = obstacles(i,2)+obstacles(i,3)*sin(t);
            plot(x,y,'r')
            scatter(obstacles(i,1),obstacles(i,2),'r')
        end
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])




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
    cmd = 'v';
    wp_miss = [last_wp; wp1; wp3];
    while cmd ~= 'n'
        
        hold off
        plot(wp_miss(:,1),wp_miss(:,2),'b')
        hold on
        scatter(wp_miss(2,1),wp_miss(2,2),'b')
        plot(bounds(:,1),bounds(:,2),'r--')
        
        if ~isempty(temp_points)
            scatter(temp_points(:,1),temp_points(:,2),'b')
            temp = [last_wp; temp_points; wp1];
            plot(temp(:,1),temp(:,2),'r')
        end
        
        midpoint = (last_wp(1:2)+wp1(1:2))/2;
        maxdist = norm(last_wp(1:2)-wp1(1:2))*.75;
        t = -.1:.1:2*pi;
        for i = 1:size(obstacles,1)
            x = obstacles(i,1)+obstacles(i,3)*cos(t);
            y = obstacles(i,2)+obstacles(i,3)*sin(t);
            plot(x,y,'r')
            scatter(obstacles(i,1),obstacles(i,2),'r')
        end
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])
        

        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            add_point = ginput(1);
            height_mean = norm(add_point-wps(1,1:2))/(norm(add_point-wps(1,1:2))+norm(wps(2,1:2)-add_point));
            temp_points = [temp_points; add_point wps(1,3)+(wps(2,3)-wps(1,3))*height_mean];
        end

        if cmd == 'r'
            temp_points = [];
        end

        if cmd == 'n'
            total_wps = [wps(1,:); temp_points; wp1; wp2; wp3];
        end
    end
    
    
    
    
    wp_list = [];
    for k = 1:length(total_wps)
        wp_list = [wp_list; WP(16,0,0,0,0,total_wps(k,1),total_wps(k,2),total_wps(k,3))];
    end
    
    final_wps = wp_list;
end

