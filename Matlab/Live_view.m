format long
miss = mission('../missions/test_mission_1.txt');

current_data_file = '../MissionPlanner/LiveData.txt';

path = [];
while 1
    data = getdata(current_data_file);
    
    path = plot_data(data,path,miss);
    miss.visualize_live();
    
    axis equal
    pause(.5)
end


function new_path = plot_data(data,path,mission)
        hold off
        data(4) = 90-data(4);
        pos = toMeters(data(1:2),mission.dropPoint_gps);
        scatter(pos(1),pos(2),'bx')
        hold on
        text(pos(1),pos(2),string(round(data(3))),'Color','blue')
        dist = 30;
        plot([pos(1) pos(1)+dist*cosd(data(4))],[pos(2) pos(2)+dist*sind(data(4))],'b')
        
        path = [pos;path];
        if size(path,1) > 20
            path = path(1:end-1,:);
        end
        plot(path(:,1),path(:,2),'m')
        title("WP#: "+string(data(5))+" Time: "+string(data(6)))
        new_path = path;
end

function data = getdata(file)
            data = importdata(file);
%             data = cellfun(@str2num,strsplit(filedata,' '));
%             lat lng alt yaw wpno time
end

function meters = toMeters(GPS,homeGPS)
            rad_Earth = 6371000;
            dlng = (pi/180)*rad_Earth*cos(homeGPS(1)*pi/180);
            dlat = (pi/180)*rad_Earth;

            x = (GPS(2)-homeGPS(2))*dlng;
            y = (GPS(1)-homeGPS(1))*dlat;
            if length(GPS) < 3
                meters = [x,y,0];
            elseif length(GPS) > 3
                meters = [x,y,GPS(3:length(GPS))];
            else
                meters = [x,y,GPS(3)];
            end
        end