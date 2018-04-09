#!/usr/bin/env python3
"""Main module."""

import urwid
from frame import MainFrame

# TODO: wrap everything into the main function


PALETTE = [
    ('reversed', 'standout', ''),
    ('bg', 'bold', 'dark blue'),
    ('bg_back', 'bold', 'black'), ]


TOP = MainFrame()

urwid.MainLoop(TOP, palette=PALETTE).run()
