#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import audioselector
import beatgrid
import player

import sys
if len(sys.argv) < 2:
    sys.stderr.write("usage: %s <audiofile>\n" % sys.argv[0])
    sys.exit(1)


class ReBeatApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, None,)
        self.configure(background='white')
        self.grid()

        self.player = player.Player(sys.argv[1])

        # UI components from top to bottom
        # Audio visualization and selection
        self.audio = audioselector.AudioSelector(self,
                                                 self.player.get_signal(),
                                                 self.player.get_fps(),
                                                 highlightthickness=0)
        self.audio.grid(column=0, row=0, columnspan=2)
        self.audio.on_create_selection(self.selection_created)
        self.audio.on_create_mark(self.audiomark_created)
        self.audio.focus_set()

        # Step sequencer style grid
        self.beats = beatgrid.BeatGrid(self)
        self.beats.grid(row=1, columnspan=2, sticky="EW")
        self.beats.on_play(self.audiomark_play)
        self.beats.on_kill(self.audiomark_kill)
        self.beats.add_row()

        # Selection of resolution and number of bars
        self.bars = tk.Spinbox(self, from_=1, to=16)
        self.bars.grid(row=2, column=0)
        self.resolution = tk.Spinbox(self, values=(1,2,4,8,16))
        self.bars.grid(row=2, column=1)

    def audiomark_created(self, i, start):
        print start
        self.beats.add_row(i)

    def selection_created(self, start, end):
        print "selection", start, end
        print "all", self.audio.get_selections()

    def audiomark_kill(self, i):
        print "kill partition", i

    def audiomark_play(self, i):
        # hack. should s/mark/partition/ and get them as ranges
        x = self.audio.get_marks()
        x.insert(0, 0.0)
        self.player.play(x[i], x[i+1])

if __name__ == "__main__":
    app = ReBeatApp()
    app.title("ReBeat")
    app.mainloop()
    #app.destroy()
