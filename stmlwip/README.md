# stm32cube-platformio-lwip
This library links in the version of LwIP shipped with the STM32Cube framework.

Configuration is possible with extra options in the platformio.ini. These are looked up relative to the current environment.
These are:

    - custom_lwip_opts_location: *REQUIRED* must point to either a path containing lwipopts.h or the file itself.
