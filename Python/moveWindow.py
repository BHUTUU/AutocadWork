import win32gui
import win32con
import win32api

def move_window(window_title, x, y, width, height):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print(f"Window '{window_title}' not found.")
        return False
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.MoveWindow(hwnd, x, y, width, height, True)
    print(f"Moved '{window_title}' to ({x}, {y}) with size {width}x{height}.")
    return True

if __name__ == "__main__":
    move_window("Google Earth Pro", 100, 100, 800, 600)