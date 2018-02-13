classdef moving_Object
    
    properties
        Nodes = [];
        Location = [0 0 0];
        Velocity = 0;
        direction = [0 0];
        AverageVel = 0;
        OnNode = 1;
        VelocityChange = 1;
    end
    
    methods
        function obj = addNodes(obj,Nodes)
            obj.Nodes = Nodes;
            obj.direction = [atan2((Nodes(size(Nodes,1),2)-Nodes(1,2)),(Nodes(size(Nodes,1),1)-Nodes(1,1))),atan2((Nodes(size(Nodes,1),3)-Nodes(1,3)),sqrt((Nodes(size(Nodes,1),1)-Nodes(1,1))^2+(Nodes(size(Nodes,1),2)-Nodes(1,2))^2))];
            for k = 2:size(Nodes,1)
                obj.direction  = [obj.direction; atan2((Nodes(k,2)-Nodes(k-1,2)),(Nodes(k,1)-Nodes(k-1,1))),atan2((Nodes(k,3)-Nodes(k-1,3)),sqrt((Nodes(k,1)-Nodes(k-1,1))^2+(Nodes(k,2)-Nodes(k-1,2))^2))]; %between node 1 and 2
            end
            obj.Location = Nodes(1,:);
        end
        
        function obj = setVel(obj,input1)
            obj.Velocity = input1;
            obj.AverageVel = input1;
        end
        
        function obj = Update(obj,time)
%             if(VelocityChange > 0)
                
%             end
            LocationNew = [obj.Location(1)+obj.Velocity*cos(obj.Direction(obj.OnNode,1))/time obj.Location(2)+obj.Velocity*sin(obj.Direction(obj.OnNode,1))/time obj.Location(3)+obj.Velocity*sin(obj.Direction(obj.OnNode,2))/time];
            if(0) % sqrt(()^2+()^2))%find if it has hit node)
                obj.OnNode = obj.OnNode+1;
                if (obj.OnNode > size(obj.Nodes,1))
                    obj.OnNode = 1;
                end
                LocationNew = Obj.Nodes(obj.OnNode);
                obj.Direction(obj.OnNode,:)
%                 obj.Velocity = velocity of that to next node
            end
            obj.Location = LocationNew;
%           
        end
        
        function plot(obj,alt)
            dif = 1-(abs(obj.Location(3)-alt)/100)
            if(dif < 0)
                dif = 0;
            end
            scatter(obj.Location(1),obj.Location(2),'MarkerFaceColor',[dif 1 1])
%             plot circle at loc
        end
    end
end

