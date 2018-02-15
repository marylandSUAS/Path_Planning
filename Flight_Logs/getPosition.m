function loc = getPosition()
    fileID = fopen('flightInfo.txt');
    C = fscanf(fileID,'%f %f %f');
    fclose(fileID);
    
    loc = C;
end