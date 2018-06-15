function varargout = Final(varargin)
% FINAL MATLAB code for Final.fig
%      FINAL, by itself, creates a new FINAL or raises the existing
%      singleton*.
%
%      H = FINAL returns the handle to a new FINAL or the handle to
%      the existing singleton*.
%
%      FINAL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in FINAL.M with the given input arguments.
%
%      FINAL('Property','Value',...) creates a new FINAL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Final_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Final_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Final

% Last Modified by GUIDE v2.5 12-Jun-2018 00:32:40

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Final_OpeningFcn, ...
                   'gui_OutputFcn',  @Final_OutputFcn, ...
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


% --- Executes just before Final is made visible.
function Final_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
clc
handles.running = 0;
handles.AltitudeText.String = '0';
handles.wpnoText.String = '0';
handles.AirspeedText.String = '0';
handles.wp_distText.String = '0';


handles.button_staticOnly.BackgroundColor = [.47 .67 .19];
handles.button_dynamic.BackgroundColor = [.8 .8 .8];
%  Choose default command line output for Final
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Final wait for user response (see UIRESUME)
% uiwait(handles.figure1);


function obs = getStaticObs()
    fileStatic = fopen('static_obstacles.txt');
    C = fscanf(fileStatic,'%f %f %f %f',[4 Inf]);
    fclose(fileStatic);
    obs = C';


function bounds = getBoundry()
    fileStatic = fopen('boundry.txt');
    C = fscanf(fileStatic,'%f %f',[2 Inf]);
    fclose(fileStatic);
    C = [C C(:,1)];
    bounds = C';


function obs = getMovingObs()
    fileStatic = fopen('moving_obstacles.txt');
    C = fscanf(fileStatic,'%f %f %f %f',[4 Inf]);
    fclose(fileStatic);
    obs = C';


function wps = getWps()
    fileStatic = fopen('waypoints.txt');
    C = fscanf(fileStatic,'%f %f %f',[3 Inf]);
    fclose(fileStatic);
    wps = C';


function dat = getState()
    fileStatic = fopen('current_state.txt');
    C = fscanf(fileStatic,'%f %f %f %f %f %f',[6 Inf]);
    fclose(fileStatic);
    dat = C';


function dat = getMission()
    fileStatic = fopen('Mission_data.txt');
    C = fscanf(fileStatic,'%f %f',[2 Inf]);
    fclose(fileStatic);
    dat = C';
    
% --- Outputs from this function are returned to the command line.
function varargout = Final_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



% --- Executes on button press in button_start.
function button_start_Callback(hObject, eventdata, handles)
%     hanldes.running = 1;
    format long
    static_obs = getStaticObs();
    boundry = getBoundry();
    mis = getMission();

    tic
    while(toc < 15)
        

        state = getState();
        if (size(state,2) > 4)
            handles.AirspeedText.String = string(state(4));
            handles.wpnoText.String = string(state(5));
            handles.AltitudeText.String = string(state(3));
            handles.wp_distText.String = string(state(6));
            hold off
            scatter(state(1),state(2),50,'b','filled')
            hold on
        end

        wps = getWps();
        moving_obs = getMovingObs();
%         axis(handles.Map)
        
        scatter(mis(:,1),mis(:,2),60,'g','filled')
        
        scatter(wps(:,1),wps(:,2),'r')
        plot(wps(:,1),wps(:,2),'r')
        
        for k = 1:size(moving_obs)
            viscircles([moving_obs(k,1),moving_obs(k,2)],moving_obs(k,4),'Color',[0 1 .5]);
        end
        
        for k = 1:size(static_obs)
            viscircles([static_obs(k,1),static_obs(k,2)],static_obs(k,4),'Color',[1 0 .5]);
        end
        
        plot(boundry(:,1),boundry(:,2),'k')
        axis([-2250 2200 -2000 2700])


        pause(.5)
    end
    
    handles.output = hObject;
    guidata(hObject, handles);
% hObject    handle to button_start (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in button_dynamic.
function button_staticOnly_Callback(hObject, eventdata, handles)
    fileID = fopen('static_bool.txt','w');
    fprintf(fileID,'1 ');
    fclose(fileID);
    
%     handles.button_dynamic.BackgroundColor = [.47 .67 .19];
%     handles.button_staticOnly.BackgroundColor = [.8 .8 .8];
    
    handles.output = hObject;
    guidata(hObject, handles);

% --- Executes on button press in button_stop.
function button_stop_Callback(hObject, eventdata, handles)
    hanldes.running = 0;
    
    handles.output = hObject;
    guidata(hObject, handles);
