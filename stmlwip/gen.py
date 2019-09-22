#!/usr/bin/env python3
"""
Generate the files inside the 'librepo' directory from the upstream sources + create the necessary extra files

This file is intended to be ran from a CI as this entire process should be automatic
"""

import os
import shutil
import re
import json

CUBE = "../cube/f2"

# first, check if things exist
if not os.path.exists(CUBE):
    print("please run git submodule init")
    exit(1)
if not os.path.exists("librepo"):
    print("librepo does not exist.")
    exit(1)

# create library.json
#  get version
#  yes i know re's for xml are terrible, but i only need a parameter

with open(os.path.join(CUBE, "package.xml"), "r") as f:
    version = re.findall(r'DBVersion="([\d.]+)"', f.read())[0]

print("found cube version", version)

library_json = {
    "name": "STM32Cube Middleware-LwIP",
    "keywords": "socket",
    "description": """This library links in the STM32Cube version of LwIP to your project. It does _not_ include the stub ethernetif.c and other assorted files required to use the Ethernet library. These may be released as a separate library at some point
in the future, however for now copy them from an STM32CubeMX project. If you include the FreeRTOS library as well, a CubeMX project should compile under platformio.

<todo config>
""",
    "repository":
    {
        "type": "git",
        "url": "https://github.com/mincrmatt12/stm32-platformio-lwip.git"
    },
    "authors": [
        {
            "name": "Matthew Mirvish",
            "maintainer": True
        },
        {
            "name": "STMicroelectronics & LwIP developers"
        }
    ],
    "platforms": "ststm32",
    "frameworks": "stm32cube",
    "version": version,
    "dependencies": {
        "6696": version
    },
    "build": {
        "extraScript": "add_config.py"
    }
}

with open(os.path.join("librepo", "library.json"), "w") as f:
    json.dump(library_json, f, indent=4, sort_keys=True)

print("wrote lib.json")

print("copying sources...", end="")

if os.path.exists(os.path.join("librepo", "src")):
    shutil.rmtree(os.path.join("librepo", "src"))
if os.path.exists(os.path.join("librepo", "include")):
    shutil.rmtree(os.path.join("librepo", "include"))

shutil.copytree(os.path.join(CUBE, "Middlewares/Third_Party/LwIP/src"), os.path.join("librepo", "src"))
shutil.copytree(os.path.join(CUBE, "Middlewares/Third_Party/LwIP/system"), os.path.join("librepo", "src/system"))
print("done.")

print("cleaning up...")
shutil.move(os.path.join("librepo", "src/include"), os.path.join("librepo", "include"))
shutil.move(os.path.join("librepo", "src/system/arch"), os.path.join("librepo", "include/arch"))
shutil.move(os.path.join("librepo", "src/system/OS"), os.path.join("librepo", "src/systemOS"))
os.rmdir(os.path.join("librepo", "src/system"))
os.remove("librepo/src/Filelists.mk")
os.remove("librepo/src/FILES")
shutil.move(os.path.join("librepo", "src/systemOS"), os.path.join("librepo", "src/system"))
shutil.rmtree("librepo/src/apps")
print("adding script...")
shutil.copy("./add_config.py", "librepo/add_config.py")
print("adding license...")
shutil.copy(os.path.join(CUBE, "Middlewares/Third_Party/LwIP/COPYING"), "librepo")
print("generated.")
