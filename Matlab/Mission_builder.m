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

last_wp = wps(end);


%% Drop target (wind testing)
% N-0  E-90  S-180  W-270
wind = 0;
wind_dir = 0;
drop_wps = DropMission([last_wp; miss.dropPoint],miss.bounds,miss.obstacles,wind,wind_dir);

last_wp = drop_wps(end);


%% Emergent (should be done)
emergent_wps = Emergent(miss.emergent, last_wp, miss.bounds, miss.obstacles);


%% Search Grid (lot of work)
% not right
search_wps = DropMission([last_wp; miss.emergent],miss.bounds,miss.obstacles);


%% Off Axis (not started)
offAxis_wps = DropMission([last_wp; miss.offAxis],miss.bounds,miss.obstacles);


%% Landing (should be good to go)
landing_wps = Landing(miss.landing_point, last_wp, miss.bounds, miss.obstacles);


%% Convert to Lat/Long and Write to file (Should be done)
convertWps(final_wps,miss.dropPoint)
printMission(final_wps,'../MissionPlanner/mission_File_1.txt')

