clear all; close all; clc;
missionDirectory = 'C:\Users\imaging2.0\Documents\MUAS-17\Flight_Path';
rhs_info = strcat(missionDirectory,'\rhs.txt');
rhs_handle = fopen(rhs_info);
dim = sscanf(fgets(shortest_path_handle),'%f, %f, %f');
dim1 = dim(1); dim2 = dim(2); dim3 = dim(3);
% if(changed == '1')
    % Extract data for start, goal and current nodes, and obstacle
    % locations.
    line = fgets(flight_information_handle);
    while line ~= -1
        obstacle_index = obstacle_index + 1;
        line = textscan(line,'%s %f %f %f %f');
    path_data = fscanf(shortest_path_handle,'%f',[3,inf])';
    updated = textscan(fgets(flight_information_handle),'%s %d');
    updated = updated{2};
    goal = textscan(fgets(flight_information_handle),'%s %f %f %f');
    goal = [goal{2},goal{3},goal{4}];
fclose(f);