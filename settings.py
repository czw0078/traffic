#!/usr/bin/env python3

# TODO adjust MAP, money one net each vehicle -> cost = alpha*travel_time + charge
# The update of road information only available next round
# therefore the agents has 1 step delay by default

import tkinter
import graph
import agents
import patches

DEBUG = False

animation_window_width=800
animation_window_height=800
animation_refresh_milliseconds = 100

# world_width_m = 200000
# world_height_m = 200000
world_width_m = 1600
world_height_m = 1600
vehicle_size_px = 6

tw = 0.5*animation_window_width
th = 0.5*animation_window_height
sw = animation_window_width/world_width_m
sh = animation_window_height/world_height_m

total_ticks = 30 # 3600 = 1 hour
time_interval = 1 # 1 second per tick
global_t = 0 # the global clock

total_travel_time = 0
total_number_vehicle = 0

def convert_to_window(x, y):
    w = int(x*sw + tw)
    h = int(-y*sh + th)
    return w, h

def config_window(window):
    window.title("Traffic Demo")
    window.geometry(str(animation_window_width)+'x'+str(animation_window_height))
    window.attributes("-topmost", True)

def config_canvas(canvas):
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)

def prepare_model(canvas):
    # node and road network
    n0 = patches.Node(canvas, -50, 50, 'n0')
    n1 = patches.Node(canvas, 0, 0, 'n1')
    n2 = patches.Node(canvas, 200,200, 'n2')
    n3 = patches.Node(canvas, -50, -50, 'n3')
    r0 = patches.Road(canvas, n0, n1, 0)
    r1 = patches.Road(canvas, n2, n1, 0)
    r2 = patches.Road(canvas, n1, n2, 1)
    r3 = patches.Road(canvas, n3, n1, 0)
    node_list = [n0, n1, n2, n3]
    road_list = [r0, r1, r2, r3]
    net = graph.Network(node_list, road_list)
    patch_list = node_list + road_list + [net]

    # LATERDO OD_profile
    turtle_set = set()
    v1 = agents.Vehicle(canvas, net, n0, n2,  0)
    v2 = agents.Vehicle(canvas, net, n3, n2, 10)
    turtle_set.add(v1)
    turtle_set.add(v2)
    return patch_list, turtle_set

def add_vehicle(canvas, net, ramp, D, N, t):
    pass

class Map:

    def __init__(self, canvas, net):
        pass


