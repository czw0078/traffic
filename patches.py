import tkinter
from collections import deque
import automata
import graph
import settings

DEBUG = False

class Road:
    def __init__(self, canvas, start, end, lane=0):
        self.start, self.end, self.l = self._init_endpoint(start, end)
        self.v_max = 25
        self.last_travel_time = None
        self.vehicle_queue = deque()
        # shape
        self.h_offset = -lane*6
        self.road_width_px = 3
        self.sprite = self._init_sprite(canvas)

    def __repr__(self):
        return str(self.start.tag)+"->"+str(self.end.tag)

    def _init_endpoint(self, start, end):
        end.inflow.append(self)
        start.outflow.append(self)
        l = ((start.x - end.x)**2 + (start.y - end.y)**2)**0.5
        return start, end, l

    def _init_sprite(self, canvas):
        self.w1, self.h1 = settings.convert_to_window(self.start.x, self.start.y)
        self.w2, self.h2 = settings.convert_to_window(self.end.x, self.end.y)
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
        if DEBUG:
            print("--debug--", settings.global_t, self.get_travel_time())

class Node:
    def __init__(self, canvas, x, y, tag="x"):
        self.tag = tag
        self.x = x
        self.y = y
        self.inflow = []
        self.outflow = []
        self.inflow_neighbors = []
        self.node_width_px = 3
        self.node_height_px = 24
        self.sprite = self._init_sprite(canvas)

    def __repr__(self):
        return self.tag

    def _init_sprite(self, canvas):
        self.w, self.h = settings.convert_to_window(self.x, self.y)
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
            print("--debug--", settings.global_t, self.inflow_neighbors)


