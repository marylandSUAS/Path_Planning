function final_wps = Emergent(emergent_wp,last_wp,bounds,obstacles)

        
    temp_points = [];
    mission_wps = [last_wp; emergent_wp];
    
    cmd = 'v';
    while cmd ~= 'n'
        
        
        
        hold off
        plot(mission_wps(:,1),mission_wps(:,2),'b')
        hold on
        scatter(mission_wps(1,1),mission_wps(1,2),'g','filled')
        scatter(mission_wps(2,1),mission_wps(2,2),'y','filled')     
        text(mission_wps(:,1),mission_wps(:,2),string(round(mission_wps(:,3))))
        
        if ~isempty(temp_points)
            scatter(temp_points(:,1),temp_points(:,2),'b')
            text(temp_points(:,1),temp_points(:,2),string(round(temp_points(:,3))))
            temp = [last_wp; temp_points; emergent_wp];
            plot(temp(:,1),temp(:,2),'r')
        end
        
        plot(bounds(:,1),bounds(:,2),'r--')
        plot_obs(obstacles)
 
        midpoint = (emergent_wp(1:2)+last_wp(1:2))/2;
        maxdist = norm(emergent_wp(1:2)-last_wp(1:2))*.75;
        
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])


        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            add_point = ginput(1);
            height_mean = norm(add_point-last_wp(1:2))/(norm(add_point-last_wp(1:2))+norm(emergent_wp(1:2)-add_point));
            temp_points = [temp_points; add_point last_wp(3)+(emergent_wp(3)-last_wp(3))*height_mean];
        end

        if cmd == 'r'
            temp_points = [];
        end

        if cmd == 'n'
            total_wps = [temp_points; emergent_wp];
        end
    end
    
    
    
    
    wp_list = [];
    for k = 1:length(total_wps)
        wp_list = [wp_list; WP(16,0,0,0,0,total_wps(1),total_wps(2),total_wps(3))];
    end
    
    final_wps = wp_list;
end

