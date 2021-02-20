from os.path import dirname, join, exists, isdir, basename
Import('env')

custom_lwip_location = env.GetProjectOption("custom_lwip_opts_location", None)
if custom_lwip_location is None:
    raise ValueError("Please set custom_lwip_opts_location in your platformio.ini to the location of a lwipopts.h header file -- relative to the location of platformio.ini")

if not isdir(custom_lwip_location):
    if basename(custom_lwip_location) != "lwipopts.h":
        raise ValueError("The file must be named lwipopts.h; if you want different ones per environment put them in separate folders.")
    custom_lwip_location = join(env.get("PROJECT_DIR"), dirname(custom_lwip_location))

if not exists(custom_lwip_location):
    raise ValueError("That custom_lwip_opts_location does not exist.")

env.Append(CPPPATH=[custom_lwip_location,
                    Dir(join("include", "arch")).srcnode().abspath
])
