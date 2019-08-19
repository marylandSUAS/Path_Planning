%% start mission
% miss = mission(' ');
format long
miss = mission('../missions/test_mission_4.txt');
final_wps = [];
miss.visualize()

%% Visualize
miss.visualize()


%% View Current
miss.visualize_current(final_wps)


%% Reset mission
final_wps = [];


%% Testing
last_wp = miss.waypoints(end,:);


%% Waypoints 
takeoff_wp = WP(22,15,0,0,1,0,0,100);
wps = WPMission([miss.launch_wps; miss.waypoints],miss.bounds,miss.obstacles);

final_wps = [takeoff_wp;wps];
last_wp = [wps(end).lat wps(end).lng wps(end).alt];


%% Drop target (wind testing)
% N-0  E-90  S-180  W-270
wind = 5;
wind_dir = 240;
drop_wps = DropMission(miss.dropPoint, last_wp, miss.bounds,miss.obstacles,wind,wind_dir);

last_wp = [drop_wps(end).lat drop_wps(end).lng drop_wps(end).alt];
final_wps = [final_wps;drop_wps];


%% Landing
landing_wps = Landing(last_wp, miss, miss.bounds, miss.obstacles);
final_wps = [final_wps;landing_wps];


%% Convert to Lat/Long and Write to file
for i = 1:length(final_wps)
    if(final_wps(i).id == 16 || final_wps(i).id == 21)
        final_wps(i) = final_wps(i).toGPS(miss.dropPoint_gps);
    end
end
printMission(final_wps,'../MissionPlanner/mission_File_1.txt')
fprintf('Done\n')
