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
        state
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
            obj.state = 0; %0 = Meters, 1 = GPS
        end
        
        function strng = toString(obj)            
            strng = string(obj.id)+" "+string(obj.p1)+" "+string(obj.p2)+" "+string(obj.p3)+" "+string(obj.p4)+" "+string(obj.lat)+" "+string(obj.lng)+" "+string(obj.alt);
        end
        
        function meters_obj = toMeters(obj,GPS)
            rad_Earth = 6371000;
            dlng = (pi/180)*rad_Earth*cos(GPS(1)*pi/180);
            dlat = (pi/180)*rad_Earth;
            
            temp = obj;
            if obj.state == 1
                x = (obj.lat-GPS(1))*dlng;
                y = (obj.lng-GPS(2))*dlat;
                temp.lat = x;
                temp.lng = y;
                temp.state = 0;
            end
            meters_obj = temp;
        end
        
        
        
        function meters_obj = toGPS(obj,GPS)
            
            rad_Earth = 6371000;
            dlng = (pi/180)*rad_Earth*cos(GPS(1)*pi/180);
            dlat = (pi/180)*rad_Earth;
            
            temp = obj;
            if obj.state == 0
                x = obj.lng/dlat;
                y = obj.lat/dlng;
                temp.lat = x+GPS(1);
                temp.lng = y+GPS(2);
                temp.state = 1;
            end
            meters_obj = temp;
        end
                    
    end
end

