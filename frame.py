#!/usr/bin/env python3
"""Main frame."""

import urwid

from get_menu_items import MENU_ITEMS, TEXT_MAIN_MENU, EXIT_KEY
from buttons import MenuButton, CheckBoxButton
from boxes import SubMenu, ActionBox


class MainFrame(urwid.WidgetPlaceholder):
    # TODO: add the exit_key param
    def __init__(self):
        super().__init__(urwid.SolidFill(u'\N{MEDIUM SHADE}'))

        self.box_level = 0

        sub_menu = SubMenu('Main menu', TEXT_MAIN_MENU, self,
                           top_level=True,
                           contents=self._load_menu(MENU_ITEMS))
        self.open_box(sub_menu)

    #
    # Private methods
    #

    def _load_menu(self, obj, checkbox=False):
        lst = []  # TODO: come up with more suitable name
        if isinstance(obj, dict):
            if obj["items"] is None:
                if checkbox:
                    return CheckBoxButton(obj["name"])
                else:
                    return ActionBox(obj["name"], obj["text"], self,
                                     script=obj.get("script", '')).button
            else:
                checkbox = True if obj.get("checkbox", 'n') == 'y' else False
                return SubMenu(obj["name"], obj["text"], self,
                               top_level=False,
                               contents=self._load_menu(obj["items"], checkbox),
                               chkbox_group=checkbox,
                               script=obj.get("script", "")).button
        for item in obj:
            lst.append(self._load_menu(item, checkbox))
        return lst

    def _exit_confirmation(self):
        response = urwid.Text(['Do you really want to leave?'])

        def really_exit(button):
            return self._exit_program()

        apply = MenuButton('OK', really_exit)
        back_to_menu = MenuButton('Back', self.back)
        widget_list = [response, urwid.Divider(), apply, back_to_menu]
        box = urwid.Filler(urwid.Pile(widget_list))
        self.open_box(box)

    def _exit_program(self):
        raise urwid.ExitMainLoop()

    #
    # Public methods
    #

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
                                             self.original_widget,
                                             align='center',
                                             width=('relative', 20),
                                             valign='middle',
                                             height=('relative', 20),
                                             min_width=60, min_height=20)
        self.box_level += 1

    def keypress(self, size, key):
        if key == EXIT_KEY:
            self._exit_confirmation()

        return super().keypress(size, key)

    def item_chosen(self, button, param):
        print('item chosen')

    def back(self, button):
        if self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
