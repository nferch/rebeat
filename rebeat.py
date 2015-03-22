#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk


import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import wave
import struct

import audioselector

import sys
if len(sys.argv) < 2:
    sys.stderr.write("usage: %s <audiofile>\n" % sys.argv[0])
    sys.exit(1)

w = wave.open(sys.argv[1])
assert w.getsampwidth() == 2
raw = w.readframes(w.getnframes())
frames = [struct.unpack("<h", raw[i:i+2])[0] / float(2**15)
          for i in range(0, len(raw), 2)]
fps = w.getframerate()*2

class ReBeatApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, None)
        self.grid()

        self.audio = audioselector.AudioSelector(self, frames, fps,
                                                 highlightthickness=0)
        self.audio.grid(column=0, row=0, columnspan=2)

        self.slider = tk.Scale(self, from_=0, to=len(frames),
                               orient=tk.HORIZONTAL,
                               borderwidth=0)
        self.slider.grid(row=1, column=0, columnspan=2, sticky=tk.EW)

        self.button = tk.Button(self, text="close", command=self.quit)
        self.button.grid(row=2, column=0)

        self.button = tk.Button(self, text="play", command=self.play)
        self.button.grid(row=2, column=1)

        self.marks = []

        import pyaudio
        self.p = pyaudio.PyAudio()

    def partition_created(self, time):
        import bisect
        bisect.insort(self.marks, time)
        print self.marks

    def play(self):
        stream = self.p.open(format=self.p.get_format_from_width(2),
                             channels=2,
                             rate=fps/2,
                             output=True)
        samples = []
        start = 0
        for mark in self.marks + [len(frames)]:
            end = int(mark * fps)*2
            stream.write(raw[start:end])
            stream.write(raw[start:end])
            stream.write(raw[start:end])
            stream.write(raw[start:end])
            stream.write(raw[start:end])
            start = end
        stream.stop_stream()
        stream.close()



if __name__ == "__main__":
    app = ReBeatApp()
    app.title("ReBeat")
    print len(frames)
    app.mainloop()
    #app.destroy()