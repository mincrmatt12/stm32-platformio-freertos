try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from os.path import dirname, join, exists, isdir, basename
Import('env')

config = configparser.ConfigParser()
config.read(env.get("PROJECT_CONFIG"))

try:
    custom_freertos_location = config.get("env:" + env.get("PIOENV"), "custom_freertos_config_location")
except configparser.NoOptionError:
    raise ValueError("Please set custom_freertos_config_location in your platformio.ini to the location of a FreeRTOSConfig.h header file -- relative to the location of platformio.ini")

if not isdir(custom_freertos_location):
    if basename(custom_freertos_location) != "FreeRTOSConfig.h":
        raise ValueError("The file must be named FreeRTOSConfig.h; if you want different ones per environment put them in separate folders.")
    custom_freertos_location = join(env.get("PROJECT_DIR"), dirname(custom_freertos_location))

if not exists(custom_freertos_location):
    raise ValueError("That custom_freertos_config_location does not exist.")

env.Append(CPPPATH=[custom_freertos_location])

# compute the include path for this CPU

cpu_name = env.BoardConfig().get("build.cpu")
foldername = {
    "cortex-m3": "ARM_CM3",
    "cortex-m0": "ARM_CM0",
    "cortex-m4": "ARM_CM4F",
    "cortex-m7": "ARM_CM7"
}[cpu_name]

try:
    heap_impl = config.get("env:" + env.get("PIOENV"), "custom_freertos_heap_impl")
except configparser.NoOptionError:
    heap_impl = "heap_4.c"

try:
    extra_features = config.get("env:" + env.get("PIOENV"), "custom_freertos_features").split(",")
    extra_features = [x.strip() for x in extra_features]
except configparser.NoOptionError:
    extra_features = []

incpath = join("src", "portable", "GCC", foldername)
src_filter = ["+<*>", "-<portable/*>", "+<portable/MemMang/{}>".format(heap_impl), "+<portable/GCC/{}/*.c>".format(foldername)]
src_filter.append("-<croutine.c>" if "coroutines" not in extra_features else "+<croutine.c>")
src_filter.append("-<timers.c>" if "timers" not in extra_features else "+<timers.c>")
src_filter.append("-<event_groups.c>" if "event_groups" not in extra_features else "+<event_groups.c>")
src_filter.append("-<stream_buffer.c>" if "stream_buffers" not in extra_features else "+<stream_buffer.c>")
env.Replace(SRC_FILTER=
        src_filter
)
env.Append(CPPPATH=
        [Dir(incpath).srcnode().abspath,
         Dir(join("src", "CMSIS_RTOS")).srcnode().abspath]
)
