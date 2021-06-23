#!/usr/bin/env python3

import tkinter
import settings

class View:
    def __init__(self, root):
        self.t = 0
        self.t_max = settings.total_ticks
        self.window = root
        settings.config_window(self.window)
        self.canvas = tkinter.Canvas(self.window)
        settings.config_canvas(self.canvas)
        self.model = settings.prepare_model(self.canvas)

    def run(self):
        if self.t < self.t_max:
            for each in self.model:
                each.rule()
                each.go()
                each.redraw()
            self.t += 1
            self.canvas.after(settings.animation_refresh_milliseconds, self.run)
        else:
            settings.logger("ticks:"+str(self.t))

tk = tkinter.Tk()
widget = View(tk)
widget.run()
tk.mainloop()



