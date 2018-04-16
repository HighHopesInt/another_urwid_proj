#!/usr/bin/env python3
"""Boxes. """

import urwid

from buttons import MenuButton, ScriptButton


class MenuBtnGroup(urwid.WidgetWrap):
    """Menu button group. """
    def __init__(self, button_group):
        attr_button_group = []
        for item in button_group:
            attr_button_group.append(urwid.AttrMap(item, 'button'))

        super().__init__(urwid.GridFlow(attr_button_group, 20, 1, 1, 'center'))


class Box(urwid.WidgetWrap):
    """Base box class. """
    # TODO: rework params
    def __init__(self, title, text, frame, contents=None, actions=None):

        _header = urwid.Pile(
            [
                ('pack', urwid.Text(('title', title))),
                ('pack', urwid.Divider())
            ]
        )

        if text:
            _header.contents.extend(
                [
                    (urwid.Text(text), _header.options()),
                    (urwid.Divider('-'), _header.options())
                ]
            )

        self.body = []

        if contents:
            self.body.extend(contents)

        _body = urwid.ListBox(
                    urwid.SimpleFocusListWalker(self.body)
                )

        action_box = urwid.Pile([])

        if actions:
            action_box.contents.append((urwid.Divider('-'),
                                        action_box.options()))
            action_box.contents.append((MenuBtnGroup(self.actions),
                                        action_box.options()))

        _footer = action_box
        if _footer.contents:
            _footer.focus_position = 1  # the first one is Divider

        self.button = MenuButton(title, self.open, frame)
        self.frame = frame

        super().__init__(urwid.Pile([
            ('pack', _header),
            _body,
            ('pack', _footer)
        ]))

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
    """Submenu box. """
    def __init__(self, title, text, frame,
                 top_level=False,
                 contents=None,
                 checkbox_group=False,
                 script='', sub=False):

        self.actions = []
        self.parameters = []
        self.count_click_select_all = 0
        self.checkbox_group = checkbox_group
        self.elements = contents[:]

        item_name = title + " ..." if sub else title

        if self.checkbox_group:
            for item in self.elements:
                urwid.connect_signal(item, 'postchange', self.checkbox_changed)

            self.actions.append(
                MenuButton('Select all...', self.select_all)
            )

        if not top_level:
            self.actions.append(MenuButton('Back', frame.back))

        if script:
            self.actions.append(ScriptButton('Apply...',
                                             script=script,
                                             parameters=self.parameters,
                                             output=frame,
                                             confirmation=True))
        body = contents[:]

        super().__init__(title, text, frame, body, self.actions)

    def select_all(self, button):
        """Selects all checkboxes. """
        for i in self.elements:
            if self.count_click_select_all % 2 == 0:
                i.set_state(True)
            else:
                i.set_state(False)
        self.count_click_select_all += 1

    def checkbox_changed(self, button, data=None):
        """Checkbox change event. """
        if button.state:
            self.parameters.append(button.label)
        else:
            try:
                self.parameters.remove(button.label)
            except ValueError:
                pass

    def clear_edited(self):
        """Clears editable fields. """
        if self.checkbox_group:
            for i in self.elements:
                if i.state:
                    i.set_state(False)
            self.count_click_select_all = 0


class ActionBox(Box):
    """ Single action box with no child boxes. """
    def __init__(self, title, text, frame, contents=None, script=''):
        self.actions = []
        self.parameters = []
        item_name = title

        self.actions.append(MenuButton('Back', frame.back))
        if script:
            self.actions.append(ScriptButton('Apply...',
                                             script=script,
                                             parameters=self.parameters,
                                             output=frame,
                                             confirmation=True))

        body = []
        if contents:
            body.extend(contents)

        body.append(MenuBtnGroup(self.actions))

        super().__init__(title, text, frame, body, item_name)

    def clear_edited(self):
        """Does nothing, as this box does not have editable elements yet. """
        pass
