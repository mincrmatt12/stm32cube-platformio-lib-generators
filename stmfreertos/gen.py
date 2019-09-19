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
    "name": "STM32Cube Middleware-FreeRTOS",
    "keywords": "rtos",
    "description": """This library links in the version of FreeRTOS shipped with the STM32Cube framework.

Configuration is possible with extra options in the platformio.ini.
These are:

    - custom_freertos_config_location: *REQUIRED* must point to either a path containing FreeRTOSConfig.h or the file itself.
    - custom_freertos_heap_impl: *OPTIONAL, defaults to heap_4.c* heap implementation file to use (see FreeRTOS docs)
    - custom_freertos_features: *OPTIONAL*, comma separated list of optional files to build, any of ["coroutines", "timers", "event_groups", "stream_buffers"]

There is currently no support for the MPU.
If you use the RTOS heap you may want to disable allocation of a heap in the link script.
A good starting point for the FreeRTOSConfig.h is in the include directory, and can be used a default by using

```
#include "FreeRTOSConfig_template.h"
```

as your FreeRTOSConfig.h, or by simply copying its contents which is the preferred method if you plan to modify values in it.
""",
    "repository":
    {
        "type": "git",
        "url": "https://github.com/mincrmatt12/stm32-platformio-freertos.git"
    },
    "authors": [
        {
            "name": "Matthew Mirvish",
            "maintainer": True
        },
        {
            "name": "STMicroelectronics & FreeRTOS developers"
        }
    ],
    "platforms": "ststm32",
    "frameworks": "stm32cube",
    "version": version,
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

shutil.copytree(os.path.join(CUBE, "Middlewares/Third_Party/FreeRTOS/Source"), os.path.join("librepo", "src"))
print("done.")
print("cleaning up...")
shutil.move(os.path.join("librepo", "src/include"), os.path.join("librepo", "include"))
shutil.rmtree(os.path.join("librepo", "src/CMSIS_RTOS_V2"))
shutil.rmtree(os.path.join("librepo", "src/portable/IAR"))
shutil.rmtree(os.path.join("librepo", "src/portable/Keil"))
shutil.rmtree(os.path.join("librepo", "src/portable/Tasking"))
shutil.rmtree(os.path.join("librepo", "src/portable/RVDS"))
print("adding script...")
shutil.copy("./add_config.py", "librepo/add_config.py")
print("adding license...")
shutil.copy(os.path.join(CUBE, "Middlewares/Third_Party/FreeRTOS/License/license.txt"), "librepo")
print("generated.")

