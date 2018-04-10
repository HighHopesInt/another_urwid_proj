#!/usr/bin/env python3
"""Importing settings from file."""

import yaml

MENU = {"menu_items": [], "exit_key": 'q', "text_main_screen": "",
        "title_main_screen": "", "path_to_scripts": ""}

with open("settings.yaml", 'r') as stream:
    try:
        MENU = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

MENU_ITEMS = MENU["menu_items"]
EXIT_KEY = MENU["exit_key"]
TITLE_MAIN_SCREEN = MENU["title_main_screen"]
TEXT_MAIN_SCREEN = MENU["text_main_screen"]
PATH_TO_SCRIPTS = MENU["path_to_scripts"]

RESERVE_SCRIPT = "./scripts/reserve.py"
