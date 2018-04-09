#!/usr/bin/env python3
import urwid
from get_menu_items import menu_items, text_main_menu, exit_key
from buttons import MenuButton, CheckBoxButton, ScriptButton
from boxes import SubMenu


class MainFrame(urwid.WidgetPlaceholder):
    def __init__(self):
        super().__init__(urwid.SolidFill(u'\N{MEDIUM SHADE}'))

        self.box_level = 0
        self.open_box(
            SubMenu('Main menu',
                    text_main_menu,
                    self,
                    top_level=True,
                    contents=self._load_menu(menu_items)
                    ))

    def _load_menu(self, obj, checkbox=False):
        lst = []
        if isinstance(obj, dict):
            if obj["items"] is None:
                if checkbox:
                    return CheckBoxButton(obj["name"])
                else:
                    return MenuButton(obj["name"], self.item_chosen, obj["script"])
            else:
                checkbox = True if obj.get("checkbox", 'n') == 'y' else False
                return SubMenu(obj["name"],
                               obj["text"],
                               self,
                               top_level=False,
                               contents=self._load_menu(obj["items"], checkbox),
                               chkbox_group=checkbox,
                               script=getattr(obj, "script", "")).button
        for item in obj:
            lst.append(self._load_menu(item, checkbox))
        return lst

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
        if key == exit_key:
            self.exit_confirmation()

        return super().keypress(size, key)

    def item_chosen(self, button, param):
        print('item chosen')

    def back(self, button):
        if self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1

    def exit_confirmation(self):
        response = urwid.Text(['Do you really want to leave?'])

        def really_exit(button):
            return self.exit_program()

        apply = MenuButton('OK', really_exit)
        back_to_menu = MenuButton('Back', self.back)
        box = urwid.Filler(urwid.Pile([response,
                                       urwid.Divider(),
                                       apply,
                                       back_to_menu]))
        self.open_box(box)

    def exit_program(self):
        raise urwid.ExitMainLoop()


palette = [
    ('reversed', 'standout', ''),
    ('bg', 'bold', 'dark blue'),
    ('bg_back', 'bold', 'black'), ]


# buttons = [
#     ScriptButton('first', 'sample script'),
#     MenuButton('second'),
#     MenuButton('third')
# ]

top = MainFrame()

# buttons.append(SubMenu('second', 'text', top).button)
#
# box = SubMenu('title', 'text', top, buttons)
#
# top.open_box(box)

urwid.MainLoop(top, palette=palette).run()

