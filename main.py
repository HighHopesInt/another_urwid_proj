#!/usr/bin/env python3
import urwid
from frame import MainFrame


palette = [
    ('reversed', 'standout', ''),
    ('bg', 'bold', 'dark blue'),
    ('bg_back', 'bold', 'black'), ]


top = MainFrame()

urwid.MainLoop(top, palette=palette).run()

