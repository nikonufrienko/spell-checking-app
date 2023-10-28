import pyautogui as pya
from pynput import keyboard
import pyperclip
import time


def dummy_print(text):
    print(text)


def copy_clipboard():
    # time.sleep(.1)
    # pya.hotkey('ctrl', 'c')
    # time.sleep(.1)
    return pyperclip.paste()


text_process_handler = dummy_print


def capture_hotkey_handler():
    copy_text = copy_clipboard()
    text_process_handler(copy_text)


def start_capture_daemon(hotkey='<alt>+y', handler=dummy_print):
    global text_process_handler
    text_process_handler = handler
    with keyboard.GlobalHotKeys({
            hotkey: capture_hotkey_handler}) as h:
        h.join()


def get_cursor_pos():
    return pya.position()
