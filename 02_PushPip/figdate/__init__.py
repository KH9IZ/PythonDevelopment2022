import time
import pyfiglet

def date(format="%Y %d %b, %A", font="graceful"):
    formated_str = time.strftime(format)
    return pyfiglet.figlet_format(text=formated_str, font=font)

