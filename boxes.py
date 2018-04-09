#!/usr/bin/env python3
import urwid
from buttons import MenuButton, ScriptButton


class MenuBtnGroup(urwid.WidgetWrap):
    def __init__(self, button_group):
        super().__init__(urwid.GridFlow(button_group, 20, 1, 1, 'center'))


class Box(urwid.WidgetWrap):
    def __init__(self, title, text, frame, contents=None):
        self.body=[urwid.Text(title), urwid.Divider()]
        if text:
            self.body.append(urwid.Text(text))

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
                 chkbox_group=False,
                 script=''):

        self.actions = []
        self.parameters = []

        if chkbox_group:
            self.actions.append(MenuButton('Select all...', self.select_all, contents))

        self.actions.append(MenuButton('Back', frame.back))

        if len(script)>0:
            self.actions.append(ScriptButton('Apply...', script, self.parameters))

        body = contents[:]

        if not top_level and contents:
            body.append(MenuBtnGroup(self.actions))

        super().__init__(title, text, frame, body)

    def select_all(self, button, choices):
        [i.set_state(True) for i in choices if not i.state]





class InfoBox(Box):
    def __init__(self, title, text, frame, contents=None):
        super(InfoBox, self).__init__(title, text, frame, contents)