classdef moving_Object
    
    properties
        Nodes
        OnNode = 2;
        PrevNode = 1;
        Radius = 1;
        
        Location = [0 0 0];
        Velocity = 0;
        
        direction = [0 0];
        CurrentNode = [];
        
        AverageVel = 0;
        VelocityChange = 1;
    end
    
    methods
        function obj = setup(obj,Nodes1, input1, input2)
            obj.Radius = input2;
            obj.Nodes = Nodes1;
            obj.Location = Nodes1(1,:);
            obj.CurrentNode = Nodes1(obj.OnNode,:);
            
            dx = Nodes1(obj.OnNode,1)-Nodes1(obj.PrevNode,1);
            dy = Nodes1(obj.OnNode,2)-Nodes1(obj.PrevNode,2);
            dz = Nodes1(obj.OnNode,3)-Nodes1(obj.PrevNode,3);
            obj.direction = [atan2(dy,dx),atan2(dz,sqrt((dx)^2+(dy)^2))];
            
            obj.Velocity = input1;
            obj.AverageVel = input1;
        end
        
        function obj = Update(obj,time)
%             if(VelocityChange > 0)
                
%             end
            
            LocationNew = [obj.Location(1)+obj.Velocity*cos(obj.direction(1))*time obj.Location(2)+obj.Velocity*sin(obj.direction(1))*time obj.Location(3)+obj.Velocity*sin(obj.direction(2))*time];
            
            if(sqrt((obj.Location(1)-obj.Nodes(obj.OnNode,1))^2+(obj.Location(2)-obj.Nodes(obj.OnNode,2))^2) < 2)
                obj.PrevNode = obj.OnNode;
                obj.OnNode = obj.OnNode+1;
                if (obj.OnNode > size(obj.Nodes,1))
                    obj.OnNode = 1;
                end
                LocationNew = obj.Nodes(obj.PrevNode,:);
                
                dx = (obj.Nodes(obj.OnNode,1)-obj.Nodes(obj.PrevNode,1));
                dy = (obj.Nodes(obj.OnNode,2)-obj.Nodes(obj.PrevNode,2));
                dz = (obj.Nodes(obj.OnNode,3)-obj.Nodes(obj.PrevNode,3));
                
                direc = [atan2(dy,dx) atan2(dz,sqrt((dx)^2+(dy)^2))];
                obj.direction = direc;
            end
            obj.Location = LocationNew;
            
        end
        
        function plot(obj,alt)
            
            dif = 1-(abs(obj.Location(3)-alt)/100);
            if(dif < 0)
                dif = 0;
            end
%             scatter(obj.Location(1),obj.Location(2),'MarkerFaceColor',[dif 1-dif .5],'MarkerSize',obj.Radius)
            viscircles([obj.Location(1),obj.Location(2)],obj.Radius,'Color',[dif 1-dif .5]);
        end
        
        function print(obj)
            
            
        end
    end
end

