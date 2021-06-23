#!/usr/bin/env python3

# import tkinter

animation_window_width=800
animation_window_height=800
animation_ball_radius = 30
animation_ball_min_movement = 5
animation_refresh_milliseconds = 10

# world_width_m = 200000
# world_height_m = 200000
world_width_m = 1600
world_height_m = 1600
vehicle_size_px = 6

tw = 0.5*animation_window_width
th = 0.5*animation_window_height
sw = animation_window_width/world_width_m
sh = animation_window_height/world_height_m

total_ticks = 500 # 3600 = 1 hour

def convert_to_window(x, y):
    w = int(x*sw + tw)
    h = int(y*sh + th)
    return w, h

def logger(message):
    print(message)

def prepare_model(canvas):
    res = []
    v1 = Vehicle(canvas,0,0)
    v2 = Vehicle(canvas,50,50)
    res.append(v1)
    res.append(v2)
    return res

def config_window(window):
    window.title("Traffic Demo")
    window.geometry(str(animation_window_width)+'x'+str(animation_window_height))

def config_canvas(canvas):
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)

class Vehicle():

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.delta_x = 5
        self.delta_y = 5
        self.w = 0
        self.h = 0
        self.sprite = self._init_sprite(self.canvas)

    def _init_sprite(self, canvas):
        self.w, self.h = convert_to_window(self.x, self.y)
        res = canvas.create_rectangle(self.w, self.h,
            self.w + vehicle_size_px,
            self.h + vehicle_size_px,
            fill="red")
        return res

    def go(self):
        self.x = self.x + self.delta_x
        self.y = self.y + self.delta_y
        self.w, self.h = convert_to_window(self.x, self.y)

    def redraw(self):
        self.canvas.coords(self.sprite,
                self.w, self.h,
                self.w + vehicle_size_px,
                self.h + vehicle_size_px)

    def rule(self):
        if self.x < - world_width_m/2 + 1  or self.x > world_width_m/2 - 1:
            self.delta_x = - self.delta_x
        if self.y < - world_height_m/2 + 1 or self.y > world_height_m/2 - 1:
            self.delta_y = - self.delta_y








