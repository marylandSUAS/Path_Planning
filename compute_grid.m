function [outputArg1,outputArg2] = compute_grid(obj,photo_coverage) 

    grid_point = obj.searchGrid(:,1:2);
    grid_point = [grid_point; grid_point(1,:)];

    longest_line = [1,0];
    for k = 2:size(grid_point,1)
        temp = hypot(grid_point(k,1)-grid_point(k-1,1),grid_point(k,2)-grid_point(k-1,2));
        if temp > longest_line(2)
            longest_line = [k,temp];
        end
    end
    grid_theta = -atan((grid_point(longest_line(1),2)-grid_point(longest_line(1)-1,2))/(grid_point(longest_line(1),1)-grid_point(longest_line(1)-1,1)))

    grid_rotated = [];
    for k = 1:size(grid_point,1)
        grid_rotated = [grid_rotated; ([cos(grid_theta) -sin(grid_theta); sin(grid_theta) cos(grid_theta)] * grid_point(k,:)')'];
    end


    topLeftPoint = 1;
    grid_dist = [0 0];
    for k = 1:size(grid_rotated,1)-1
        distX = grid_rotated(k,1)-grid_rotated(topLeftPoint,1);
        distY = grid_rotated(k,2)-grid_rotated(topLeftPoint,2);
        grid_dist(1) = sign(distX)*max([abs(grid_dist(1)) abs(distX)]);
        grid_dist(2) = sign(distY)*max([abs(grid_dist(2)) abs(distY)]);
    end




    num_points = [round(grid_dist(1)/photo_coverage(2))+1 abs(round(grid_dist(2)/photo_coverage(1)+.5))+1];

    Grid(1:num_points(1),1:num_points(2)) = Grid_Point();
    for k = 1:num_points(1)
        for j = 1:num_points(2)
            Grid(j,k).Location = [grid_rotated(topLeftPoint,1)+k*photo_coverage(2)-photo_coverage(2)/2
                                  photo_coverage(1)/2+grid_rotated(topLeftPoint,2)-j*photo_coverage(1)];
        end
    end

    inPloyPoints = [];
    k_limit = [inf 0];
    j_limit = [inf 0];
    for k = 1:num_points(1)
        for j = 1:num_points(2)
            if(Grid(j,k).inPoly(grid_rotated))
                if k < k_limit(1)
                    k_limit(1) = k;
                end
                if k > k_limit(2)
                    k_limit(2) = k;
                end
                if j < j_limit(1)
                    j_limit(1) = j;
                end
                if j > j_limit(2)
                    j_limit(2) = j;
                end
                Grid(j,k).in_que = 1;


            end
        end
    end

    if k_limit(2)-k_limit(1) < j_limit(2)-j_limit(1)
        max_limit = k_limit;
        min_limit = j_limit;
        a = 1


        finalPath = [];
        finalPath_points = [];
        for k = max_limit(1):2:max_limit(2)

            for j = min_limit(1):min_limit(2)
                if Grid(j,k).in_que == 1
                    finalPath_points = [finalPath_points;j k];
                    finalPath = [finalPath; Grid(j,k).Location'];
                    break
                end
            end
            temp = [0 0];
            for j = min_limit(1):min_limit(2)
                if Grid(j,k).in_que == 1
                    temp = [j k];
                end
            end
            finalPath_points = [finalPath_points; temp];
            finalPath = [finalPath; Grid(temp(1),temp(2)).Location'];

            if max_limit(2) >= k+1
                for j = min_limit(2):-1:min_limit(1)
                    if Grid(j,k+1).in_que == 1
                        finalPath_points = [finalPath_points;j k+1];
                        finalPath = [finalPath; Grid(j,k+1).Location'];
                        break
                    end 
                end

                temp = [0 0];
                for j = min_limit(2):-1:min_limit(1)
                    if Grid(j,k+1).in_que == 1
                        temp = [j k+1];

                    end 
                end
                finalPath_points = [finalPath_points;temp];
                finalPath = [finalPath; Grid(temp(1),temp(2)).Location'];
            end
        end
    else
        max_limit = j_limit
        min_limit = k_limit



        finalPath = [];
        finalPath_points = [];
        for j = max_limit(1):2:max_limit(2)

            for k = min_limit(1):min_limit(2)
                if Grid(j,k).in_que == 1
                    finalPath_points = [finalPath_points;j k];
                    finalPath = [finalPath; Grid(j,k).Location'];
                    break
                end
            end
            temp = [0 0];
            for k = min_limit(1):min_limit(2)
                if Grid(j,k).in_que == 1
                    temp = [j k];
                end
            end
            finalPath_points = [finalPath_points; temp];
            finalPath = [finalPath; Grid(temp(1),temp(2)).Location'];

            if max_limit(2) >= j+1
                for k = min_limit(2):-1:min_limit(1)
                    if Grid(j+1,k).in_que == 1
                        finalPath_points = [finalPath_points;j+1 k];
                        finalPath = [finalPath; Grid(j+1,k).Location'];
                        break
                    end 
                end

                temp = [0 0];
                for k = min_limit(2):-1:min_limit(1)
                    if Grid(j+1,k).in_que == 1
                        temp = [j+1 k];

                    end 
                end
                finalPath_points = [finalPath_points;temp];
                finalPath = [finalPath; Grid(temp(1),temp(2)).Location'];
            end
        end


    end

    final_loc = [];
    for k = 1:size(finalPath,1)
        final_loc = [final_loc; ([cos(-grid_theta) -sin(-grid_theta); sin(-grid_theta) cos(-grid_theta)] * finalPath(k,:)')'];
    end



    obj.grid_points = final_loc;
    disp('Number of wps: ')
    disp(length(finalPath))






    % Grid Points
    hold on
%             plot(grid_rotated(:,1),grid_rotated(:,2))
%             plot(inPloyPoints(:,1),inPloyPoints(:,2))
    plot(grid_point(:,1),grid_point(:,2))
    plot(final_loc(:,1),final_loc(:,2),'r')
    scatter(final_loc(:,1),final_loc(:,2),'r')



    axis equal
end


