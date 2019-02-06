classdef mission
    % Mission definition
    
    properties
        launch_wps
        launch_gps
        
        waypoints
        bounds
        searchGrid
        dropPoint
        offAxis
        emergent
        obstacles
        
        waypoints_gps
        bounds_gps
        searchGrid_gps
        dropPoint_gps
        offAxis_gps
        emergent_gps
        obstacles_gps
        
        order
        grid_points
        grid_start_points
    end
    
    methods
        function obj = mission(location)
            format long
          
            file = location;
            if file == ' '
                file = '../missions/current_mission.txt';
            end
            
            data = importdata(file);
%             cellfun(@str2num,strsplit(data{k}{1},', '))
            obj.dropPoint_gps = cellfun(@str2num,strsplit(data{1},' '));
            obj.offAxis_gps = cellfun(@str2num,strsplit(data{2},' '));
            obj.emergent_gps = cellfun(@str2num,strsplit(data{3},' '));
            
            obj.launch_gps = [38.1451213 -76.4282048];
            obj.launch_wps = obj.toMeters(obj.launch_gps);
            launch_dist = 60;
            launch_theta = 0;
            obj.launch_wps = [obj.launch_wps; [obj.launch_wps(1)+launch_dist*cos(launch_theta) obj.launch_wps(2)+launch_dist*sin(launch_theta) 0]];
            
            
            temp = string(cell2mat(split(data{4},',')));
            temp2 = [];
            for a = 1:size(temp)
                temp2 = [temp2;cellfun(@str2num,strsplit(temp{a},' '))];
            end
            obj.waypoints_gps = temp2;
            
            temp = string(cell2mat(split(data{5},',')));
            temp2 = [];
            for a = 1:size(temp)
                temp2 = [temp2;cellfun(@str2num,strsplit(temp{a},' '))];
            end
            temp2 = [temp2; temp2(1,:)];
            obj.bounds_gps = temp2;
            
            temp = string(cell2mat(split(data{6},',')));
            temp2 = [];
            for a = 1:size(temp)
                temp2 = [temp2;cellfun(@str2num,strsplit(temp{a},' '))];
            end
            obj.searchGrid_gps = temp2;
            
            temp = string(cell2mat(split(data{7},',')));
            temp2 = [];
            for a = 1:size(temp)
                temp2 = [temp2;cellfun(@str2num,strsplit(temp{a},' '))];
            end
            obj.obstacles_gps = temp2;
            
            obj.dropPoint = obj.toMeters(obj.dropPoint_gps);
            obj.offAxis = obj.toMeters(obj.offAxis_gps);
            obj.emergent = obj.toMeters(obj.emergent_gps);
            
            obj.waypoints = [];
            for a = 1:size(obj.waypoints_gps,1)
                obj.waypoints = [obj.waypoints; obj.toMeters(obj.waypoints_gps(a,:))];
            end
            
            obj.bounds = [];
            for a = 1:size(obj.bounds_gps,1)
                obj.bounds = [obj.bounds; obj.toMeters(obj.bounds_gps(a,:))];
            end
            
            obj.searchGrid = [];
            for a = 1:size(obj.searchGrid_gps,1)
                obj.searchGrid = [obj.searchGrid; obj.toMeters(obj.searchGrid_gps(a,:))];
            end
            
            obj.obstacles = [];
            ob_bnd = [min(obj.bounds(:,1)) max(obj.bounds(:,1)) min(obj.bounds(:,2)) max(obj.bounds(:,2))];
            for k = 1:10
                obj.obstacles = [obj.obstacles; ob_bnd(1)+rand()*(ob_bnd(2)-ob_bnd(1)) ob_bnd(3)+rand()*(ob_bnd(4)-ob_bnd(3)) 100+650*rand() rand()*270+30];
            end
%             for a = 1:size(obj.obstacles_gps,1)
%                 obj.obstacles = [obj.obstacles; obj.toMeters(obj.obstacles_gps(a,:))];
%             end
            
            
            
        end
        
        function meters = toMeters(obj,GPS)
            start = obj.dropPoint_gps;
            rad_Earth = 20909000.0;
            dlng = (pi/180)*rad_Earth*cos(38.1459*pi/180);
            dlat = (pi/180)*rad_Earth;

            x = (GPS(2)-start(2))*dlng;
            y = (GPS(1)-start(1))*dlat;
            if length(GPS) < 3
                meters = [x,y,0];
            elseif length(GPS) > 3
                meters = [x,y,GPS(3:length(GPS))];
            else
                meters = [x,y,GPS(3)];
            end
            
            
        end
        
        function GPS = toGPS(obj,Meters) 
            start = obj.dropPoint_gps;
            rad_Earth = 20909000.0;
            dlng = (pi/180)*rad_Earth*cos(38.1459*pi/180);
            dlat = (pi/180)*rad_Earth;

            lng = (Meters(1)/dlng)+start(2);
            lat = (Meters(2)/dlat)+start(1);
            if length(Meters) < 3
                GPS = [lat,lng,0];
            elseif length(Meters) > 3
                GPS = [lat,lng,Meters(3:length(Meters))];
            else
                GPS = [lat,lng,Meters(3)];
            end
        end    
        
        
        function visualize(obj)
            figure;
            
            temp = obj.bounds;
            temp = [temp; temp(1,:)];
            plot(temp(:,1),temp(:,2),'r')
            hold on
%             scatter(obj.bounds(:,1),obj.bounds(:,2),'ro')
            
            plot(obj.waypoints(:,1),obj.waypoints(:,2),'b')
            scatter(obj.waypoints(:,1),obj.waypoints(:,2),'bo')
            scatter(obj.waypoints(1,1),obj.waypoints(1,2),'g','filled')
            
            temp = obj.searchGrid;
            temp = [temp; temp(1,:)];
            plot(temp(:,1),temp(:,2),'g')
            
            scatter(obj.dropPoint(1),obj.dropPoint(2),'y','filled')
            
            scatter(obj.offAxis(1),obj.offAxis(2),'b','filled')
            
            scatter(obj.emergent(1),obj.emergent(2),'or','filled')
            
            
            th = 0:pi/50:2*pi;
            for a = 1:size(obj.obstacles,1)
                xunit = obj.obstacles(a,4) * cos(th) + obj.obstacles(a,1);
                yunit = obj.obstacles(a,4) * sin(th) + obj.obstacles(a,2);
                plot(xunit, yunit,'r');
            end
            
%             axis([center(1)+sizing(1)/2 center(1)-sizing(1)/2 center(2)+sizing(2)/2 center(2)-sizing(2)/2])
            hold off
        end
    end
end

