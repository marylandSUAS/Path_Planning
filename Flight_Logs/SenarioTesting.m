%% Testing Senarios

clc 
clear all
close all

static_obstacles = randomizeStatic([-150 0 50],[150 0 50],3);

Nodes1 = [-100 -75 50;
        -100 75 50;
        100 75 50;
        100 -75 50];

Nodes2 = [0 75 65;
        0 -75 35];

Nodes3 = [0 50 50;
        25 -25 50
        -25 -25 50];
    
    
Object1 = moving_Object();
Object2 = moving_Object();
Object3 = moving_Object();

% Object(Nodes,Speed,Radius)
Object1 = Object1.setup(Nodes1,10,10);
Object2 = Object2.setup(Nodes2,8,15);
Object3 = Object3.setup(Nodes3,5,8);


Hz = 10;
r = robotics.Rate(Hz);

reset(r)
while(1)
%     tic
    Object1 = Object1.Update(1/Hz);
    Object2 = Object2.Update(1/Hz);
    Object3 = Object3.Update(1/Hz);
    tempLoc = getPosition();
    figure(1)
    
    hold off
    scatter(tempLoc(1),tempLoc(2))
    hold on
    Object1.plot(tempLoc(3))
    Object2.plot(tempLoc(3))
    Object3.plot(tempLoc(3))
    
    
    for k = 1:size(static_obstacles,1)
        viscircles([static_obstacles(k,1),static_obstacles(k,2)],static_obstacles(k,4),'Color','bl');
    end
    
    printLoc([Object1 Object2 Object3])
    
    axis([-150 150 -150 150])

    waitfor(r);
%     toc
end
