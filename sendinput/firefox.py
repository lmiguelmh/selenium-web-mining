# @author lmiguelmh
# @since

import win32gui
import win32con
import win32api
import sendinput

# http://stackoverflow.com/questions/12996985/send-some-keys-to-inactive-window-with-python
# hwndMain = win32gui.FindWindow("MozillaWindowClass", "Google - Mozilla Firefox")
hwndMain = win32gui.FindWindow("Chrome_WidgetWin_1", "Google - Google Chrome")
win32gui.SetForegroundWindow(hwndMain)
hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
# win32api.PostMessage(hwndChild, win32con.WM_CHAR, ord('t'), 0)
# http://stackoverflow.com/questions/5144877/sending-ctrl-s-message-to-a-window
# send ALT + F
# win32api.PostMessage(hwndMain, 0x0112, 0xF100, ord('F'))
# send G
# win32api.PostMessage(hwndMain, 0x0102, ord('P'), 0)
# win32api.PostMessage(hwndChild, 0x0102, ord('P'), 0)
sendinput.Ctrl(sendinput.VK_S, sleep=0.2)
# sendinput.Alt(sendinput.VK_F)
