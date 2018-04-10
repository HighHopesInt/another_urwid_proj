#!/usr/bin/env python3
"""Main frame."""

import urwid

from boxes import SubMenu, ActionBox
from buttons import MenuButton, CheckBoxButton
from get_menu_items import MENU_ITEMS, TEXT_MAIN_SCREEN, EXIT_KEY, \
    TITLE_MAIN_SCREEN


class MainFrame(urwid.WidgetPlaceholder):
    # TODO: add the exit_key param
    def __init__(self):
        super().__init__(urwid.SolidFill('/'))

        self.box_level = 0

        sub_menu = SubMenu(TITLE_MAIN_SCREEN, TEXT_MAIN_SCREEN, self,
                           top_level=True,
                           contents=self._load_menu(MENU_ITEMS))
        self.open_box(sub_menu)

    #
    # Private methods
    #

    def _load_menu(self, obj, checkbox=False):
        structure = []
        if isinstance(obj, dict):
            name = obj['name']
            text = obj['text']
            items = obj['items']
            script = obj.get('script', '')
            if obj["items"] is None:
                if checkbox:
                    return CheckBoxButton(obj["name"])
                else:
                    return ActionBox(name, text, self, script=script).button
            else:
                checkbox = True if obj.get("checkbox", 'n') == 'y' else False
                return SubMenu(name, text, self,
                               top_level=False,
                               contents=self._load_menu(items, checkbox),
                               checkbox_group=checkbox,
                               script=script).button
        for item in obj:
            structure.append(self._load_menu(item, checkbox))
        return structure

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
        if getattr(box, 'clear_edited', None):
            box.clear_edited()

        self.original_widget = urwid.Overlay(
            urwid.AttrMap(urwid.LineBox(box), None),
            self.original_widget,
            align='center',
            width=('relative', 95),
            valign='middle',
            height=('relative', 90))

        self.box_level += 1

    def keypress(self, size, key):
        if key == EXIT_KEY:
            self._exit_confirmation()
        return super().keypress(size, key)

    def back(self, button):
        if self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
