%% Testing Senarios

clc 
clear all
close all

Nodes = [100 100 50;
        100 -100 50;
        -100 -100 50;
        -100 100 50];

Object1 = moving_Object();

Object1.addNodes(Nodes);

for k = 10:1:150
    Object1.plot(k)
    pause(.01)
    k
end
