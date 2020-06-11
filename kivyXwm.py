#!/usr/bin/env python

from Xlib.display import Display
from Xlib import X


def resize(title=str, height=int, width=int):
    TITLE = title
    HEIGHT = height
    WIDTH = width

    display = Display()
    root = display.screen().root
    windowIDs = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'),
                                       X.AnyPropertyType).value
    for windowID in windowIDs:
        window = display.create_resource_object('window', windowID)
        title = window.get_wm_name()
        pid = window.get_full_property(display.intern_atom('_NET_WM_PID'),
                                       X.AnyPropertyType)
        if TITLE in title:
            window.configure(width=WIDTH, height=HEIGHT)
            display.sync()