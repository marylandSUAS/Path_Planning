%% start mission
% miss = mission(' ');
format long
miss = mission('../missions/test_mission_1.txt');
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

        
%% Test boundry
boundry_wps = [38.146269 -76.428164;
                38.151625 -76.428683;
                38.151889 -76.431467;
                38.150594 -76.435361;
                38.147567 -76.432342;
                38.144667 -76.432947;
                38.143256 -76.434767;
                38.140464 -76.432636;
                38.140719 -76.426014;
                38.143761 -76.421206;
                38.147347 -76.423211;
                38.146131 -76.426653;
                38.146269 -76.428164];
temp_wps = [];
for k = 1:size(boundry_wps,1)
    temp_wps = [temp_wps; miss.toMeters(boundry_wps(k,:))];
end
final_wps = [];
for k = 1:size(boundry_wps,1)
    final_wps = [final_wps; WP(16,0,0,0,0,temp_wps(k,1),temp_wps(k,2),0)];
end

%% Waypoints 
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


%% Emergent
emergent_wps = Emergent(miss.emergent, last_wp, miss.bounds, miss.obstacles);

last_wp = [emergent_wps(end).lat emergent_wps(end).lng emergent_wps(end).alt];
final_wps = [final_wps;emergent_wps];


%% Search Grid 
% not right
search_wps = SearchGrid(miss.searchGrid,last_wp,miss.bounds,miss.obstacles);

last_wp = [search_wps(end).lat search_wps(end).lng search_wps(end).alt];
final_wps = [final_wps;search_wps];


%% Off Axis
offAxis_wps = OffAxis(miss.offAxis, last_wp, miss.bounds, miss.obstacles);

last_wp = [offAxis_wps(end-1).lat offAxis_wps(end-1).lng offAxis_wps(end-1).alt];
final_wps = [final_wps;offAxis_wps];


%% Landing
landing_wps = Landing(last_wp,miss.dropPoint_gps, miss.bounds, miss.obstacles);
final_wps = [final_wps;landing_wps];


%% Convert to Lat/Long and Write to file
for i = 1:length(final_wps)
    if(final_wps(i).id == 16 || final_wps(i).id == 21)
        final_wps(i) = final_wps(i).toGPS(miss.dropPoint_gps);
    end
end
printMission(final_wps,'../MissionPlanner/mission_File_1.txt')
fprintf('Done\n')
