#!/usr/bin/env python3
"""Buttons."""

import urwid

import subprocess

from get_menu_items import PATH_TO_SCRIPTS, RESERVE_SCRIPT


class MenuButton(urwid.Button):
    """
    Base button class.
    """
    def __init__(self, caption='', callback=None, param=None):
        """
        :param caption: button label (str);
        :param callback: function
        :param param: function parameter
        """
        super(MenuButton, self).__init__(caption)
        if callback:
            urwid.connect_signal(self, 'click', callback, param)

        self._w = urwid.AttrMap(
            urwid.SelectableIcon(
                ['[ ', caption, ' ]'], 100), None, 'reversed')


class ScriptButton(MenuButton):
    """
    Script running button.
    """
    def __init__(self, caption='', script='', parameters=None,
                 confirmation=False):
        """
        :param caption: label (str)
        :param script: (str)
        :param parameters: script parameters (list)
        :param confirmation: (bool)
        """
        super(ScriptButton, self).__init__(caption)

        self.script = script
        self.parameters = parameters
        self.confirmation = confirmation

        if script:
            urwid.connect_signal(self, 'click', self.run_script)

    def run_script(self, button):
        scr = ""
        try:
            open(PATH_TO_SCRIPTS + self.script)
            # self.parameters = ['a', 'b', 'c']
            scr = [PATH_TO_SCRIPTS + self.script]
            scr.extend(self.parameters)
        except FileNotFoundError:
            scr = RESERVE_SCRIPT
        finally:
            running = subprocess.Popen(scr, stdout=subprocess.PIPE)
            [print(line) for line in iter(running.stdout.readline, b'')]


class CheckBoxButton(urwid.CheckBox):
    def __init__(self, caption):
        """
        :param caption: checkbox label (str)
        """
        super(CheckBoxButton, self).__init__(caption)
