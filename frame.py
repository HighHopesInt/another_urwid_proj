#!/usr/bin/env python3
"""
Main frame module.
"""

import urwid

from boxes import SubMenu, ActionBox
from buttons import MenuButton, CheckBoxButton
from get_menu_items import MENU_ITEMS, TEXT_MAIN_SCREEN, EXIT_KEY, \
    TITLE_MAIN_SCREEN


class MainFrame(urwid.WidgetPlaceholder):
    """
    Main window of the application.
    Loads the menu tree from the configuration file and walk over this tree.
    Handles general key events.
    """
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
        """ Builds the whole menu objects tree recursively.
        :param obj: current node of the tree;
        :param checkbox: True if this node is a checkbox group;
        :return: (list of) current node contents;
        """
        structure = []
        if isinstance(obj, dict):
            name = obj['name']
            text = obj['text']
            items = obj['items']
            script = obj.get('script', '')
            if obj["items"] is None:
                if checkbox:
                    return CheckBoxButton(name)
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
        """
        Shows the exit confirmation box with common action buttons.
        """
        response = urwid.Text(['Do you really want to leave?'])

        def really_exit(_button):
            """ Actual exit. """
            return self._exit_program()

        apply = MenuButton('OK', really_exit)
        back_to_menu = MenuButton('Back', self.back)
        widget_list = [response, urwid.Divider(), apply, back_to_menu]
        box = urwid.Filler(urwid.Pile(widget_list))
        self.open_box(box)

    def _exit_program(self):
        """ Exits from the program (main loop). """
        raise urwid.ExitMainLoop()

    #
    # Public methods
    #

    def open_box(self, box):
        """
        Displays the contents of the box,
        keeping current tree level.
         """
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
        """ Handles general keypress. """
        if key == EXIT_KEY:
            self._exit_confirmation()
        return super().keypress(size, key)

    def back(self, _button):
        """ Returns back out of the box. """
        if self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1

    def output_script(self, text):
        """
        Shows the output of script.
        """
        back_to_menu = MenuButton('Back', self.back)
        scrolling = urwid.Pile([urwid.Text(text)])
        output = urwid.ListBox(urwid.SimpleListWalker([scrolling]))
        box = urwid.Pile([output, ('pack', back_to_menu)])
        self.open_box(box)
