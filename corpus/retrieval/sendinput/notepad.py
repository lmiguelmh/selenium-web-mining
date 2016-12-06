# @author lmiguelmh
# @since 
import win32gui
import win32con
import win32api

# http://stackoverflow.com/questions/12996985/send-some-keys-to-inactive-window-with-python
hwndMain = win32gui.FindWindow("notepad", "Sin título: Bloc de notas")
# hwndEdit = win32gui.FindWindowEx(hwndMain, 0, "Edición", 0)
# hwndEdit = win32gui.FindWindowEx(hwndMain, 0, "Edición", "Edición")
# win32api.PostMessage(hwndEdit, win32con.WM_CHAR, ord('t'), 0)
win32gui.SetForegroundWindow(hwndMain)
hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
# win32gui.SetForegroundWindow(hwndChild)

win32api.PostMessage(hwndChild, win32con.WM_CHAR, ord('t'), 0)

# is not possible to send ctrl
# win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
# win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, ord('e'), 0)
# win32api.PostMessage(hwndChild, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)
# win32api.PostMessage(hwndChild, win32con.WM_KEYUP, ord('e'), 0)

# win32api.PostMessage(hwndChild, 0x0112, 0xF100, 0x0046)
# win32api.PostMessage(hwndChild, 0x0102, ord('a'), 0)
# win32api.PostMessage(hwndMain, 0x0112, 0xF100, 0x0046)

# http://stackoverflow.com/questions/5144877/sending-ctrl-s-message-to-a-window
# send ALT + A
win32api.PostMessage(hwndMain, 0x0112, 0xF100, ord('a'))
# send G
win32api.PostMessage(hwndMain, 0x0102, ord('g'), 0)

# win32api.PostMessage(hwndChild, 0x0111, 3, 0)
# win32api.PostMessage(hwndMain, 0x0111, 3, 0)

# win32api.PostMessage(hwndChild, 0x0102, 0x0053, 0)

# Sending ALT + VK_NUMPAD1 (alt+1) after 3 hours of searching!
# https://social.msdn.microsoft.com/Forums/vstudio/en-US/5f77339e-502f-48eb-afb3-12aaacfb28ab/simulating-alt2-keypad-combination?forum=vclanguage
win32api.keybd_event(win32con.VK_LMENU, win32api.MapVirtualKey(win32con.VK_LMENU, 0), 0, 0)
win32api.keybd_event(win32con.VK_NUMPAD2, win32api.MapVirtualKey(win32con.VK_NUMPAD2, 0), 0, 0)
win32api.keybd_event(win32con.VK_NUMPAD2, win32api.MapVirtualKey(win32con.VK_NUMPAD2, 0), win32con.KEYEVENTF_KEYUP, 0)
win32api.keybd_event(win32con.VK_LMENU, win32api.MapVirtualKey(win32con.VK_LMENU, 0), win32con.KEYEVENTF_KEYUP, 0)

