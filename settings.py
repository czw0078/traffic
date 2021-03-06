#!/usr/bin/env python3

# TODO money one net each vehicle -> cost = alpha*travel_time + charge
# The update of road information only available next round
# therefore the agents has 1 step delay by default

import tkinter
import graph
import agents
import patches
import profile

DEBUG = False

animation_window_width=800
animation_window_height=800
animation_refresh_milliseconds = 100 # for demo it could be 100

# world_width_m = 200000
# world_height_m = 200000
world_width_m = 1600
world_height_m = 1600
vehicle_size_px = 6

tw = 0.5*animation_window_width
th = 0.5*animation_window_height
sw = animation_window_width/world_width_m
sh = animation_window_height/world_height_m

min_gap = 7.6 # the minimal gap between cars

total_ticks = profile.total_ticks # 600 = 10 min, 3600 = 1 hour
time_interval = 1 # 1 second per tick
global_t = 0 # the global clock

total_travel_time = []
total_number_vehicle = 0

def print_all():
    at = sum(total_travel_time)/len(total_travel_time)
    print(at)

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


class Map:
    def __init__(self, canvas):
        self.canvas = canvas
        self.node_list = []
        self.road_list = []
        self.net = None
        self.patch_list = None
        self.turtle_set = set()
        self.ODN = profile.get_ODN()

    def node(self, x, y):
        n = len(self.node_list)
        tag = 'n'+str(n)
        res = patches.Node(self.canvas, x, y, tag)
        self.node_list.append(res)
        return res

    def road(self, start, end, v_free=25, lane=0):
        res = patches.Road(self.canvas, start, end, v_free, lane)
        self.road_list.append(res)
        return res

    def patch_section_end(self):
        if self.net == None:
            self.net = graph.Network(self.node_list, self.road_list)
        if self.patch_list == None:
            self.patch_list = self.node_list + self.road_list + [self.net]

    def demand(self):
        if global_t < len(self.ODN) and self.ODN[global_t] != None:
            # print("demand", self.ODN[global_t])
            for i_O, i_D, N in self.ODN[global_t]:
                O = self.node_list[i_O]
                D = self.node_list[i_D]
                for _ in range(N):
                    res = agents.Vehicle(self.canvas, self.net, O, D)
                    self.turtle_set.add(res)

    def prepare_model(self):
        profile.prepare_patch_list(self)

        if self.net == None:
            self.net = graph.Network(self.node_list, self.road_list)
        if self.patch_list == None:
            self.patch_list = self.node_list + self.road_list + [self.net]
        # self.patch_section_end()
        return self.patch_list, self.turtle_set

