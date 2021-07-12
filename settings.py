#!/usr/bin/env python3

# TODO OD, money, adjust MAP
# The update of road information only available next round
# therefore the agents has 1 step delay by default

import tkinter
from collections import deque
import automata

DEBUG = False

animation_window_width=800
animation_window_height=800
animation_refresh_milliseconds = 100

# world_width_m = 200000
# world_height_m = 200000
ramp_v_max = 3
world_width_m = 1600
world_height_m = 1600
vehicle_size_px = 6

tw = 0.5*animation_window_width
th = 0.5*animation_window_height
sw = animation_window_width/world_width_m
sh = animation_window_height/world_height_m

total_ticks = 20 # 3600 = 1 hour
time_interval = 1 # 1 second per tick
global_t = 0 # the global clock

route_table = [None, None]

total_travel_time = 0
total_number_vehicle = 0

def convert_to_window(x, y):
    w = int(x*sw + tw)
    h = int(-y*sh + th)
    return w, h

def logger(message):
    print(message)

def prepare_model(canvas):
    patch_list = []
    turtle_set = set() 
    # node and road network
    n0 = Node(canvas, -50, 50)
    n1 = Node(canvas, 0, 0)
    n2 = Node(canvas, 200,200)
    n3 = Node(canvas, -50, -50)
    r0 = Road(canvas, n0, n1, 0)
    r1 = Road(canvas, n1, n2, 0)
    r2 = Road(canvas, n1, n2, 1)
    r3 = Road(canvas, n3, n1, 0)
    # LATERDO
    # split prepare into prepare network and OD_profile later
    # a route table, OD to route lists
    # OD profile
    route_table[0] = [r0, r2]
    route_table[1] = [r3, r2]
    v1 = Vehicle(canvas, 0, tag="v1")
    v2 = Vehicle(canvas, 1, 10, tag="v2")
    patch_list.append(n1)
    patch_list.append(n2)
    patch_list.append(r0)
    patch_list.append(r3)
    patch_list.append(r2)
    turtle_set.add(v1)
    turtle_set.add(v2)
    return patch_list, turtle_set

def config_window(window):
    window.title("Traffic Demo")
    window.geometry(str(animation_window_width)+'x'+str(animation_window_height))
    window.attributes("-topmost", True)

def config_canvas(canvas):
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)

class Vehicle:

    def __init__(self, canvas, OD, s=0, tag="x"):
        # annotation and stats
        self.tag = tag
        self.timestamp = 0
        # number +1
        global total_number_vehicle
        total_number_vehicle += 1
        self.finished = False
        # road inital variables
        self.t = 0
        self.a = 0
        self.v = 0 # 6
        self.next_a = 0
        self.next_v = 0
        self.s = 0
        self.kksw = automata.kksw()
        # direction update
        self.route_list = self._caculate_route(OD)
        self.segment_index = 0
        self.road = self.route_list[self.segment_index]
        self.front_vehicle = None
        self.road.add_vehicle_and_update_front(self)
        self.s = s % self.road.l
        self.x, self.y = self.road.drive_along(self.s)
        # screen draw
        self.w, self.h = convert_to_window(self.x, self.y)
        self.h += self.road.h_offset
        self.canvas = canvas
        self.sprite = self._init_sprite(self.canvas)

    def _init_sprite(self, canvas):
        res = canvas.create_rectangle(
                self.w - vehicle_size_px,
                self.h - vehicle_size_px,
                self.w, self.h, fill="red")
        return res

    def _timing_if_passed(self):
        if self.s >= self.road.l:
            self.road.last_travel_time = global_t - self.timestamp
            self.timestamp = global_t

    def _transition_if_passed(self):
        if self.s >= self.road.l:
            self.road.remove_vehicle_and_update_s(self)
            self.segment_index += 1
            self.road = self.route_list[self.segment_index]
            self.road.add_vehicle_and_update_front(self)

    def _update_direction(self):
        self._timing_if_passed()
        last_segment = self.segment_index == len(self.route_list) - 1
        if last_segment and self.s >= self.road.l:
            # __del__
            self.finished = True
            self.road.remove_vehicle_and_update_s(self)
            self.front_vehicle = None
            self.road.end.update_neighbors()
            global total_travel_time
            total_travel_time += self.t
            return
        self._transition_if_passed()
        self.x, self.y = self.road.drive_along(self.s)

    def _update_screen(self):
        self.w, self.h = convert_to_window(self.x, self.y)
        self.h += self.road.h_offset

    def _caculate_route(self, OD):
        # LATERDO
        return route_table[OD]

    def _nearest_car_vl_g(self):
        current_rest_distance = self.road.l - self.s
        if self.front_vehicle:
            # could be front car in the next road
            g=(self.front_vehicle.s - self.s)%self.road.l
            return self.front_vehicle.v, g 
        for rest_distance, vehicle in self.road.end.inflow_neighbors:
            if rest_distance < current_rest_distance:
                return vehicle.v, current_rest_distance - rest_distance
        if self.segment_index + 1 < len(self.route_list):
            next_road = self.route_list[self.segment_index + 1]
            far_vehicle = next_road.vehicle_queue_leftmost()
            if far_vehicle:
                return far_vehicle.v, far_vehicle.s + self.road.l - self.s
        return 0, 120

    def rule(self):
        # TODO micro rul
        vl, g = self._nearest_car_vl_g()
        self.a_next, self.v_next = self.kksw.update_a_v_vl_g_and_get_a_v(
                self.a, self.v, vl, g)
        if DEBUG:
            print("--debug--", self.t, self.tag, "vl_g", self._nearest_car_vl_g())

    def go(self):
        self.v = self.v_next
        self.a = self.a_next
        self.v = self.v + self.a*time_interval
        self.s = self.s + self.v*time_interval
        self._update_direction()
        self._update_screen()
        self.t += 1

    def redraw(self):
        self.canvas.coords(self.sprite,
                self.w - vehicle_size_px,
                self.h - vehicle_size_px,
                self.w, self.h) 

class Road:
    def __init__(self, canvas, start, end, lane=0):
        self.start, self.end, self.l = self._init_endpoint(start, end)
        self.v_max = 25
        self.last_travel_time = None
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

    def get_travel_time(self):
        if self.last_travel_time == None:
            return self.l/self.v_max
        else:
            return self.last_travel_time

    def vehicle_queue_leftmost(self):
        if len(self.vehicle_queue)>0:
            return self.vehicle_queue[0]
        else:
            return None

    def add_vehicle_and_update_front(self, current_vehicle):
        current_vehicle.front_vehicle = self.vehicle_queue_leftmost()
        self.vehicle_queue.appendleft(current_vehicle)

    def remove_vehicle_and_update_s(self, current_vehicle):
        not_empty = len(self.vehicle_queue) > 0
        if not_empty and self.vehicle_queue[-1] == current_vehicle:
            self.vehicle_queue.pop()
        current_vehicle.s = current_vehicle.s - self.l

    def drive_along(self, s):
        x = (s*self.end.x + (self.l - s)*self.start.x)/self.l
        y = (s*self.end.y + (self.l - s)*self.start.y)/self.l
        return x, y

    def rule(self):
        pass

    def go(self):
        if Debug:
            print("--debug--", global_t, self.get_travel_time())

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
        self.update_neighbors()

    def go(self):
        if DEBUG:
            print("--debug--", global_t, self.inflow_neighbors)



