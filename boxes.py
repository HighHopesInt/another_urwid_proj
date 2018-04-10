#!/usr/bin/env python3
"""Boxes."""

import urwid

from buttons import MenuButton, ScriptButton


class MenuBtnGroup(urwid.WidgetWrap):
    def __init__(self, button_group):
        super().__init__(urwid.GridFlow(button_group, 20, 1, 1, 'center'))


class Box(urwid.WidgetWrap):
    # TODO: rework params
    def __init__(self, title, text, frame, contents=None):
        self.body = [urwid.Text(title), urwid.Divider()]

        if text:
            self.body.extend([urwid.Text(text), urwid.Divider()])

        if contents:
            self.body.extend(contents)

        self.button = MenuButton(title, self.open, frame)
        self.frame = frame

        super().__init__(
            urwid.ListBox(urwid.SimpleFocusListWalker(self.body)))

    def open(self, button, frame):
        return frame.open_box(self)


class SubMenu(Box):
    def __init__(self, title, text, frame,
                 top_level=False,
                 contents=None,
                 checkbox_group=False,
                 script=''):

        self.actions = []
        self.parameters = []
        self.count_click_select_all = 0

        if checkbox_group:
            self.actions.append(
                MenuButton('Select all...', self.select_all, contents)
            )

        self.actions.append(MenuButton('Back', frame.back))

        if script:
            self.actions.append(ScriptButton('Apply...',
                                             script=script,
                                             parameters=self.parameters,
                                             confirmation=True))
        body = contents[:]

        if not top_level and contents:
            body.append(MenuBtnGroup(self.actions))

        super().__init__(title, text, frame, body)

    def select_all(self, button, choices):
        for i in choices:
            if self.count_click_select_all % 2 == 0:
                i.set_state(True)
            else:
                i.set_state(False)
        self.count_click_select_all += 1


class ActionBox(Box):
    def __init__(self, title, text, frame, contents=None, script=''):
        self.actions = []
        self.parameters = []

        self.actions.append(MenuButton('Back', frame.back))
        if script:
            self.actions.append(ScriptButton('Apply...',
                                             script=script,
                                             parameters=self.parameters,
                                             confirmation=True))

        body = []
        if contents:
            body.extend(contents)

        body.append(MenuBtnGroup(self.actions))

        super().__init__(title, text, frame, body)
