#!/usr/bin/env python3

import tkinter
import settings
import profile

import random
random.seed(profile.random_seed)

class View:
    def __init__(self, root):
        self.t_max = settings.total_ticks
        self.window = root
        settings.config_window(self.window)
        self.canvas = tkinter.Canvas(self.window)
        settings.config_canvas(self.canvas)
        self.map = settings.Map(self.canvas)
        self.patch_list, self.turtle_set = self.map.prepare_model()

    def run(self):
        if settings.global_t < self.t_max:

            self.map.demand()

            for each in self.patch_list:
                each.rule()
            # debug later
            for each in list(self.turtle_set):
                if each.finished:
                    self.turtle_set.remove(each)
            for each in self.turtle_set:
                each.rule()

            for each in self.patch_list:
                each.go()
            for each in self.turtle_set:
                each.go()

            for each in self.turtle_set:
                each.redraw()

            settings.global_t += 1
            self.canvas.after(settings.animation_refresh_milliseconds, self.run)
        else:
            settings.print_all()


tk = tkinter.Tk()
widget = View(tk)
widget.run()
tk.mainloop()



