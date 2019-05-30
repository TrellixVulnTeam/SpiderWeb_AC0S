import socket
from lexer import Lexer
from pygments import highlight
from pygments.lexers import *
from pygments.formatters.terminal import TerminalFormatter
import sys

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# class for handling platform
class Host_OS(object):
    def is_windows(self):
        return sys.platform == 'win32' or sys.platform == 'cygwin'

    def is_linux(self):
        return 'linux' in sys.platform

    def is_mac(self):
        return sys.platform == 'darwin'

# handles regex output with custom lexer
class Regex:
    @staticmethod
    def highlight_line(content):
        return highlight(content, Lexer(ensurenl=False), TerminalFormatter())

    @staticmethod
    def output_highlight(*a_list):
        for each in a_list:
            print(Regex.highlight_line(each) + '\n')
