classdef mission
    % Mission definition
    
    properties
        launch_wps
        launch_gps
        
        landing_point
        landing_gps
        
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

            obj.dropPoint_gps = [38.1458416667 -76.426375];
            obj.offAxis_gps = [38.1467472222 -76.4221305556];
            obj.emergent_gps = [38.1448833333 -76.4246277778];
            
            obj.launch_gps = [38.1451213 -76.4282048];
            obj.landing_gps = [38.1446914 -76.4279937];
            obj.launch_wps = obj.toMeters(obj.launch_gps);
            obj.landing_point = obj.toMeters(obj.landing_gps);
            
            launch_dist = 60;
            launch_theta = 0;
            obj.launch_wps = [obj.launch_wps; [obj.launch_wps(1)+launch_dist*cos(launch_theta) obj.launch_wps(2)+launch_dist*sin(launch_theta) 0]];
            
            
%             temp = string(cell2mat(split(data{4},',')));
%             temp = split(data{4},',');
%             temp2 = [];
%             for a = 1:size(temp)
%                 temp2 = [temp2;cellfun(@str2num,strsplit(temp{a},' '))];
%             end
%             
            
            temp2 = [38.1446916667 -76.4279944444 200.0;
                38.1461944444 -76.4237138889 300.0;
                38.1438972222 -76.42255 400.0;
                38.1417722222 -76.4251083333 400.0;
                38.14535 -76.428675 300.0;
                38.1508972222 -76.4292972222 300.0;
                38.1514944444 -76.4313833333 300.0;
                38.1505333333 -76.434175 300.0;
                38.1479472222 -76.4316055556 200.0;
                38.1443333333 -76.4322888889 200.0;
                38.1433166667 -76.4337111111 300.0;
                38.1410944444 -76.4321555556 400.0;
                38.1415777778 -76.4252472222 400.0;
                38.1446083333 -76.4282527778 200.0];
            temp2(:,3) = 0.3048*temp2(:,3);
            obj.waypoints_gps = temp2;
%             temp = string(cell2mat(split(data{5},',')));
%             temp = split(data{5},',');
%             temp2 = [];
%             for a = 1:size(temp)
%                 temp2 = [temp2;cellfun(@str2num,strsplit(temp{a},' '))];
%             end
%             temp2 = [temp2; temp2(1,:)];
            obj.bounds_gps = [38.146269 -76.428164;...
                              38.151625 -76.428683;...
                              38.151889 -76.431467;...
                              38.150594 -76.435361;...
                              38.147567 -76.432342;...
                              38.144667 -76.432947;...
                              38.143256 -76.434767;...
                              38.140464 -76.432636;...
                              38.140719 -76.426014;...
                              38.143761 -76.421206;...
                              38.147347 -76.423211;...
                              38.146131 -76.426653;...
                              38.146269 -76.428164];
            
%             temp = string(cell2mat(split(data{6},',')));
%             temp = split(data{6},',');
%             temp2 = [];
%             for a = 1:size(temp)
%                 temp2 = [temp2;cellfun(@str2num,strsplit(temp{a},' '))];
%             end
%             obj.searchGrid_gps = temp2;
            
%             temp = string(cell2mat(split(data{7},',')));
%             temp = split(data{7},',');
%             temp2 = [];
%             for a = 1:size(temp,1)
%                 temp2 = [temp2;cellfun(@str2num,strsplit(temp{a},' '))];
%             end
            
            temp2 = [38.146689 -76.426475 750.0 150.0;
                38.142914 -76.430297 300.0 300.0;
                38.149504 -76.43311 750.0 100.0;
                38.148711 -76.429061 750.0 300.0;
                38.144203 -76.426155 400.0 50.0;
                38.146003 -76.430733 500.0 225.0];
            temp2(:,3) = 0.3048*temp2(:,3);
            temp2(:,4) = 0.3048*temp2(:,4);
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
            randomize_obs = 0;
            if randomize_obs
                for k = 1:10
                    obj.obstacles = [obj.obstacles; ob_bnd(1)+rand()*(ob_bnd(2)-ob_bnd(1)) ob_bnd(3)+rand()*(ob_bnd(4)-ob_bnd(3)) 100+650*rand() rand()*150+30];%270+30];
                end
            else
                for a = 1:size(obj.obstacles_gps,1)
                    obj.obstacles = [obj.obstacles; obj.toMeters(obj.obstacles_gps(a,:))];
                end
            end
            
            
        end
        
        function visualize_current(obj, final_wps)
            obj.visualize()
            hold on
            temp_plot = [];
            for i = 1:length(final_wps)
                if(final_wps(i).id == 16 || final_wps(i).id == 21)
                    final_wps(i) = final_wps(i).toMeters(obj.dropPoint_gps);
                end
            end
            
            for i = 1:length(final_wps)
                if(final_wps(i).id == 16 || final_wps(i).id == 21)
                    temp_plot = [temp_plot; final_wps(i).lat final_wps(i).lng final_wps(i).alt];
            %     elseif(final_wps(i).id == 16)
            %         temp_scatter = [temp_scatter; final_wps(i).lat final_wps(i).lng final_wps(i).alt];
                end
            end
            plot(temp_plot(:,1),temp_plot(:,2))
            % scatter(temp_scatter(:,1),temp_scatter(:,2))
            axis([min(obj.bounds(:,1)) max(obj.bounds(:,1)) min(obj.bounds(:,2)) max(obj.bounds(:,2))])
            axis equal
            
        end
        
        
        function meters = toMeters(obj,GPS)
            start = obj.dropPoint_gps;
            rad_Earth = 6371000;
            dlng = (pi/180)*rad_Earth*cos(start(1)*pi/180);
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
            rad_Earth = 6371000;
            dlng = (pi/180)*rad_Earth*cos(start(1)*pi/180);
            dlat = (pi/180)*rad_Earth;

            lat = Meters(2)/dlat+start(1);
            lng = Meters(1)/dlng+start(2);

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
            
            scatter(obj.dropPoint(1),obj.dropPoint(2),'y','filled')
            hold on
            scatter(obj.offAxis(1),obj.offAxis(2),'b','filled')
            scatter(obj.emergent(1),obj.emergent(2),'or','filled')
            
            
            temp = obj.bounds;
            temp = [temp; temp(1,:)];
            plot(temp(:,1),temp(:,2),'r')
            scatter(obj.bounds(:,1),obj.bounds(:,2),'ro')
            
            plot(obj.waypoints(:,1),obj.waypoints(:,2),'b')
            scatter(obj.waypoints(:,1),obj.waypoints(:,2),'bo')
            scatter(obj.waypoints(1,1),obj.waypoints(1,2),'g','filled')
            
%             temp = obj.searchGrid;
%             temp = [temp; temp(1,:)];
%             plot(temp(:,1),temp(:,2),'g')
            
            plot_obs(obj.obstacles)
            
%             axis([center(1)+sizing(1)/2 center(1)-sizing(1)/2 center(2)+sizing(2)/2 center(2)-sizing(2)/2])
            legend('Drop Point','Off Axis','Emergent')
            hold off
            axis equal
            
        end
        
        function visualize_live(obj)            
            
            scatter(obj.dropPoint(1),obj.dropPoint(2),'y','filled')
            scatter(obj.offAxis(1),obj.offAxis(2),'b','filled')
            scatter(obj.emergent(1),obj.emergent(2),'or','filled')
            
            
            temp = obj.bounds;
            temp = [temp; temp(1,:)];
            plot(temp(:,1),temp(:,2),'r')
%             scatter(obj.bounds(:,1),obj.bounds(:,2),'ro')
            
            plot(obj.waypoints(:,1),obj.waypoints(:,2),'b')
%             scatter(obj.waypoints(:,1),obj.waypoints(:,2),'bo')
            scatter(obj.waypoints(1,1),obj.waypoints(1,2),'g','filled')
            
            temp = obj.searchGrid;
            temp = [temp; temp(1,:)];
            plot(temp(:,1),temp(:,2),'g')
            
            plot_obs(obj.obstacles)
            
        end
    end
end

