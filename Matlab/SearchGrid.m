function final_wps = SearchGrid(searchGrid,last_wp,bounds,obstacles)
    
    grid_point = [searchGrid(:,1:2); searchGrid(1,1:2)];
    search_altitude = 100;
    photo_coverage = [70 40];
    
%   choose direction to run along
%   usually the long line distance
    longest_line = [1,0];
    for k = 2:size(grid_point,1)
        temp = sqrt((grid_point(k,1)-grid_point(k-1,1))^2+(grid_point(k,2)-grid_point(k-1,2))^2);
        if temp > longest_line(2)
            longest_line = [k,temp];
        end
    end
    
    cmd = 'v';
    while cmd ~= 'n'

        grid_theta = atan((grid_point(longest_line(1),2)-grid_point(longest_line(1)-1,2))/(grid_point(longest_line(1),1)-grid_point(longest_line(1)-1,1)));
        
        hold off
        plot(bounds(:,1),bounds(:,2),'r--')
        hold on
        plot_obs(obstacles)
        plot(grid_point(:,1),grid_point(:,2),'g')
        center = [mean(grid_point(:,1)) mean(grid_point(:,2))];
        temp_diff = 200*[cos(grid_theta) sin(grid_theta)];
        plot([center(1)+temp_diff(1) center(1)-temp_diff(1)],[center(2)+temp_diff(2) center(2)-temp_diff(2)],'b','linewidth', 2)
        axis([min(grid_point(:,1)-100) max(grid_point(:,1)+100) min(grid_point(:,2)-100) max(grid_point(:,2)+100)])
%         axis equal
        
        
        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            if(longest_line(1) == 2)
                longest_line(1) = size(grid_point,1);
            else
                longest_line(1) = longest_line(1) - 1;
            end
        end
        if cmd == 'd'
            if(longest_line(1) == size(grid_point,1))
                longest_line(1) = 2;
            else
                longest_line(1) = longest_line(1) + 1;
            end
        end
        if cmd == 'n'
%           continue 
        end
    end
    
    
    grid_rotated = [];
    for k = 1:size(grid_point,1)
        grid_rotated = [grid_rotated; ([cos(-grid_theta) -sin(-grid_theta); sin(-grid_theta) cos(-grid_theta)] * grid_point(k,:)')'];
    end
    
    
%     compute all grid points here
    grid_bounds = [min(grid_rotated(:,1)) max(grid_rotated(:,1)) min(grid_rotated(:,2)) max(grid_rotated(:,2))];
    
    num_points = [round(((grid_bounds(2)-grid_bounds(1))/photo_coverage(1))+.5) round(((grid_bounds(4)-grid_bounds(3))/photo_coverage(2))+.5)];
    
    
    grid_points(num_points(1),num_points(2)) = Grid_Point();
    for k = 1:num_points(1)
        for l = 1:num_points(2)
            grid_points(k,l).Location = [grid_bounds(1)+photo_coverage(1)*k-.5*photo_coverage(1) grid_bounds(3)+photo_coverage(2)*l-.5*photo_coverage(2)];
            grid_points(k,l).in_que = grid_points(k,l).inPoly([grid_rotated; grid_rotated(1,:)]);
        end
    end
    
    %{
    grid_points_in = [];
    grid_points_out = [];
    hold off
    plot(grid_rotated(:,1),grid_rotated(:,2),'g')
    hold on
    for k = 1:num_points(1)
        for l = 1:num_points(2)
            if grid_points(k,l).in_que
                grid_points_in = [grid_points_in; grid_points(k,l).Location(1) grid_points(k,l).Location(2)];
            else
                grid_points_out = [grid_points_out; grid_points(k,l).Location(1) grid_points(k,l).Location(2)];
            end
        end
    end
    scatter(grid_points_in(:,1),grid_points_in(:,2),'g')
    scatter(grid_points_out(:,1),grid_points_out(:,2),'r')
    axis equal
    figure;
    %}
    
    edges = [];
    for k = 1:num_points(2)
        if (grid_points(1,k).in_que)
            edges = [edges; 1 k];
        else
            for m = 2:num_points(1)
                if (grid_points(m,k).in_que && ~grid_points(m-1,k).in_que)
                    edges = [edges; m k];
                    break;
                end
            end
        end
        
        if (grid_points(num_points(1),k).in_que)
            edges = [edges; num_points(1) k];
        else
            for m = num_points(1)-1:-1:1
                if ((grid_points(m,k).in_que && ~grid_points(m+1,k).in_que))
                    edges = [edges; m k];
                    break;
                end
            end
        end
    end
    
    
%     choosing starting point
    starting_points = [edges(1:2,1:2); edges(end-1:end,1:2)];
    starting_num = 1;
    
    cmd = 'v';
    while cmd ~= 'n'
        starting_point = grid_points(starting_points(starting_num,1),starting_points(starting_num,2)).Location;
        starting_point = ([cos(grid_theta) -sin(grid_theta); sin(grid_theta) cos(grid_theta)] * starting_point')';
        starting_point = [starting_point search_altitude];
        
        hold off
        plot(bounds(:,1),bounds(:,2),'r--')
        hold on
        plot_obs(obstacles)
        plot(grid_point(:,1),grid_point(:,2),'g')
        plot([last_wp(1) starting_point(1)],[last_wp(2) starting_point(2)],'b','linewidth',2)
        scatter(last_wp(1),last_wp(2),'g','filled')
        
        midpoint = (last_wp(1:2)+starting_point(1:2))/2;
        maxdist = norm(last_wp(1:2)-starting_point(1:2));
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])
        
        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        
        if cmd == 'a'
            if(starting_num == 1)
                starting_num = 4;
            else
                starting_num = starting_num-1;
            end
        end
        if cmd == 'd'
            if(starting_num == 4)
                starting_num = 1;
            else
                starting_num = starting_num+1;
            end
        end
        if cmd == 'n'
%           continue 
        end
    end
    
    
%     add points for collisions on the way to first point
    arrival_points = [];
    cmd = 'v';
    while cmd ~= 'n'
        
        hold off
        plot(bounds(:,1),bounds(:,2),'r--')
        hold on
        plot_obs(obstacles)
        plot(grid_point(:,1),grid_point(:,2),'g')
        plot([last_wp(1) starting_point(1)],[last_wp(2) starting_point(2)],'b')
        scatter(last_wp(1),last_wp(2),'g','filled')
        
        if ~isempty(arrival_points)
            scatter(arrival_points(:,1),arrival_points(:,2),'b')
            temp = [last_wp; arrival_points; starting_point];
            plot(temp(:,1),temp(:,2),'r')
            text(temp(:,1),temp(:,2),string(round(temp(:,3))))
        end
        
        midpoint = (last_wp(1:2)+starting_point(1:2))/2;
        maxdist = norm(last_wp(1:2)-starting_point(1:2));
        axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])
        

        w = waitforbuttonpress;
        cmd = get(gcf, 'CurrentCharacter');

        if cmd == 'a'
            add_point = ginput(1);
            height_mean = norm(add_point-last_wp(1:2))/(norm(add_point-last_wp(1:2))+norm(starting_point(1:2)-add_point));
            arrival_points = [arrival_points; add_point last_wp(3)+(search_altitude-last_wp(3))*height_mean];
        end

        if cmd == 'r'
            arrival_points = [];
        end

        if cmd == 'n'

        end
    end


    if (rem(starting_num,2) == 1)
        f2l = 0;
    else
        f2l = 1;
    end
    temp_waypoints = [];
    flip = 0;
    if (starting_num > 2)
        for k = size(edges,1)/2:-1:1
            if ~flip
                temp_waypoints = [temp_waypoints; grid_points(edges(2*k-1+f2l,1),edges(2*k-1+f2l,2)).Location];
                temp_waypoints = [temp_waypoints; grid_points(edges(2*k-f2l,1),edges(2*k-f2l,2)).Location];
                flip = 1;
            else
                temp_waypoints = [temp_waypoints; grid_points(edges(2*k-f2l,1),edges(2*k-f2l,2)).Location];
                temp_waypoints = [temp_waypoints; grid_points(edges(2*k-1+f2l,1),edges(2*k-1+f2l,2)).Location];
                flip = 0;
            end
        end
    else
        for k = 1:size(edges,1)/2
            if ~flip
                temp_waypoints = [temp_waypoints; grid_points(edges(2*k-1+f2l,1),edges(2*k-1+f2l,2)).Location];
                temp_waypoints = [temp_waypoints; grid_points(edges(2*k-f2l,1),edges(2*k-f2l,2)).Location];
                flip = 1;
            else
                temp_waypoints = [temp_waypoints; grid_points(edges(2*k-f2l,1),edges(2*k-f2l,2)).Location];
                temp_waypoints = [temp_waypoints; grid_points(edges(2*k-1+f2l,1),edges(2*k-1+f2l,2)).Location];
                flip = 0;
            end
            
        end
    end
    waypoints = [];
    for k = 1:size(temp_waypoints,1)
        waypoints = [waypoints; [([cos(grid_theta) -sin(grid_theta); sin(grid_theta) cos(grid_theta)] * temp_waypoints(k,:)')' search_altitude]];
    end
    
    %{
    hold off
    plot(waypoints(:,1),waypoints(:,2),'b')
    hold on
    plot(grid_point(:,1),grid_point(:,2),'g')
    axis equal
    %}
    
    
    total_wps = [];
    for k = 1:length(waypoints)-1
        
        temp_points = [];

        
        cmd = 'v';
        while cmd ~= 'n'
            en = min(k+2,length(waypoints));
            bg = max(1,k-1);
    %         plot the next two
            hold off
            plot(waypoints(bg:en,1),waypoints(bg:en,2),'b')
            hold on
            scatter(waypoints(bg:en,1),waypoints(bg:en,2),'b')
            scatter(waypoints(k,1),waypoints(k,2),'g','filled')
            text(waypoints(bg:en,1),waypoints(bg:en,2),string(round(waypoints(bg:en,3))))
                
            
            if ~isempty(temp_points)
                scatter(temp_points(:,1),temp_points(:,2),'b')
                text(temp_points(:,1),temp_points(:,2),string(round(temp_points(:,3))))
                temp = [waypoints(k,1:3); temp_points; waypoints(k+1,1:3)];
                plot(temp(:,1),temp(:,2),'r')
            end
            
            plot(bounds(:,1),bounds(:,2),'r--')
            plot_obs(obstacles)
            
            midpoint = (waypoints(k,1:2)+waypoints(k+1,1:2))/2;
            maxdist = norm(waypoints(k,1:2)-waypoints(k+1,1:2));
            axis([midpoint(1)-maxdist midpoint(1)+maxdist midpoint(2)-maxdist midpoint(2)+maxdist])
%             axis equal
            
        
            w = waitforbuttonpress;
            cmd = get(gcf, 'CurrentCharacter');
        
            
            if cmd == 'a'
                add_point = ginput(1);
                height_mean = norm(add_point-waypoints(k,1:2))/(norm(add_point-waypoints(k,1:2))+norm(waypoints(k+1,1:2)-add_point));
                temp_points = [temp_points; add_point waypoints(k,3)+(waypoints(k+1,3)-waypoints(k,3))*height_mean];
            end
            
            if cmd == 'r'
                temp_points = [];
            end
            
            if cmd == 'n'
                total_wps = [total_wps; temp_points; waypoints(k+1,:)];
            end
            
            if cmd == 'x'
                total_wps = [total_wps; temp_points];
                cmd = 'n';
            end
            
            if cmd == 'm'
                add_point = ginput(1);
                waypoints(k+1,:) = [add_point search_altitude];
            end
        end
        
    end
    
    
    
    arrival_points
    total_wps
    
    wp_list = [];
    for k = 1:size(arrival_points,1)
        wp_list = [wp_list; WP(16,0,0,0,0,arrival_points(k,1),arrival_points(k,2),temp_points(k,3))];
    end
    for k = 1:size(total_wps,1)
        wp_list = [wp_list; WP(16,0,0,0,0,total_wps(k,1),total_wps(k,2),total_wps(k,3))];
    end
    
    final_wps = wp_list;
end

