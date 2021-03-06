#!/usr/bin/env python3
import os
import sys
import django

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        open('current_app.txt').read().strip() + ".settings"
    )
    django.setup()
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
