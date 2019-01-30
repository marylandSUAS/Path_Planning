%% start mission
miss = mission(' ');


%% Visualize

miss.visualize()

%% waypoints

takeoff_wp = WP(22,15,0,0,0,0,0,100);

wps = WPMission([miss.launch_wps; miss.waypoints],miss.bounds,miss.obstacles);
wps = wps(2:end);

%% Emergent

%% Drop target

%% Search Grid

%% Off Axis


%% Landing 

land_wp = WP(22,15,0,0,0,0,0,100);
