clear all
clc

grid_point = [-500 0; 300 100; 350 -150; -0 -300; -450 -200];

grid_point = [grid_point; grid_point(1,:)];
flyPoints = [-300 -70; -70 -120; 180 -20];

longest_line = [1,0];
for k = 2:size(grid_point,1)
    temp = sqrt((grid_point(k,1)-grid_point(k-1,1))^2+(grid_point(k,2)-grid_point(k-1,2))^2);
    if temp > longest_line(2)
        longest_line = [k,temp];
    end
end
grid_theta = -atan((grid_point(longest_line(1),2)-grid_point(longest_line(1)-1,2))/(grid_point(longest_line(1),1)-grid_point(longest_line(1)-1,1)));

grid_rotated = [];
for k = 1:size(grid_point,1)
    grid_rotated = [grid_rotated; ([cos(grid_theta) -sin(grid_theta); sin(grid_theta) cos(grid_theta)] * grid_point(k,:)')'];
end

fly_rotated = [];
for k = 1:size(flyPoints,1)
    fly_rotated = [fly_rotated; ([cos(grid_theta) -sin(grid_theta); sin(grid_theta) cos(grid_theta)] * flyPoints(k,:)')'];
end

topLeftPoint = 1;
grid_dist = [0 0];
for k = 1:size(grid_rotated,1)-1
    distX = grid_rotated(k,1)-grid_rotated(topLeftPoint,1);
    distY = grid_rotated(k,2)-grid_rotated(topLeftPoint,2);
    grid_dist(1) = sign(distX)*max([abs(grid_dist(1)) abs(distX)]);
    grid_dist(2) = sign(distY)*max([abs(grid_dist(2)) abs(distY)]);
end



num_points = [round(grid_dist(1)/photo_coverage(2))+1 abs(round(grid_dist(2)/photo_coverage(1)+.5))+1];

Grid(1:num_points(1),1:num_points(2)) = Grid_Point();
for k = 1:num_points(1)
    for j = 1:num_points(2)
        Grid(j,k).Location = [grid_rotated(topLeftPoint,1)+k*photo_coverage(2)-photo_coverage(2)/2
                              photo_coverage(1)/2+grid_rotated(topLeftPoint,2)-j*photo_coverage(1)];
    end
end

inPloyPoints = [];
for k = 1:num_points(1)
    for j = 1:num_points(2)
        if(Grid(j,k).inPoly(grid_rotated))
            inPloyPoints = [inPloyPoints; Grid(j,k).Location'];
        end
    end
end


final_loc = [];
for k = 1:size(inPloyPoints,1)
    final_loc = [final_loc; ([cos(-grid_theta) -sin(-grid_theta); sin(-grid_theta) cos(-grid_theta)] * inPloyPoints(k,:)')'];
end


disp('Number of photos: ')
disp(length(inPloyPoints))
Pos1 = [];
Pos2 = [];
Pos3 = [];


for k = 1:size(final_loc,1)
    dist1 = sqrt((flyPoints(1,1)-final_loc(k,1))^2+(flyPoints(1,2)-final_loc(k,2))^2);
    dist2 = sqrt((flyPoints(2,1)-final_loc(k,1))^2+(flyPoints(2,2)-final_loc(k,2))^2);
    dist3 = sqrt((flyPoints(3,1)-final_loc(k,1))^2+(flyPoints(3,2)-final_loc(k,2))^2);
    if(dist1 < dist2 && dist1 < dist3)
        Pos1 = [Pos1; final_loc(k,:)];
    elseif(dist2 < dist1 && dist2 < dist3)
        Pos2 = [Pos2; final_loc(k,:)];
    else
        Pos3 = [Pos3; final_loc(k,:)];
    end
end




% hold off
% 
% hold on
% fly points
% 

% Grid Points
hold off
% plot(grid_rotated(:,1),grid_rotated(:,2))
plot(grid_point(:,1),grid_point(:,2))
hold on
scatter(flyPoints(:,1),flyPoints(:,2))
% scatter(fly_rotated(1,1),fly_rotated(1,2),'mx')
scatter(Pos1(:,1),Pos1(:,2),'mx')
% scatter(fly_rotated(2,1),fly_rotated(2,2),'gx')
scatter(Pos2(:,1),Pos2(:,2),'gx')
% scatter(fly_rotated(3,1),fly_rotated(3,2),'bx')
scatter(Pos3(:,1),Pos3(:,2),'bx')

%{
for k = 1:num_points(1)
    for j = 1:num_points(2)
        scatter(Grid(j,k).Location(1),Grid(j,k).Location(2),'rx')
    end
end
% plot([0 1000*cos(grid_theta)],[0 1000*sin(grid_theta)])
%}


axis equal