%% start mission
miss = mission(' ');
final_wps = [];


%% Visualize
miss.visualize()


%% View Current
miss.visualize_current(final_wps)


%% Reset mission
final_wps = [];


%% Testing
last_wp = miss.waypoints(end,:);


%% Waypoints (should be good to go)
takeoff_wp = WP(22,15,0,0,1,0,0,100);
wps = WPMission([miss.launch_wps; miss.waypoints],miss.bounds,miss.obstacles);
final_wps = [takeoff_wp;wps];

last_wp = [wps(end).lat wps(end).lng wps(end).alt];


%% Drop target (wind testing)
% N-0  E-90  S-180  W-270
wind = 0;
wind_dir = 0;
drop_wps = DropMission(miss.dropPoint, last_wp, miss.bounds,miss.obstacles,wind,wind_dir);

last_wp = [drop_wps(end).lat drop_wps(end).lng drop_wps(end).alt];
final_wps = [final_wps;drop_wps];


%% Emergent (should be done)
emergent_wps = Emergent(miss.emergent, last_wp, miss.bounds, miss.obstacles);

last_wp = [emergent_wps(end).lat emergent_wps(end).lng emergent_wps(end).alt];
final_wps = [final_wps;emergent_wps];


%% Search Grid (lot of work)
% not right
search_wps = DropMission([last_wp; miss.emergent],miss.bounds,miss.obstacles);

last_wp = [search_wps(end).lat search_wps(end).lng search_wps(end).alt];
final_wps = [final_wps;search_wps];


%% Off Axis (not started)
offAxis_wps = OffAxis(miss.offAxis, last_wp, miss.bounds, miss.obstacles);

last_wp = [offAxis_wps(end-1).lat offAxis_wps(end-1).lng offAxis_wps(end-1).alt];
final_wps = [final_wps;offAxis_wps];


%% Landing (should be good to go)
landing_wps = Landing(miss.landing_point, last_wp, miss.bounds, miss.obstacles);
final_wps = [final_wps;landing_wps];


%% Convert to Lat/Long and Write to file (Should be done)
convertWPs(final_wps,miss.dropPoint)
printMission(final_wps,'../MissionPlanner/mission_File_1.txt')
done = 1
