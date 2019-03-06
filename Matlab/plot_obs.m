function plot_obs(obstacles)
    t = -.1:.1:2*pi;
    for i = 1:size(obstacles,1)
        x = obstacles(i,1)+obstacles(i,4)*cos(t);
        y = obstacles(i,2)+obstacles(i,4)*sin(t);
        plot(x,y,'r')
%         scatter(obstacles(i,1),obstacles(i,2),'r')
        text(obstacles(i,1),obstacles(i,2),string(round(obstacles(i,3))),'Color','red')
    end
end

