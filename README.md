This generates a bunch of `platformio` libraries. These can then be pushed to GitHub to be able to use FreeRTOS and LWIP in a platformio stm32cube project.

## Layout

The `cube` submodule contains the original cube sources that will be packaged.
The `examples` show how to use the libraries since they work a little different to most.

The other folders contain scripts that will create a folder called `librepo`, which is the final library.

## Usage

Go into each library folder and run `gen.py`. You now have a bunch of platformio libraries. Alternatively, simply import them from the pio registry.
