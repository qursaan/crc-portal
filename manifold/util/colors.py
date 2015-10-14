# ANSI escape codes for terminals.
#  X11 xterm: always works, all platforms
#  cygwin dosbox: run through |cat and then colors work
#  linux: works on console & gnome-terminal
#  mac: untested
 
BLACK      = "\033[0;30m"
BLUE       = "\033[0;34m"
GREEN      = "\033[0;32m"
CYAN       = "\033[0;36m"
RED        = "\033[0;31m"
PURPLE     = "\033[0;35m"
BROWN      = "\033[0;33m"
GRAY       = "\033[0;37m"
BOLDGRAY   = "\033[1;30m"
BOLDBLUE   = "\033[1;34m"
BOLDGREEN  = "\033[1;32m"
BOLDCYAN   = "\033[1;36m"
BOLDRED    = "\033[1;31m"
BOLDPURPLE = "\033[1;35m"
BOLDYELLOW = "\033[1;33m"
WHITE      = "\033[1;37m"

MYGREEN    = '\033[92m'
MYBLUE     = '\033[94m'
MYWARNING  = '\033[93m'
MYRED      = '\033[91m'
MYHEADER   = '\033[95m'
MYEND      = '\033[0m'
 
NORMAL = "\033[0m"

if __name__ == '__main__':
    # Display color names in their color
    for name, color in locals().items():
        if name.startswith('__'): continue
        print color, name, MYEND

