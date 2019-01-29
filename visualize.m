
function = visualize(obj)
%             figure;

    temp = obj.bounds;
    temp = [temp; temp(1,:)];
    plot(temp(:,1),temp(:,2),'r')
    hold on
%             scatter(obj.bounds(:,1),obj.bounds(:,2),'ro')

    plot(obj.waypoints(:,1),obj.waypoints(:,2),'b')
    scatter(obj.waypoints(:,1),obj.waypoints(:,2),'bo')
    scatter(obj.waypoints(1,1),obj.waypoints(1,2),'g','filled')

    temp = obj.searchGrid;
    temp = [temp; temp(1,:)];
    plot(temp(:,1),temp(:,2),'g')

    scatter(obj.dropPoint(1),obj.dropPoint(2),10,'y')

    scatter(obj.offAxis(1),obj.offAxis(2),10,'b')

    scatter(obj.emergent(1),obj.emergent(2),10,'or')


    th = 0:pi/50:2*pi;
    for a = 1:size(obj.obstacles,1)
        xunit = obj.obstacles(a,4) * cos(th) + obj.obstacles(a,1);
        yunit = obj.obstacles(a,4) * sin(th) + obj.obstacles(a,2);
        plot(xunit, yunit,'r');
    end

%             axis([center(1)+sizing(1)/2 center(1)-sizing(1)/2 center(2)+sizing(2)/2 center(2)-sizing(2)/2])
    hold off
end


