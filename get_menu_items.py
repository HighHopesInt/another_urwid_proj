#!/usr/bin/env python3
"""Importing settings from file."""

import yaml

MENU = {"menu_items": [], "exit_key": 'q', "text_main_menu": ""}

with open("settings.yaml", 'r') as stream:
    try:
        MENU = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

MENU_ITEMS = MENU["menu_items"]
EXIT_KEY = MENU["exit_key"]
TEXT_MAIN_MENU = MENU["text_main_menu"]
