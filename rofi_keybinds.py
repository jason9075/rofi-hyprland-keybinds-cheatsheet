#!/usr/bin/env python3

import json
import subprocess
import re

modmask_map = {
    64: "SUPER",
    8: "ALT",
    4: "CTRL",
    1: "SHIFT",
}


def modmask_to_key(modmask: int) -> str:
    res = []
    for bf, key in modmask_map.items():
        if modmask & bf == bf:
            res.append(key)
            modmask -= bf
    if modmask != 0:
        res.append(f"({modmask})")
    if len(res) > 0:
        res.append("+ ")
    return " ".join(res)


bindmap = ""
for bind in json.loads(subprocess.check_output(["hyprctl", "binds", "-j"])):
    bindmap += f'<b>{modmask_to_key(bind['modmask'])}{bind['key']}</b> <i>{bind["description"]}</i> <span color="gray">{bind["dispatcher"]}</span> <span color="lightgray">{bind["arg"]}</span>\n'

choice = subprocess.check_output(["rofi", "-dmenu", "-i", "-markup-rows", "-p", "Hyprland Keybinds:"], input=bindmap, text=True)

pattern = r'<span color="gray">(.*?)</span> <span color="lightgray">(.*?)</span>'
match = re.search(pattern, choice)

if match:
    dispatcher = match.group(1)
    args = match.group(2)

    cmd = f"hyprctl dispatch {dispatcher} {args}"
    if dispatcher == "exec":
        cmd = args

    subprocess.run(cmd, shell=True)
