%% start mission
miss = mission(' ');


%% Visualize

miss.visualize()

%% waypoints

takeoff_wp = WP(22,15,0,0,1,0,0,100);

wps = WPMission([miss.launch_wps; miss.waypoints],miss.bounds,miss.obstacles);
wps = wps(2:end);

last_wp = wps(end);



%% Drop target

last_wp = miss.waypoints(end,:);
wind = 0;
wind_dir = 0;
drop_wps = DropMission([last_wp; miss.dropPoint],miss.bounds,miss.obstacles,wind,wind_dir);

last_wp = drop_wps(end);


%% Emergent

emergent_wps = DropMission([last_wp; miss.emergent],miss.bounds,miss.obstacles);



%% Search Grid

search_wps = DropMission([last_wp; miss.emergent],miss.bounds,miss.obstacles);


%% Off Axis

offAxis_wps = DropMission([last_wp; miss.offAxis],miss.bounds,miss.obstacles);


%% Landing 



land_wp = WP(22,15,0,0,0,0,0,100);
