function printLoc(Obstacles)
    fileID = fopen('moving_obstacles.txt','w');
    for ob = 1:length(Obstacles)
        fprintf(fileID,'%4.2f %4.2f %4.2f %4.2f %4.2f %4.2f %4.2f\n',[Obstacles(ob).Radius Obstacles(ob).Location Obstacles(ob).Velocity*[cos(Obstacles(ob).direction(1)) sin(Obstacles(ob).direction(1)) sin(Obstacles(ob).direction(2))]]);
    end 
    fclose(fileID);
end