function printMission(waypoints, file_location)
    fileID = fopen(file_location,'w');
    for i = 1:length(waypoints)
        temp = [i waypoints(i).id waypoints(i).p1 waypoints(i).p2 waypoints(i).p3 waypoints(i).p4 waypoints(i).lat waypoints(i).lng waypoints(i).alt];
        fprintf(fileID,'%d %d %4.2f %4.2f %4.2f %4.2f %4.9f %4.9f %4.9f\n',temp);
    end 
    fclose(fileID);
end

