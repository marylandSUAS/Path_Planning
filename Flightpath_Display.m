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

% Last Modified by GUIDE v2.5 08-Jun-2017 12:59:11

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
handles.missionDirectory = 'C:\Users\imaging2.0\Documents\MUAS-17\Flight_Path';
handles.shortest_path_path = strcat(handles.missionDirectory,'\shortest_path.txt');
handles.flight_information_path = strcat(handles.missionDirectory,'\flight_information.txt');
handles.intermediate_waypoints_path = strcat(handles.missionDirectory,'intermediate_waypoints.txt');

% Choose default command line output for Flightpath_Display
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Flightpath_Display wait for user response (see UIRESUME)
% uiwait(handles.figure1);


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
mode = handles.mode_list.Value;
if(mode ~= 2)
    return
end
!make
!main.exe
% ... doing stuff ...

% Create file handles
flight_information_handle = fopen(handles.flight_information_path);
shortest_path_handle = fopen(handles.shortest_path_path);
waypoints_handle = fopen(handles.intermediate_waypoints_path);

% Only update graph if shortest path is different than before
changed = sscanf(fgets(shortest_path_handle),'Changed %s');
if(changed == '1')
    % Extract data for start, goal and current nodes, and obstacle
    % locations.
    path_data = fscanf(shortest_path_handle,'%f',[3,inf])';
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
        line = textscan(line,'%s %f %f %f %f');
        obstacles(obstacle_index,:) = [line{2},line{3},line{4},line{5}];
        obstacle_type(obstacle_index,:) = line{1};
        line = fgets(flight_information_handle);
    end
    
    % Plot obstacles as cylinders, and start, goal and current nodes as
    % spheres.
    axes(handles.current_path_axes);
    shading FLAT;
    hold on;
    plot3(path_data(:,1),path_data(:,2),path_data(:,3)); % Plot raw path data.
    % Plot obstacles.
    z_min = min(start(3),goal(3));
    z_max = max(start(3),goal(3));
    for i = [1:1:obstacle_index]
        switch obstacle_type{i,1}
            case 'static'
                [x,y,z] = cylinder(obstacles(i,4),10);
                surf(x+obstacles(i,1),y+obstacles(i,2),z+z_min,'FaceColor',[0.85 0.6 0]);
                for z_inc = [z_min+1:1:z_max-1]
                    surf(x+obstacles(i,1),y+obstacles(i,2),z+z_inc,'FaceColor','none','EdgeColor',[0.8 0.8 0.8]);
                end
                surf(x+obstacles(i,1),y+obstacles(i,2),z+z_max,'FaceColor',[0.85 0.6 0]);
            case 'dynamic'
                [x,y,z] = sphere(10);
                surf(x*obstacles(i,4)+obstacles(i,1),y*obstacles(i,4)+obstacles(i,2),z*obstacles(i,4)+obstacles(i,3),'FaceColor','none','EdgeColor',[0.8 0.8 0.8]);
        end
    end
    view(-(0.5-handles.az_slider.Value)*180,-(0.5-handles.elev_slider.Value)*180);
    % Plot start, goal, current nodes.
    diag_dist = norm(goal-start);
    wp_rad = diag_dist/75;
    [x,y,z] = sphere(10);
    surf(x*wp_rad+start(1),y*wp_rad+start(2),z*wp_rad+start(3),'FaceColor','none','EdgeColor',[0.5 0 0]);
    surf(x*wp_rad+goal(1),y*wp_rad+goal(2),z*wp_rad+goal(3),'FaceColor','none','EdgeColor',[0 0.5 0]);
    surf(x*wp_rad+current(1),y*wp_rad+current(2),z*wp_rad+current(3),'FaceColor',[0.6 0.6 0.9]);
    axis equal;
    grid on;
    hold off;
end
fclose(flight_information_handle);
fclose(shortest_path_handle);
fclose(intermediate_waypoints_handle);

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
        line = textscan(line,'%s %f %f %f %f');
        obstacles(obstacle_index,:) = [line{2},line{3},line{4},line{5}];
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
view(-(0.5-handles.az_slider.Value)*180,-(0.5-handles.elev_slider.Value)*180);
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
view(-(0.5-handles.az_slider.Value)*180,-(0.5-handles.elev_slider.Value)*180);
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
set_goal = ['goal 25.0 25.0 25.0\n'];
set_start = ['start 0.0 0.0 0.0\n'];
set_current = ['current 0.0 0.0 0.0\n'];
add_obstacle = ['static 12.5 12.5 12.5 2.5\n'];
fprintf(flight_information_handle,set_updated);
fprintf(flight_information_handle,set_goal);
fprintf(flight_information_handle,set_start);
fprintf(flight_information_handle,set_current);
fprintf(flight_information_handle,add_obstacle);
fclose(flight_information_handle);
mode_list_Callback(handles.mode_list,eventdata,handles);

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
mode_list_Callback(handles.mode_list,eventdata,handles);

% --- Executes on selection change in delete_obstacle_list.
function delete_obstacle_list_Callback(hObject, eventdata, handles)
% hObject    handle to delete_obstacle_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns delete_obstacle_list contents as cell array
%        contents{get(hObject,'Value')} returns selected item from delete_obstacle_list


% --- Executes during object creation, after setting all properties.
function delete_obstacle_list_CreateFcn(hObject, eventdata, handles)
% hObject    handle to delete_obstacle_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
current_obstacle_list_size = handles.obstacle_gps_locations.String;
current_obstacle_list_size = current_obstacle_list_size.size;
for i = [1:1:current_obstacle_list_size]
    set(handles.delete_obstacle_list,'String',[handles.delete_obstacle_list num2str(i)]);
end


% --- Executes on button press in delete_obstacle_button.
function delete_obstacle_button_Callback(hObject, eventdata, handles)
% hObject    handle to delete_obstacle_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
delete_num = handles.delete_obstacle_list.String;
flight_information_handle = fopen(handles.flight_information_path,'r');
updated = fgets(flight_information_handle);
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
    fprintf(flight_information_handle,obstacles{i});
end
fclose(flight_information_handle);
mode_list_Callback(handles.mode_list,eventdata,handles);
