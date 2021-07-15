import tkinter
from collections import deque
import automata
import graph
import settings

DEBUG = False

class Vehicle:

    def __init__(self, canvas, net, O, D, s=0, tag="v"):
        # annotation and stats
        self.tag = tag
        self.timestamp = 0
        # number +1
        settings.total_number_vehicle += 1
        self.finished = False
        # road inital variables
        self.t = 0
        self.a = 0
        self.v = 0
        self.next_a = 0
        self.next_v = 0
        self.s = 0
        self.kksw = automata.kksw()
        # direction update
        self.net = net
        self.D = D
        self.road, self.next_road = self.net.get_current_and_next_road(O,D)
        self.front_vehicle = None
        self.road.add_vehicle_and_update_front(self)
        self.s = s % self.road.l
        self.x, self.y = self.road.drive_along(self.s)
        # screen draw
        self.w, self.h = settings.convert_to_window(self.x, self.y)
        self.h += self.road.h_offset
        self.canvas = canvas
        self.sprite = self._init_sprite(self.canvas)

    def __repr__(self):
        return self.tag

    def _init_sprite(self, canvas):
        color = "red"
        res = canvas.create_rectangle(
                self.w - settings.vehicle_size_px,
                self.h - settings.vehicle_size_px,
                self.w, self.h, fill=color)
        return res

    def _timing_if_passed(self):
        if self.s >= self.road.l:
            self.road.last_travel_time = settings.global_t - self.timestamp
            self.timestamp = settings.global_t

    def _transition_if_passed(self):
        if self.s >= self.road.l:
            self.road.remove_vehicle_and_update_s(self)
            self._recaculate_route()
            self.road.add_vehicle_and_update_front(self)

    def _update_direction(self):
        self._timing_if_passed()
        # if last road, __del__ remove all reference
        if self.next_road == None and self.s >= self.road.l:
            self.finished = True
            self.road.remove_vehicle_and_update_s(self)
            self.front_vehicle = None
            self.road.end.update_neighbors()
            # and last time draw when > road.l
            self.x = self.road.end.x
            self.y = self.road.end.y
            settings.total_travel_time += self.t
            return
        self._transition_if_passed()
        self.x, self.y = self.road.drive_along(self.s)

    def _update_screen(self):
        self.w, self.h = settings.convert_to_window(self.x, self.y)
        self.h += self.road.h_offset

    def _recaculate_route(self):
        O = self.road.end
        self.road, self.next_road = self.net.get_current_and_next_road(O, self.D)

    def _nearest_car_vl_g(self):
        current_rest_distance = self.road.l - self.s
        if self.front_vehicle:
            # could be front car in the next road
            g=(self.front_vehicle.s - self.s)%self.road.l
            return self.front_vehicle.v, g
        for rest_distance, vehicle in self.road.end.inflow_neighbors:
            if rest_distance < current_rest_distance:
                return vehicle.v, current_rest_distance - rest_distance
        if self.next_road:
            far_vehicle = self.next_road.vehicle_queue_leftmost()
            if far_vehicle:
                return far_vehicle.v, far_vehicle.s + self.road.l - self.s
        return 0, 120

    def rule(self):
        if self.front_vehicle and self.front_vehicle.finished:
            self.front_vehicle = None
        vl, g = self._nearest_car_vl_g()
        self.a_next, self.v_next = self.kksw.update_a_v_vl_g_and_get_a_v(
                self.a, self.v, vl, g)
        if DEBUG:
            print("--debug--", self.t, self.tag, self.road, self.next_road, self.s,self.road.l, vl, g)

    def go(self):
        self.v = self.v_next
        self.a = self.a_next
        self.v = self.v + self.a*settings.time_interval
        self.s = self.s + self.v*settings.time_interval
        self._update_direction()
        self._update_screen()
        self.t += 1

    def redraw(self):
        self.canvas.coords(self.sprite,
                self.w - settings.vehicle_size_px,
                self.h - settings.vehicle_size_px,
                self.w, self.h)
