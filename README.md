# stm32cube-platformio-freertos
This library links in the version of FreeRTOS shipped with the STM32Cube framework.

Configuration is possible with extra options in the platformio.ini. These are looked up relative to the current environment.
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
