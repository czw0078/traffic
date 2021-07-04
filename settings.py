#!/usr/bin/env python3

import tkinter
from collections import deque

animation_window_width=800
animation_window_height=800
animation_ball_radius = 30
animation_ball_min_movement = 5
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

route_table = [None]

def convert_to_window(x, y):
    w = int(x*sw + tw)
    h = int(-y*sh + th)
    return w, h

def logger(message):
    print(message)

def prepare_model(canvas):
    res = []
    # add node and road, and connect them with v1 v2
    n1 = Node(canvas, 0, 0)
    n2 = Node(canvas, 200,200)
    tr1 = Road(canvas, n1, n2, 0)
    tr2 = Road(canvas, n1, n2, 1) # second lane
    o3 = Node(canvas, -50, 50)
    r1 = Road(canvas, o3, n1, 0)
    # add a route table, OD to route lists
    route_table[0] = [r1, tr2]
    #
    # tr1.add_vechle
    v1 = Vehicle(canvas,-50,50)
    #v1.road.vehicle_queue.appendleft(v1)
    if len(r1.vehicle_queue) > 0:
        v1.front_vehicle = r1.vehicle_queue[0]
    else:
        v1.front_vehicle = None
    r1.vehicle_queue.appendleft(v1)

    #
    v2 = Vehicle(canvas,50,50)
    v2.road = tr2
    tr2.vehicle_queue.appendleft(v2)
    # 
    res.append(v1)
    res.append(v2)
    return res

def config_window(window):
    window.title("Traffic Demo")
    window.geometry(str(animation_window_width)+'x'+str(animation_window_height))
    window.attributes("-topmost", True)

def config_canvas(canvas):
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)

class Direction:
    def __init__(self, route_list, current_vehicle):
        self.vehicle = current_vehicle
        self.segment_index = 0
        self.road = route_list[self.segment_index]
        self.front_vehicle = self.new_front_vehicle() #TODO
        self.x, self.y = self.road.drive_along(current_vehicle.s)

    def new_front_vehicle(self):
        if len(self.road.vehicle_queue)>0:
            return self.road.vehicle_queue[0]
        else:
            return None

    def enter_road(self):
            self.front_vehicle = new_front_vehicle()
            self.road.vehicle_queue.appendleft(self.vehicle)

    def exit_road_if_head(self):
        if self.road.vehicle_queue[-1] == self.vehicle:
            self.vehicle.s = self.vehicle.s - self.road.l
            self.road.vehicle_queue.pop()

    def next_road_if_passed(self):
        is_passed = self.vehicle.s > self.road.l
        if not is_passed:
            return
        self.exit_road_if_head()
        self.segment_index += 1
        self.road = route_list[self.segment_index]
        self.enter_road()

    def update(self):
        if self.segment_index < len(route_list):
            self.next_road_if_passed()
        self.x, self.y = self.road.drive_along(self.vehicle.s)

class Vehicle:

    def __init__(self, canvas, x, y):
        # world
        self.x = x
        self.y = y
        # screen
        self.w = 0
        self.h = 0
        self.h_offset = 0
        self.canvas = canvas
        self.sprite = self._init_sprite(self.canvas)
        # road
        self.a = 0
        self.v = 3 
        self.s = 0
        # TODO set up direction and screen class
        self.front_vehicle = None
        self.route_index = None
        self.route_list = self.caculate_route()
        self.segment_index = 0
        self.road = self.route_list[self.segment_index]

    def caculate_route(self):
        return route_table[0]

    def _init_sprite(self, canvas):
        self.w, self.h = convert_to_window(self.x, self.y)
        # self.h += self.road.h_offset
        res = canvas.create_rectangle(
                self.w - vehicle_size_px,
                self.h - vehicle_size_px,
                self.w,
                self.h,
                fill="red")
        return res

    def rule(self):
        is_queue_head = self.road.vehicle_queue[-1] == self
        is_passed = self.s > self.road.l
        if is_queue_head and is_passed:
            self.s = self.s - self.road.l
            self.road.vehicle_queue.pop()
            self.segment_index += 1
            self.road = self.route_list[self.segment_index]
            if len(self.road.vehicle_queue) > 0:
                self.front_vehicle = self.road.vehicle_queue[0]
            else:
                self.front_vehicle = None
            self.road.vehicle_queue.appendleft(self)

    def go(self):
        self.v = self.v + self.a*time_interval
        self.s = self.s + self.v*time_interval
        self.x, self.y = self.road.drive_along(self.s)
        self.w, self.h = convert_to_window(self.x, self.y)

    def redraw(self):
        self.canvas.coords(self.sprite,
                self.w - vehicle_size_px,
                self.h - vehicle_size_px + self.road.h_offset,
                self.w,
                self.h + self.road.h_offset)

class Road:
    def __init__(self, canvas, start, end, lane=0):
        self.start, self.end, self.l = self._init_endpoint(start, end)
        self.v_max = 25
        self.vehicle_queue = deque() #left right 0, -1
        # shape
        self.h_offset = -lane*6
        self.road_width_px = 3
        self.sprite = self._init_sprite(canvas)

    def _init_endpoint(self, start, end):
        end.inflow.append(self)
        start.outflow.append(self)
        l = ((start.x - end.x)**2 + (start.y - end.y)**2)**0.5
        return start, end, l

    def _init_sprite(self, canvas):
        self.w1, self.h1 = convert_to_window(self.start.x, self.start.y)
        self.w2, self.h2 = convert_to_window(self.end.x, self.end.y)
        self.h1 += self.h_offset
        self.h2 += self.h_offset
        res = canvas.create_line(self.w1, self.h1, self.w2, self.h2, 
                arrow=tkinter.LAST, fill="white")
        return res

    def enter(self):
        pass

    def exit(self):
        pass
        # return new road

    def drive_along(self, s):
        x = (s*self.end.x + (self.l - s)*self.start.x)/self.l
        y = (s*self.end.y + (self.l - s)*self.start.y)/self.l
        return x, y

class Node:
    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.inflow = []
        self.outflow = []
        self.inflow_neighbors = []
        self.node_width_px = 3
        self.node_height_px = 24
        self.sprite = self._init_sprite(canvas)

    def _init_sprite(self, canvas):
        self.w, self.h = convert_to_window(self.x, self.y)
        res = canvas.create_rectangle(self.w,
            self.h,
            self.w + self.node_width_px,
            self.h - self.node_height_px,
            fill="green")
        return res

    def update_neighbors(self):
        self.inflow_neighbors = []
        for each_road in self.inflow:
            if len(each_road.vehicle_queue) > 0:
                vehicle = each_road.vehicle_queue[-1]
                self.inflow_neighbors.append((each_road.l - vehicle.s, vehicle))
        self.inflow_neighbors.sort(reverse=True)

    def rule(self):
        self.inflow_neighbors()

    def go(self):
        pass

    def redraw(self):
        pass










