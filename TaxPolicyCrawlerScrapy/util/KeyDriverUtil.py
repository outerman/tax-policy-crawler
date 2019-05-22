import pywinio
import time
import atexit

# KeyBoard Commands
# Command port
KBC_KEY_CMD = 0x64
# Data port
KBC_KEY_DATA = 0x60

g_winio = None


def get_winio():
    global g_winio

    if g_winio is None:
            g_winio = pywinio.WinIO()
            def __clear_winio():
                    global g_winio
                    g_winio = None
            atexit.register(__clear_winio)

    return g_winio


def wait_for_buffer_empty():
    """
    Wait keyboard buffer empty
    """

    winio = get_winio()

    dwRegVal = 0x02
    while (dwRegVal & 0x02):
            dwRegVal = winio.get_port_byte(KBC_KEY_CMD)


def key_down(scancode):
    winio = get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode)


def key_up(scancode):
    winio = get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode | 0x80)


def key_press(scancode, press_time=0.2):
    key_down(scancode)
    time.sleep(press_time)
    key_up(scancode)


def key_press_str(str_input):
    for char in str_input:
        key_press(get_scan_code(char))


def get_scan_code(char):
    return KEY_MAP[char]


KEY_MAP = {
    'ESC': 0x01,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0a,
    '0': 0x0b,
    '-': 0x0c,
    '=': 0x0d,
    # 0e (Backspace)
    'Tab': 0x0f,
    'q': 0x10,
    'w': 0x11,
    'e': 0x12,
    'r': 0x13,
    't': 0x14,
    'y': 0x15,
    'u': 0x16,
    'i': 0x17,
    'o': 0x18,
    'p': 0x19,
    '[': 0x1a,
    ']': 0x1b,
    'Enter': 0x1c,
     # 1d (LCtrl)
     'a': 0x1e,
    's': 0x1f,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    ';': 0x27,
    '\'': 0x28,
    '`': 0x29,
    # 2a (LShift)
    '\\': 0x2b,     # (\|), on a 102-key keyboard
    'z': 0x2c,
    'x': 0x2d,
    'c': 0x2e,
    'v': 0x2f,
    'b': 0x30,
    'n': 0x31,
    'm': 0x32,
    ',': 0x33,
    '.': 0x34,
    '/': 0x35}
    # 36 (RShift)
    # 37 (Keypad-*) or (*/PrtScn) on a 83/84-key keyboard
    # 38 (LAlt), 39 (Space bar),
    # 3a (CapsLock)
    # 3b (F1), 3c (F2), 3d (F3), 3e (F4), 3f (F5), 40 (F6), 41 (F7), 42 (F8), 43 (F9), 44 (F10)
