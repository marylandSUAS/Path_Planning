format long
clear all
clc
file_location = '../missions/test_mission_1.txt';
home_gps = [38.1458554 -76.4263836];


bounds = [38.1466738 -76.4279151;38.1512131 -76.4292884;38.1519386 -76.4314556;38.1506056 -76.435382;38.1481082 -76.4330006;38.1447501 -76.4327645;38.1432650 -76.4346743;38.1404973 -76.4327431;38.1404973 -76.4260697;38.1439738 -76.4213920;38.1471801 -76.4234304;38.1462857 -76.4264131];
obstacles = [];
waypoints = [];


cmd = 'v';

while cmd ~= 'n'

    hold off
    plot(bounds(:,2),bounds(:,1),'g')
    hold on
    if size(obstacles,1) > 0
        if size(obstacles,1) == 1
            scatter(obstacles(1),obstacles(2),'r')
        else
            scatter(obstacles(:,1),obstacles(:,2),'r')
        end
    end
    if size(waypoints,1) > 0
        if size(obstacles,1) == 1
            scatter(waypoints(1),waypoints(2),'b')
            plot(waypoints(1),waypoints(2),'b')
        else
            scatter(waypoints(:,1),waypoints(:,2),'b')
            plot(waypoints(:,1),waypoints(:,2),'b')
        end
    end
    axis([-76.436 -76.42 38.14 38.152])
    
    w = waitforbuttonpress;
    cmd = get(gcf, 'CurrentCharacter');

    if cmd == 'o'
        obstacles = [obstacles; ginput(1)];
    end
    
    if cmd == 'w'
        waypoints = [waypoints; ginput(1)]
    end
    
    if cmd == 'a'
        off_axis_gps = ginput(1);
    end
    if cmd == 'e'
        emergent_gps = ginput(1);
    end
    
end




fileID = fopen(file_location,'w');
% drop point
fprintf(fileID,'%4.9f %4.9f\n',home_gps);
% off axis
fprintf(fileID,'%4.9f %4.9f\n',[off_axis_gps(2) off_axis_gps(1)]);
% emergent
fprintf(fileID,'%4.9f %4.9f\n',[emergent_gps(2) emergent_gps(1)]);
% waypoints
for i = 1:size(waypoints,1)
    if (i ~= 1)
        fprintf(fileID,',');
    end
    temp = [waypoints(i,2) waypoints(i,1) 100+rand()*200];
    fprintf(fileID,'%4.9f %4.9f %4.9f',temp);
end 
fprintf(fileID,'\n');
% bounds
fprintf(fileID,'38.1466738 -76.4279151,38.1512131 -76.4292884,38.1519386 -76.4314556,38.1506056 -76.4353824,38.1481082 -76.4330006,38.1447501 -76.4327645,38.1432650 -76.4346743,38.1404973 -76.4327431,38.1404973 -76.4260697,38.1439738 -76.4213920,38.1471801 -76.4234304,38.1462857 -76.4264131\n');
% search grid
fprintf(fileID,'38.1428600 -76.4336872,38.1411724 -76.4323997,38.1415774 -76.4260054,38.1446488 -76.4230442,38.1457626 -76.4247608\n');
% obstacles
for i = 1:size(obstacles,1)
    if (i ~= 1)
        fprintf(fileID,',');
    end
    temp = [obstacles(i,2) obstacles(i,1) 100+300*rand() 30+100*rand()];
    fprintf(fileID,'%4.9f %4.9f %4.9f %4.9f',temp);
end 
fclose(fileID);