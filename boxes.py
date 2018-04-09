#!/usr/bin/env python3
import urwid
from buttons import MenuButton


class MenuBtnGroup(urwid.WidgetWrap):
    # self, choices_checkbox, sel_all_btn=False, apply_btn=False
    def __init__(self,
                 frame,
                 choices_checkbox=False,
                 sel_all_btn=False,
                 apply_btn=False):
        button_group=[]
        # if sel_all_btn:
        #     button=urwid.Button('Select all')
        #
        #     # def select_all(button):
        #     #     [i.set_state(True) for i in choices_checkbox if not i.state]
        #
        #     # urwid.connect_signal(button, 'click', select_all)
        #     button_group.append(
        #         urwid.AttrMap(button, 'bg', focus_map='reversed'))


        button_group.append(urwid.Button('Back', frame.back))

        # if apply_btn:
        #     button_group.append(buttons.apply_button(self))

        super().__init__(urwid.GridFlow(button_group, 15, 1, 1, 'center'))


class Box(urwid.WidgetWrap):
    def __init__(self, title, text, frame, contents=None):
        self.body=[urwid.Text(title), urwid.Divider()]
        if text:
            self.body.append(urwid.Text(text))
        if contents:
            self.body.extend(contents)
        super().__init__(
            urwid.ListBox(urwid.SimpleFocusListWalker(self.body)))
        self.button = MenuButton(title, self.open, frame)
        self.frame = frame

    def open(self, button, frame):
        return frame.open_box(self)


class SubMenu(Box):
    def __init__(self, title, text, frame, top_level=False, contents=None):
        super(SubMenu, self).__init__(title, text, frame, contents)

        if not top_level:
            self.body.append(MenuBtnGroup(frame,
                choices_checkbox=False,
                sel_all_btn=False,
                apply_btn=False
            ))


class InfoBox(Box):
    def __init__(self, title, text, frame, contents=None):
        super(InfoBox, self).__init__(title, text, frame, contents)