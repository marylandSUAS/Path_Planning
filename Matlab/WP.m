classdef WP
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        id
        p1
        p2
        p3
        p4
        lat
        lng
        alt
    end
    
    methods
        function obj = WP(id,p1,p2,p3,p4,lat,lng,alt)
            
            obj.id = id;
            obj.p1 = p1;
            obj.p2 = p2;
            obj.p3 = p3;
            obj.p4 = p4;
            obj.lat = lat;
            obj.lng = lng;
            obj.alt = alt;
        end
        
        function strng = toString(obj)            
            strng = string(id)+" "+string(p1)+" "+string(p2)+" "+string(p3)
            +" "+string(p4)+" "+string(lat)+" "+string(lng)+" "+string(alt)
        end
        
        
        function meters_obj = toMeters(obj,GPS)
            start = GPS;
            rad_Earth = 20909000.0;
            dlng = (pi/180)*rad_Earth*cos(38.1459*pi/180);
            dlat = (pi/180)*rad_Earth;
            
            temp = obj;
            x = (obj.lat-start(2))*dlng;
            y = (obj.lng-start(1))*dlat;
            temp.lat = x;
            temp.lng = y;
            meters_obj = temp;
        end
        
        function meters_obj = toGPS(obj,GPS)
            start = GPS;
            rad_Earth = 20909000.0;
            dlng = (pi/180)*rad_Earth*cos(38.1459*pi/180);
            dlat = (pi/180)*rad_Earth;
            
            temp = obj;
            x = obj.lat/dlng+start(1);
            y = obj.lng/dlat+start(2);
            temp.lat = x;
            temp.lng = y;
            meters_obj = temp;
        end
                    
    end
end

