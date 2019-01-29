function [takeoff_wps] = takeoff(launch,wp,obstacles)
    total_wps = launch;
    
    
    temp_points = [];    

    cmd = 'v';
    while cmd ~= 'n'
        en = min(k+2,length(wps));
%         plot the next two
        hold off
        plot(wps(k:en,1),wps(k:en,2),'b')
        hold on
        scatter(wps(k:en,1),wps(k:en,2),'b')
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
            if (norm(midpoint-obstacles(i,1:2)) < maxdist)
                x = obstacles(i,1)+obstacles(i,3)*cos(t);
                y = obstacles(i,2)+obstacles(i,3)*sin(t);
                plot(x,y,'r')
                scatter(obstacles(i,1),obstacles(i,2),'r')
            end
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

    takeoff_wps = total_wps;
end

