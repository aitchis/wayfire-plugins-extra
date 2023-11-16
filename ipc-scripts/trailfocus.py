#!/usr/bin/python3

import os
import sys
from wayfire_socket import *

addr = os.getenv('WAYFIRE_SOCKET')

commands_sock = WayfireSocket(addr)
commands_sock.watch()

def sort_views():
    i = 0
    for v in commands_sock.list_views():
        if v["app-id"] == "$unfocus panel" or v["layer"] == "background":
            continue
        if v["state"] != {} and v["state"]["minimized"]:
            continue
        i += 1
    o_step = 0.2 / i
    b_step = 0.5 / i
    s_step = 1.0 / i
    o_value = 0.8
    b_value = 0.5
    s_value = 0.0
    for v in commands_sock.list_views()[::-1]:
        if v["app-id"] == "$unfocus panel" or v["layer"] == "background":
            continue
        if v["state"] != {} and v["state"]["minimized"]:
            continue
        o_value += o_step
        b_value += b_step
        s_value += s_step
        commands_sock.set_view_opacity(v["id"], o_value, 1000)
        commands_sock.set_view_brightness(v["id"], b_value, 1000)
        commands_sock.set_view_saturation(v["id"], s_value, 1000)

sort_views()

while True:
    try:
        msg = commands_sock.read_message()
    except KeyboardInterrupt:
        for v in commands_sock.list_views():
            commands_sock.set_view_opacity(v["id"], 1.0, 500)
            commands_sock.set_view_brightness(v["id"], 1.0, 500)
            commands_sock.set_view_saturation(v["id"], 1.0, 500)
        exit(0)

    if "event" in msg and msg["event"] == "view-focused":
        sort_views()