classdef Grid_Point
    
    properties
        
        Location
        Index
        in_que
        
    end
    
    methods    
        function obj = Grid_Point()
            obj.in_que = 0;
        end
        
        function dist = distance(obj,loc)
            dist = ((loc(1)-obj.Location(1))^2+(loc(2)-obj.Location(2))^2)^.5;
        end
            
        function yes = inPoly(obj,pts)
            intersections = 0;
            for k = 2:size(pts,1)
                bl = [pts(k,1)-pts(k-1,1) pts(k,2)-pts(k-1,2)];
                bp = [pts(k-1,1) pts(k-1,2)];
                t = (obj.Location(2)-bp(2))/bl(2);
                if(t > 0 && t < 1)
                    t2 = t*bl(1)+bp(1)-obj.Location(1);
                    if(t2 > 0)
                        intersections = intersections+1;
                    end
                end    
            end   
            yes = rem(intersections,2);
        end
        
    end
end
