#!/usr/bin/env python3
"""Boxes."""

import urwid

from buttons import MenuButton, ScriptButton


class MenuBtnGroup(urwid.WidgetWrap):
    """Menu button group."""
    def __init__(self, button_group):
        super().__init__(urwid.GridFlow(button_group, 20, 1, 1, 'center'))


class Box(urwid.WidgetWrap):
    """Base box class."""
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
        """
        Calls parent frame method of displaying the box.
        :param button:
        :param frame: parent frame
        :return: parent frame method call
        """
        return frame.open_box(self)

    def clear_edited(self):
        """
        Clears all editable fields (turns them to default state).
        This method should be overrided in child classes.
        """
        raise NotImplementedError


class SubMenu(Box):
    """Represents submenu box."""
    def __init__(self, title, text, frame,
                 top_level=False,
                 contents=None,
                 checkbox_group=False,
                 script=''):

        self.actions = []
        self.parameters = []
        self.count_click_select_all = 0
        self.checkbox_group = checkbox_group
        self.elements = contents[:]

        if self.checkbox_group:
            for item in self.elements:
                urwid.connect_signal(item, 'change', self.checkbox_changed)

            self.actions.append(
                MenuButton('Select all...', self.select_all, self.elements)
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
        """ Select all checkboxes. """
        for i in choices:
            if self.count_click_select_all % 2 == 0:
                i.set_state(True)
            else:
                i.set_state(False)
        self.count_click_select_all += 1

    def checkbox_changed(self, button, data=None):
        """ Checkbox change event. """
        if button.state:
            self.parameters.append(button.label)
        else:
            try:
                self.parameters.remove(button.label)
            except ValueError:
                pass

    def clear_edited(self):
        """ Clear editable fields. """
        if self.checkbox_group:
            [i.set_state(False) for i in self.elements if i.state]


class ActionBox(Box):
    """ Represents single action box with no child boxes. """
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

    def clear_edited(self):
        """Do nothing, as this box does not have editable elements yet."""
        pass
