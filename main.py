#!/usr/bin/env python3
"""Main module."""

import urwid

from get_menu_items import EXIT_KEY
from frame import MainFrame


def main():
    """Initialize the main frame and run main loop."""

    palette = [
        ('body', 'bold', 'dark cyan', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('title', 'white', 'black',),
        ('reversed', 'standout', ''),
    ]

    splitter = ' | '

    footer_text = [
        ('title', "Provisioning system"), splitter,
        ('key', "UP"), ", ",
        ('key', "DOWN"), " basic navigation", splitter,
        ('key', EXIT_KEY), " exits",
    ]

    footer = urwid.AttrMap(urwid.Text(footer_text), 'foot')
    top = urwid.Frame(urwid.AttrWrap(MainFrame(), 'body'), footer=footer)

    urwid.MainLoop(top, palette=palette).run()


if __name__ == "__main__":
    main()
