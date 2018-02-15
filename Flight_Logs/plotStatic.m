function plotStatic()
    fileID = fopen('flightInfo.txt');
    C = fscanf(fileID,'%f %f %f');
    fclose(fileID);
    
    
%     viscircles([obj.Location(1),obj.Location(2)],obj.Radius,'Color',[dif 1-dif .5]);

end
