#!/usr/bin/env python3
"""Buttons."""

import urwid

import subprocess

from get_menu_items import PATH_TO_SCRIPTS, RESERVE_SCRIPT


class MenuButton(urwid.Button):
    def __init__(self, caption='', callback=None, param=None):
        super(MenuButton, self).__init__(caption)
        if callback:
            urwid.connect_signal(self, 'click', callback, param)

        # TODO: use curses to hide cursor
        self._w = urwid.AttrMap(urwid.SelectableIcon([
            '  \N{BULLET} ', caption
        ], 100), None, 'reversed')


class ScriptButton(MenuButton):
    def __init__(self, caption='', script='', parameters=None,
                 confirmation=False):
        super(ScriptButton, self).__init__(caption)

        self.script = script
        self.parameters = parameters
        self.confirmation = confirmation

        if script:
            urwid.connect_signal(self, 'click', self.run_script, script)

    def run_script(self, button, script):
        scr = ""
        try:
            open(PATH_TO_SCRIPTS + script)
            scr = PATH_TO_SCRIPTS + script
        except FileNotFoundError:
            scr = RESERVE_SCRIPT
        finally:
            running = subprocess.Popen([scr], stdout=subprocess.PIPE)
            [print(line) for line in iter(running.stdout.readline, b'')]


class CheckBoxButton(urwid.CheckBox):
    def __init__(self, title):
        super(CheckBoxButton, self).__init__(title)
