# you could use pyautogui too https://automatetheboringstuff.com/chapter18/
# @author http://stackoverflow.com/a/13615802/2692914 lmiguelmh
# @since 
import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

# https://msdn.microsoft.com/en-us/library/dd375731
VK_TAB = 0x09
VK_CONTROL = 0x11
VK_MENU = 0x12  # alt
VK_RETURN = 0x0D
VK_ESCAPE = 0x1B
VK_A = 0x41
VK_E = 0x45
VK_F = 0x46
VK_S = 0x53

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT,  # nInputs
                             LPINPUT,  # pInputs
                             ctypes.c_int)  # cbSize


# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def Key(key, sleep=0.2):
    """
    it seems that some browsers (chrome) require a sleep time between keys!
    :param key:
    :param sleep:
    :return:
    """
    PressKey(key)
    time.sleep(sleep)
    ReleaseKey(key)


def Alt(key, sleep=0.2):
    """
    it seems that some browsers (chrome) require a sleep time between keys!
    :param key:
    :param sleep:
    :return:
    """
    PressKey(VK_MENU)
    time.sleep(sleep)
    PressKey(key)
    time.sleep(sleep)
    ReleaseKey(key)
    time.sleep(sleep)
    ReleaseKey(VK_MENU)


def Ctrl(key, sleep=0.2):
    """
    it seems that some browsers (chrome) require a sleep time between keys!
    :param key:
    :param sleep:
    :return:
    """
    PressKey(VK_CONTROL)
    time.sleep(sleep)
    PressKey(key)
    time.sleep(sleep)
    ReleaseKey(key)
    time.sleep(sleep)
    ReleaseKey(VK_CONTROL)

# if __name__ == "__main__":
#     # AltTab()
#     Ctrl(VK_A)
