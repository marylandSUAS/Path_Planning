function varargout = Flightpath_Display(varargin)
% FLIGHTPATH_DISPLAY MATLAB code for Flightpath_Display.fig
%      FLIGHTPATH_DISPLAY, by itself, creates a new FLIGHTPATH_DISPLAY or raises the existing
%      singleton*.
%
%      H = FLIGHTPATH_DISPLAY returns the handle to a new FLIGHTPATH_DISPLAY or the handle to
%      the existing singleton*.
% 
%      FLIGHTPATH_DISPLAY('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in FLIGHTPATH_DISPLAY.M with the given input arguments.
%
%      FLIGHTPATH_DISPLAY('Property','Value',...) creates a new FLIGHTPATH_DISPLAY or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Flightpath_Display_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Flightpath_Display_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Flightpath_Display

% Last Modified by GUIDE v2.5 16-Feb-2018 23:33:54

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Flightpath_Display_OpeningFcn, ...
                   'gui_OutputFcn',  @Flightpath_Display_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT

% --- Executes just before Flightpath_Display is made visible.
function Flightpath_Display_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Flightpath_Display (see VARARGIN)

% Set up path variables
clc;
handles.cf = handles.current_path_axes;
handles.ca = handles.current_path_axes;
handles.current_path_axes = handles.ca;
handles.missionDirectory = 'C:\Users\mvaug\Documents\SUAS\SUAS-Path-Finding\dlite';
handles.shortest_path_path = strcat(handles.missionDirectory,'\shortest_path.txt');
handles.flight_information_path = strcat(handles.missionDirectory,'\flight_information.txt');
handles.intermediate_waypoints_path = strcat(handles.missionDirectory,'\intermediate_waypoints.txt');

% Choose default command line output for Flightpath_Display
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Flightpath_Display wait for user response (see UIRESUME)
% uiwait(handles.figure1);

function kill_dstar(eventdata,handles)
flight_information_handle = fopen(handles.flight_information_path,'r');
updated = fgets(flight_information_handle);
updated = 'Update 2\n';
goal = fgets(flight_information_handle);
start = fgets(flight_information_handle);
current = fgets(flight_information_handle);
obstacle_index = 0;
line = fgets(flight_information_handle);
while line ~= -1
    obstacle_index = obstacle_index + 1;
    obstacles{obstacle_index} = line;
    line = fgets(flight_information_handle);
end
fclose(flight_information_handle);
flight_information_handle = fopen(handles.flight_information_path,'w');
fprintf(flight_information_handle,updated);
fprintf(flight_information_handle,goal);
fprintf(flight_information_handle,start);
fprintf(flight_information_handle,current);
for i = [1:1:obstacle_index]
    fprintf(flight_information_handle,obstacles{i});
end
fclose(flight_information_handle);
mode_list_Callback(handles.mode_list,eventdata,handles);

function plot_data(handles)
% Create file handles
flight_information_handle = fopen(handles.flight_information_path);
shortest_path_handle = fopen(handles.shortest_path_path);
waypoints_handle = fopen(handles.intermediate_waypoints_path);

% Wait until algorithm is done processing new path before continuing
changed = 0;
start_t = tic;
while(changed == '0' && toc(start_t) < 15)
    shortest_path_handle = fopen(handles.shortest_path_path);
    pause(0.1);
    changed = sscanf(fgets(shortest_path_handle),'Changed %s');
    fclose(shortest_path_handle);
end
shortest_path_handle = fopen(handles.shortest_path_path);
changed = sscanf(fgets(shortest_path_handle),'Changed %s');
% Extract data for start, goal and current nodes, and obstacle
% locations.
path_data = fscanf(shortest_path_handle,'%f',[3,inf])';
if(isempty(path_data))
    path_data = [0.0 0.0 0.0];
end
updated = textscan(fgets(flight_information_handle),'%s %d');
updated = updated{2};
goal = textscan(fgets(flight_information_handle),'%s %f %f %f');
goal = [goal{2},goal{3},goal{4}];
handles.goal = goal;
start = textscan(fgets(flight_information_handle),'%s %f %f %f');
start = [start{2},start{3},start{4}];
handles.start = start;
current = textscan(fgets(flight_information_handle),'%s %f %f %f');
current = [current{2},current{3},current{4}];
obstacle_index = 0;
line = fgets(flight_information_handle);
while line ~= -1
    obstacle_index = obstacle_index + 1;
    newline = textscan(line,'%s');
    obstacle_type{obstacle_index} = newline{1}(1);
    if strcmp(newline{1}(1),'moving')
        newline = textscan(line,'%s %f %f %f %f %f %f %f');
        % moving obstacles are [x,y,z,r,velx,vely,velz];
        obstacles{obstacle_index} = [newline{2},newline{3},newline{4},newline{8},newline{5},newline{6},newline{7}];
    else
        newline = textscan(line,'%s %f %f %f %f');
        obstacles{obstacle_index} = [newline{2},newline{3},newline{4},newline{5}];
        obstacle_type{obstacle_index} = newline{1};
    end
    line = fgets(flight_information_handle);
end

% Plot obstacles as cylinders or spheres, and start, goal and current nodes as
% spheres.
axes(handles.current_path_axes);
cla(handles.current_path_axes);
shading FLAT;
hold on;
handles.node_path = plot3(path_data(:,1),path_data(:,2),path_data(:,3)); % Plot raw path data.
% Plot obstacles.
for i = [1:1:obstacle_index]
    switch string(obstacle_type{i})
        case 'static'
            [x,y,z] = cylinder(obstacles{i}(4),10);
%             surf(x+obstacles(i,1),y+obstacles(i,2),z+40,'FaceColor',[0.85 0.6 0]);
%             for z_inc = [40:1:obstacles(i,3)]
            surf(x+obstacles{i}(1),y+obstacles{i}(2),z*obstacles{i}(3),'FaceColor','none','EdgeColor',[0.8 0.8 0.8]);
%             end
%             surf(x+obstacles(i,1),y+obstacles(i,2),z+obstacles(i,3),'FaceColor',[0.85 0.6 0]);
        case 'dynamic'
            [x,y,z] = sphere(10);
            surf(x*obstacles{i}(4)+obstacles{i}(1),y*obstacles{i}(4)+obstacles{i}(2),z*obstacles{i}(4)+obstacles{i}(3),'FaceColor','none','EdgeColor',[0.8 0.8 0.8]);
        case 'moving'
            [x,y,z] = sphere(10);
            surf(x*obstacles{i}(4)+obstacles{i}(1),y*obstacles{i}(4)+obstacles{i}(2),z*obstacles{i}(4)+obstacles{i}(3),'FaceColor','none','EdgeColor',[0.8 0.8 0.8]);
    end
end
view(-(0.5-handles.az_slider.Value)*270,-(0.5-handles.elev_slider.Value)*270);
% Plot start, goal, current nodes.
handles.diag_dist = norm(goal-start);
handles.wp_rad = handles.diag_dist/75;
wp_rad = handles.wp_rad;
[x,y,z] = sphere(10);
surf(x*wp_rad+start(1),y*wp_rad+start(2),z*wp_rad+start(3),'FaceColor','none','EdgeColor',[0.5 0 0]);
surf(x*wp_rad+goal(1),y*wp_rad+goal(2),z*wp_rad+goal(3),'FaceColor','none','EdgeColor',[0 0.5 0]);
surf(x*wp_rad+current(1),y*wp_rad+current(2),z*wp_rad+current(3),'FaceColor',[0.6 0.6 0.9]);
axis equal;
grid on;
hold off;
plot_grid_obstacles(handles);
plot_intermediate_waypoints(handles);
% plot_boundary(handles);
% axis([min(start(1),goal(1)),max(start(1),goal(1)),min(start(2),goal(2)),max(start(2),goal(2)),min(start(3),goal(3)),max(start(3),goal(3))]);
fclose(flight_information_handle);
fclose(shortest_path_handle);
fclose(waypoints_handle);

function plot_boundary(handles)
boundary_handle = fopen(strcat(handles.missionDirectory,'\boundary.txt'));
line = fgets(boundary_handle);
boundary_index = 0;
while(line ~= -1)
    boundary_index = boundary_index+1;
    boundary_vert = textscan(line,'%f %f');
    boundary_vert_lst(boundary_index,:) = [boundary_vert{1} boundary_vert{2}];
    line = fgets(boundary_handle);
end
if boundary_index > 0
    axes(handles.current_path_axes);
    hold on;
    plot3(boundary_vert_lst(:,1),boundary_vert_lst(:,2),40.0*ones(boundary_index,1));
    plot3(boundary_vert_lst(:,1),boundary_vert_lst(:,2),230.0*ones(boundary_index,1));
    hold off
end

function plot_grid_obstacles(handles)
pause(0.01);
blocks_handle = fopen(strcat(handles.missionDirectory,'\3D_blocks.txt'));
line = fgets(blocks_handle);
grid_obstacle_index = 0;
while(line ~= -1)
    grid_obstacle_index = grid_obstacle_index + 1;
    grid_obst = textscan(line,'[%f %f %f] [%f %f %f]');
    grid_obst_list(grid_obstacle_index,:) = [grid_obst{1} grid_obst{2} grid_obst{3} grid_obst{4} grid_obst{5} grid_obst{6}];
    line = fgets(blocks_handle);
end
axes(handles.current_path_axes);
hold on;
for i = [1:1:grid_obstacle_index]
    l = grid_obst_list(i,4);
    w = grid_obst_list(i,5);
    h = grid_obst_list(i,6);
    x = grid_obst_list(i,1)-l/2;
    y = grid_obst_list(i,2)-w/2;
    z = grid_obst_list(i,3)-h/2;
    vertices = [x y z;x+l y z;x y+w z;x y z+h;x+l y+w z;x+l y z+h;x y+w z+h;x+l y+w z+h];
    faces = [1 2 3 4;2 6 7 3;4 3 7 8;1 5 8 4;1 2 6 5;5 6 7 8];
    patch('Vertices',vertices,'Faces',faces,'FaceColor','g');
end
hold off;

function plot_intermediate_waypoints(handles)
pause(0.5);
wps_handle = fopen(strcat(handles.missionDirectory,'\intermediate_waypoints.txt'));
line = fgets(wps_handle);
line = fgets(wps_handle);
wps_list = [];
wps_index = 0;
while(line ~= -1)
    wps_index = wps_index + 1;
    wps = textscan(line,'%f %f %f');
    wps_list(wps_index,:) = [wps{1} wps{2} wps{3}];
    line = fgets(wps_handle);
end
axes(handles.current_path_axes);
hold on;
for i = [1:1:wps_index]
    [x,y,z] = sphere(10);
    plot3(x*handles.wp_rad+wps_list(i,1),y*handles.wp_rad+wps_list(i,2),z*handles.wp_rad+wps_list(i,3));
end
wps_list = [handles.start;wps_list;handles.goal];
handles.int_wp = plot3(wps_list(:,1),wps_list(:,2),wps_list(:,3));
hold off;
% % Set up figure for paper:
% newfig = figure;
% copyobj(handles.ca,newfig);
% ax2 = gca;
% fnew = figure;
% ax1_copy = copyobj(handles.ca,fnew);
% s1 = subplot(2,1,1,ax1_copy);
% copies = copyobj(ax2,fnew);
% ax2_copy = copies(1);
% s2 = subplot(2,1,2,ax2_copy);
% % Start editing figure properties:
% figure(fnew);
% axes(ax1_copy);
% title('Shortest Path around Static Obstacles');
% xlabel('X[m]','fontsize',8);
% ylabel('Y[m]','fontsize',8);
% axis([-50 50 -250 15 0 250]);
% view([270 90]);
% XL = get(s1, 'XLim');
% YL = get(s1, 'YLim');
% patch([XL(1), XL(2), XL(2), XL(1)], [YL(1), YL(1), YL(2), YL(2)], [0 0 0 0], 'FaceColor', [0.75 0.75 0.75]);
% axes(ax2_copy)
% xlabel('X[m]','fontsize',8);
% ylabel('Y[m]','fontsize',8);
% zlabel('Z[m]','fontsize',8);
% axis([-50 50 -250 15 0 250]);
% view([270 20]);
% XL = get(s2, 'XLim');
% YL = get(s2, 'YLim');
% patch([XL(1), XL(2), XL(2), XL(1)], [YL(1), YL(1), YL(2), YL(2)], [0 0 0 0], 'FaceColor', [0.75 0.75 0.75]);
% clf(handles.cf); close(handles.cf);
% clf(newfig); close(newfig);

% --- Outputs from this function are returned to the command line.
function varargout = Flightpath_Display_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

% --- Executes on selection change in obstacle_gps_locations.
function obstacle_gps_locations_Callback(hObject, eventdata, handles)
% hObject    handle to obstacle_gps_locations (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns obstacle_gps_locations contents as cell array
%        contents{get(hObject,'Value')} returns selected item from obstacle_gps_locations


% --- Executes during object creation, after setting all properties.
function obstacle_gps_locations_CreateFcn(hObject, eventdata, handles)
% hObject    handle to obstacle_gps_locations (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: listbox controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function format_coord(handle)
if(~contains(handle.String,'.'))
    set(handle,'String',[handle.String '.0']);
end

% --- Executes on button press in start_button.
function start_button_Callback(hObject, eventdata, handles)
% hObject    handle to start_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% do a lot of other stuff here
if strcmp(handles.start_button.String,'START') == 1
    mode = handles.mode_list.Value;
    if(mode ~= 2)
        return
    end
    !make
    !main.exe &
    % ... doing stuff ...
    plot_data(handles);
    handles.start_button.String = 'STOP';
else
    kill_dstar(eventdata,handles);
    handles.start_button.String = 'START';
end

% --- Executes on selection change in mode_list.
function mode_list_Callback(hObject, eventdata, handles)
% hObject    handle to mode_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns mode_list contents as cell array
%        contents{get(hObject,'Value')} returns selected item from mode_list
mode = handles.mode_list.Value;
if(mode == 2)
    flight_information_handle = fopen(handles.flight_information_path);
    updated = textscan(fgets(flight_information_handle),'%s %d');
    updated = updated{2};
    goal = textscan(fgets(flight_information_handle),'%s %f %f %f');
    goal = [goal{2},goal{3},goal{4}];
    start = textscan(fgets(flight_information_handle),'%s %f %f %f');
    start = [start{2},start{3},start{4}];
    current = textscan(fgets(flight_information_handle),'%s %f %f %f');
    current = [current{2},current{3},current{4}];
    obstacle_index = 0;
    line = fgets(flight_information_handle);
    while line ~= -1
        obstacle_index = obstacle_index + 1;
        newline = textscan(line,'%s');
        if strcmp(newline{1}(1),'moving')
            newline = textscan(line,'%s %f %f %f %f %f %f %f');
            obstacles(obstacle_index,:) = [newline{2},newline{3},newline{4},newline{8},newline{5},newline{6},newline{7}];
        else
            newline = textscan(line,'%s %f %f %f %f');
            obstacles(obstacle_index,:) = [newline{2},newline{3},newline{4},newline{5}];
        end
        line = fgets(flight_information_handle);
    end
    set(handles.glat,'String',goal(1)); set(handles.glon,'String',goal(2)); set(handles.galt,'String',goal(3));
    set(handles.slat,'String',start(1)); set(handles.slon,'String',start(2)); set(handles.salt,'String',start(3));
    set(handles.clat,'String',current(1)); set(handles.clon,'String',current(2)); set(handles.calt,'String',current(3));
    current_list = '';
    for i = [1:1:obstacle_index]
        data = handles.obstacle_gps_locations;
        current_obstacle = [num2str(i) ') ['];
        for k = [1:1:3]
            coord = num2str(obstacles(i,k),11);
            current_obstacle = [current_obstacle coord];
            current_obstacle = [current_obstacle ', '];
        end
        current_obstacle = [current_obstacle num2str(obstacles(i,4),11) ']'];
        current_list = strvcat(current_list,current_obstacle);
        data.String = current_list;
    end
    fclose(flight_information_handle);
end

% --- Executes during object creation, after setting all properties.
function mode_list_CreateFcn(hObject, eventdata, handles)
% hObject    handle to mode_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in select_image_list.
function select_image_list_Callback(hObject, eventdata, handles)
% hObject    handle to select_image_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns select_image_list contents as cell array
%        contents{get(hObject,'Value')} returns selected item from select_image_list


% --- Executes during object creation, after setting all properties.
function select_image_list_CreateFcn(hObject, eventdata, handles)
% hObject    handle to select_image_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on slider movement.
function az_slider_Callback(hObject, eventdata, handles)
% hObject    handle to az_slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
axes(handles.current_path_axes);
view(-(0.5-handles.az_slider.Value)*270,-(0.5-handles.elev_slider.Value)*270);
% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function az_slider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to az_slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function elev_slider_Callback(hObject, eventdata, handles)
% hObject    handle to elev_slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
axes(handles.current_path_axes);
view(-(0.5-handles.az_slider.Value)*270,-(0.5-handles.elev_slider.Value)*270);
% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function elev_slider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to elev_slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on button press in set_start_button.
function set_start_button_Callback(hObject, eventdata, handles)
% hObject    handle to set_start_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

flight_information_handle = fopen(handles.flight_information_path,'r');
updated = fgets(flight_information_handle);
goal = fgets(flight_information_handle);
start = fgets(flight_information_handle);
current = fgets(flight_information_handle);
obstacle_index = 0;
line = fgets(flight_information_handle);
while line ~= -1
    obstacle_index = obstacle_index + 1;
    obstacles{obstacle_index} = line;
    line = fgets(flight_information_handle);
end
fclose(flight_information_handle);
flight_information_handle = fopen(handles.flight_information_path,'w');
start_x = handles.test_start_x.String;
start_y = handles.test_start_y.String;
start_z = handles.test_start_z.String;
set_start = ['start ' start_x ' ' start_y ' ' start_z '\n'];
fprintf(flight_information_handle,updated);
fprintf(flight_information_handle,goal);
fprintf(flight_information_handle,set_start);
fprintf(flight_information_handle,current);
for i = [1:1:obstacle_index]
    fprintf(flight_information_handle,obstacles{i});
end
fclose(flight_information_handle);
mode_list_Callback(handles.mode_list,eventdata,handles);


% --- Executes on button press in set_goal_button.
function set_goal_button_Callback(hObject, eventdata, handles)
% hObject    handle to set_goal_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
flight_information_handle = fopen(handles.flight_information_path,'r');
updated = fgets(flight_information_handle);
goal = fgets(flight_information_handle);
start = fgets(flight_information_handle);
current = fgets(flight_information_handle);
obstacle_index = 0;
line = fgets(flight_information_handle);
while line ~= -1
    obstacle_index = obstacle_index + 1;
    obstacles{obstacle_index} = line;
    line = fgets(flight_information_handle);
end
fclose(flight_information_handle);
flight_information_handle = fopen(handles.flight_information_path,'w');
goal_x = handles.test_goal_x.String;
goal_y = handles.test_goal_y.String;
goal_z = handles.test_goal_z.String;
set_goal = ['goal ' goal_x ' ' goal_y ' ' goal_z '\n'];
fprintf(flight_information_handle,updated);
fprintf(flight_information_handle,set_goal);
fprintf(flight_information_handle,start);
fprintf(flight_information_handle,current);
for i = [1:1:obstacle_index]
    fprintf(flight_information_handle,obstacles{i});
end
fclose(flight_information_handle);
mode_list_Callback(handles.mode_list,eventdata,handles);

% --- Executes on button press in set_current_button.
function set_current_button_Callback(hObject, eventdata, handles)
% hObject    handle to set_current_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
flight_information_handle = fopen(handles.flight_information_path,'r');
updated = fgets(flight_information_handle);
goal = fgets(flight_information_handle);
start = fgets(flight_information_handle);
current = fgets(flight_information_handle);
obstacle_index = 0;
line = fgets(flight_information_handle);
while line ~= -1
    obstacle_index = obstacle_index + 1;
    obstacles{obstacle_index} = line;
    line = fgets(flight_information_handle);
end
fclose(flight_information_handle);
flight_information_handle = fopen(handles.flight_information_path,'w');
current_x = handles.test_current_x.String;
current_y = handles.test_current_y.String;
current_z = handles.test_current_z.String;
set_current = ['current ' current_x ' ' current_y ' ' current_z '\n'];
fprintf(flight_information_handle,updated);
fprintf(flight_information_handle,goal);
fprintf(flight_information_handle,start);
fprintf(flight_information_handle,set_current);
for i = [1:1:obstacle_index]
    fprintf(flight_information_handle,obstacles{i});
end
fclose(flight_information_handle);
mode_list_Callback(handles.mode_list,eventdata,handles);

% --- Executes on button press in reset_test_button.
function reset_test_button_Callback(hObject, eventdata, handles)
% hObject    handle to reset_test_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
flight_information_handle = fopen(handles.flight_information_path,'w');
set_updated = ['updated_obstacles 1\n'];
set_goal = ['goal 25.0 25.0 85.0\n'];
set_start = ['start 2.0 2.0 45.0\n'];
set_current = ['current 2.0 2.0 45.0\n'];
% add_obstacle = ['dynamic 12.5 12.5 65.0 2.5\n'];
fprintf(flight_information_handle,set_updated);
fprintf(flight_information_handle,set_goal);
fprintf(flight_information_handle,set_start);
fprintf(flight_information_handle,set_current);
% fprintf(flight_information_handle,add_obstacle);
fclose(flight_information_handle);
mode_list_Callback(handles.mode_list,eventdata,handles);

plot_data(handles);

function test_start_x_Callback(hObject, eventdata, handles)
% hObject    handle to test_start_x (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of test_start_x as text
%        str2double(get(hObject,'String')) returns contents of test_start_x as a double
format_coord(handles.test_start_x)


% --- Executes during object creation, after setting all properties.
function test_start_x_CreateFcn(hObject, eventdata, handles)
% hObject    handle to test_start_x (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function test_start_y_Callback(hObject, eventdata, handles)
% hObject    handle to test_start_y (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of test_start_y as text
%        str2double(get(hObject,'String')) returns contents of test_start_y as a double
format_coord(handles.test_start_y)


% --- Executes during object creation, after setting all properties.
function test_start_y_CreateFcn(hObject, eventdata, handles)
% hObject    handle to test_start_y (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function test_start_z_Callback(hObject, eventdata, handles)
% hObject    handle to test_start_z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of test_start_z as text
%        str2double(get(hObject,'String')) returns contents of test_start_z as a double
format_coord(handles.test_start_z)


% --- Executes during object creation, after setting all properties.
function test_start_z_CreateFcn(hObject, eventdata, handles)
% hObject    handle to test_start_z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function test_goal_x_Callback(hObject, eventdata, handles)
% hObject    handle to test_goal_x (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of test_goal_x as text
%        str2double(get(hObject,'String')) returns contents of test_goal_x as a double
format_coord(handles.test_goal_x)




% --- Executes during object creation, after setting all properties.
function test_goal_x_CreateFcn(hObject, eventdata, handles)
% hObject    handle to test_goal_x (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function test_goal_y_Callback(hObject, eventdata, handles)
% hObject    handle to test_goal_y (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of test_goal_y as text
%        str2double(get(hObject,'String')) returns contents of test_goal_y as a double
format_coord(handles.test_goal_y)


% --- Executes during object creation, after setting all properties.
function test_goal_y_CreateFcn(hObject, eventdata, handles)
% hObject    handle to test_goal_y (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function test_goal_z_Callback(hObject, eventdata, handles)
% hObject    handle to test_goal_z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of test_goal_z as text
%        str2double(get(hObject,'String')) returns contents of test_goal_z as a double
format_coord(handles.test_goal_z)


% --- Executes during object creation, after setting all properties.
function test_goal_z_CreateFcn(hObject, eventdata, handles)
% hObject    handle to test_goal_z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function test_current_x_Callback(hObject, eventdata, handles)
% hObject    handle to test_current_x (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of test_current_x as text
%        str2double(get(hObject,'String')) returns contents of test_current_x as a double
format_coord(handles.test_current_x)


% --- Executes during object creation, after setting all properties.
function test_current_x_CreateFcn(hObject, eventdata, handles)
% hObject    handle to test_current_x (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function test_current_y_Callback(hObject, eventdata, handles)
% hObject    handle to test_current_y (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of test_current_y as text
%        str2double(get(hObject,'String')) returns contents of test_current_y as a double
format_coord(handles.test_current_y)


% --- Executes during object creation, after setting all properties.
function test_current_y_CreateFcn(hObject, eventdata, handles)
% hObject    handle to test_current_y (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function test_current_z_Callback(hObject, eventdata, handles)
% hObject    handle to test_current_z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of test_current_z as text
%        str2double(get(hObject,'String')) returns contents of test_current_z as a double
format_coord(handles.test_current_z)


% --- Executes during object creation, after setting all properties.
function test_current_z_CreateFcn(hObject, eventdata, handles)
% hObject    handle to test_current_z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function add_obstacle_x_Callback(hObject, eventdata, handles)
% hObject    handle to add_obstacle_x (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of add_obstacle_x as text
%        str2double(get(hObject,'String')) returns contents of add_obstacle_x as a double
format_coord(handles.add_obstacle_x)


% --- Executes during object creation, after setting all properties.
function add_obstacle_x_CreateFcn(hObject, eventdata, handles)
% hObject    handle to add_obstacle_x (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function add_obstacle_y_Callback(hObject, eventdata, handles)
% hObject    handle to add_obstacle_y (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of add_obstacle_y as text
%        str2double(get(hObject,'String')) returns contents of add_obstacle_y as a double
format_coord(handles.add_obstacle_y)


% --- Executes during object creation, after setting all properties.
function add_obstacle_y_CreateFcn(hObject, eventdata, handles)
% hObject    handle to add_obstacle_y (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function add_obstacle_z_Callback(hObject, eventdata, handles)
% hObject    handle to add_obstacle_z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of add_obstacle_z as text
%        str2double(get(hObject,'String')) returns contents of add_obstacle_z as a double
format_coord(handles.add_obstacle_z)


% --- Executes during object creation, after setting all properties.
function add_obstacle_z_CreateFcn(hObject, eventdata, handles)
% hObject    handle to add_obstacle_z (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


function add_obstacle_r_Callback(hObject, eventdata, handles)
% hObject    handle to add_obstacle_r (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of add_obstacle_r as text
%        str2double(get(hObject,'String')) returns contents of add_obstacle_r as a double
format_coord(handles.add_obstacle_r)


% --- Executes during object creation, after setting all properties.
function add_obstacle_r_CreateFcn(hObject, eventdata, handles)
% hObject    handle to add_obstacle_r (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in add_obstacle_button.
function add_obstacle_button_Callback(hObject, eventdata, handles)
% hObject    handle to add_obstacle_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
flight_information_handle = fopen(handles.flight_information_path,'r');
while(~flight_information_handle)
    flight_information_handle = fopen(handles.flight_information_path,'r');
end
updated = fgets(flight_information_handle);
updated = 'Update 1\n';
goal = fgets(flight_information_handle);
start = fgets(flight_information_handle);
current = fgets(flight_information_handle);
obstacle_index = 0;
line = fgets(flight_information_handle);
while line ~= -1
    obstacle_index = obstacle_index + 1;
    obstacles{obstacle_index} = line;
    line = fgets(flight_information_handle);
end
fclose(flight_information_handle);
flight_information_handle = fopen(handles.flight_information_path,'w+');
while(~flight_information_handle)
    flight_information_handle = fopen(handles.flight_information_path,'w+');
end
obstacle_x = handles.add_obstacle_x.String;
obstacle_y = handles.add_obstacle_y.String;
obstacle_z = handles.add_obstacle_z.String;
obstacle_r = handles.add_obstacle_r.String;
if(handles.static_button.Value == 1)
    obstacle_type = 'static';
else
    obstacle_type = 'dynamic';
end
obstacle_index = obstacle_index + 1;
new_obstacle = [obstacle_type ' ' obstacle_x ' ' obstacle_y ' ' obstacle_z ' ' obstacle_r '\n'];
obstacles{obstacle_index} = new_obstacle;
fprintf(flight_information_handle,updated);
fprintf(flight_information_handle,goal);
fprintf(flight_information_handle,start);
fprintf(flight_information_handle,current);
for i = [1:1:obstacle_index]
    fprintf(flight_information_handle,obstacles{i});
end
fclose(flight_information_handle);
plot_data(handles);
mode_list_Callback(handles.mode_list,eventdata,handles);

% --- Executes on selection change in delete_obstacle_num.
function delete_obstacle_num_Callback(hObject, eventdata, handles)
% hObject    handle to delete_obstacle_num (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns delete_obstacle_num contents as cell array
%        contents{get(hObject,'Value')} returns selected item from delete_obstacle_num


% --- Executes during object creation, after setting all properties.
function delete_obstacle_num_CreateFcn(hObject, eventdata, handles)
% hObject    handle to delete_obstacle_num (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in delete_obstacle_button.
function delete_obstacle_button_Callback(hObject, eventdata, handles)
% hObject    handle to delete_obstacle_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
delete_num = str2num(handles.delete_obstacle_num.String);
flight_information_handle = fopen(handles.flight_information_path,'r');
updated = fgets(flight_information_handle);
updated = 'Update 1\n';
goal = fgets(flight_information_handle);
start = fgets(flight_information_handle);
current = fgets(flight_information_handle);
obstacle_index = 0;
line = fgets(flight_information_handle);
while line ~= -1
    if(num2str(obstacle_index+1) ~= delete_num)
        obstacle_index = obstacle_index + 1;
        obstacles{obstacle_index} = line;
    end
    line = fgets(flight_information_handle);
end
fclose(flight_information_handle);
flight_information_handle = fopen(handles.flight_information_path,'w');
fprintf(flight_information_handle,updated);
fprintf(flight_information_handle,goal);
fprintf(flight_information_handle,start);
fprintf(flight_information_handle,current);
for i = [1:1:obstacle_index]
    if(i ~= delete_num)
        fprintf(flight_information_handle,obstacles{i});
    end
end
fclose(flight_information_handle);
mode_list_Callback(handles.mode_list,eventdata,handles);
plot_data(handles);


% --------------------------------------------------------------------
function Untitled_1_Callback(hObject, eventdata, handles)
% hObject    handle to Untitled_1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
