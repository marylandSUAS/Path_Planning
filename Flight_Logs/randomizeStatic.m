function staticObs = randomizeStatic(start,finish,number)
    
    objects = [];
    fileID = fopen('static_obstacles.txt','w');
    for k = 1:number 
        
        theta = atan2(finish(2)-start(2),finish(1)-start(1));
        z = rand()*50+50;
        r = rand()*12+3;
        dis = rand()*2-1;
        x = start(1)+((.5*rand()+.25)*(finish(1)-start(1)))+dis*r*sin(theta);
        
        y = start(2)+((.5*rand()+.25)*(finish(2)-start(2)))+dis*r*cos(theta);
        
        fprintf(fileID,'%4.2f %4.2f %4.2f %4.2f\n',[x y z r]);
        objects = [objects; x y z r];
    end
    fclose(fileID);
    staticObs = objects;
end
