#!/usr/bin/env python3

import urwid

from get_menu_items import EXIT_KEY
from frame import MainFrame


def main():

    palette = [
        ('body', 'default', 'dark cyan', 'standout'),
        ('foot', 'light gray', 'black'),

        ('key', 'light cyan, bold', 'black', 'underline'),

        ('title', 'white, bold', 'dark cyan',),
        ('button', 'white, bold', 'dark cyan'),

        ('default_bold', 'bold', 'black',),
        ('reversed', 'standout', ''),
    ]

    splitter = ' | '

    footer_text = [
        ('default_bold', "Provisioning system"), splitter,
        ('key', "UP"), ", ",
        ('key', "DOWN"), " basic navigation", splitter,
        ('key', EXIT_KEY), " exits",
    ]

    footer = urwid.AttrMap(urwid.Text(footer_text), 'foot')
    top = urwid.Frame(urwid.AttrWrap(MainFrame(), 'body'), footer=footer)

    urwid.MainLoop(top, palette=palette).run()


if __name__ == "__main__":
    main()
