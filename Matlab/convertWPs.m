function convertWPs(waypoints,home)
%UNTITLED3 Does this show somewhere
%   Detailed explanation
    for i = 1:length(waypoints)
        if(waypoints(i).id == 16 || waypoints(i).id == 21)
            waypoints(i) = waypoints(i).toGPS(home);
        end
    end
end

