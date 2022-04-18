import board
import keypad
import digitalio
import displayio
import terminalio
import adafruit_displayio_sh1107
import random
import rotaryio
from adafruit_display_text import label

FEATURES = [
    ("FORTUNE", "Fortune"),
    ("TWOS", "Two's complement"),
    ("MULTI",  "*  /  <  ="),
    ("AND",  "&  |  <  ="),
    ("XOR",  "^  ^  <  ="),
    ("DEC","2Decimal")
]

def fortune():
    with open("fortune.txt","r") as fortune:
        lines=fortune.read().splitlines()
        return random.choice(lines)

def menu_text(text):
    if len(text)>20:
        return text[0:20]
    else:
        return text+(" "*(20-len(text)))

def py2native(input):
    return input.replace("0x","").upper()

def native2py(input):
    negative=False
    absval=input
    if input[0] == "-":
        negative = True
        input = input[1:]
    if input.lower().startswith("0b"):
        absval = input.lower()
    elif input.lower().startswith("0c"):
        absval = "0o"+input[2:]
    elif input.lower().startswith("0d"):
        absval = input[2:]
    else:
        absval = "0x"+input

    if negative:
        return "-"+absval
    else:
        return absval

# From Stack Overflow: https://stackoverflow.com/a/9147327
def twos_comp(val, bits=8):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

# I fucked up the soldering
# the key matrix shoudl look like this:
"""
keys = keypad.KeyMatrix(
    row_pins=(board.D4, board.A3, board.A2, board.A1, board.A0),
    column_pins=(board.D13, board.D12, board.D11, board.D10),
    columns_to_anodes=False,
)
"""

# On my device it looks like this:
keys = keypad.KeyMatrix(
    row_pins=(board.A0, board.D4, board.A3, board.A1, board.A2),
    column_pins=(board.D13, board.D12, board.D10, board.D11),
    columns_to_anodes=False,
)

keymap = {
    0:   "+", 1:   "-", 2:   "<", 3:   "=",
    4:   "C", 5:   "D", 6:   "E", 7:   "F",
    8:   "8", 9:   "9", 10:  "A", 11:  "B",
    12:  "4", 13:  "5", 14:  "6", 15:  "7",
    16:  "0", 17:  "1", 18:  "2", 19:  "3" 
}

# ENCODER

encoder = rotaryio.IncrementalEncoder(board.MOSI, board.SCK)
encoder_button = digitalio.DigitalInOut(board.D5)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP

# SCREEN INIT

displayio.release_displays()
# oled_reset = board.D9

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
BORDER = 2

display = adafruit_displayio_sh1107.SH1107(
    display_bus, width=WIDTH, height=HEIGHT, rotation=0
)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

text1 = menu_text(fortune())
text_area = label.Label(terminalio.FONT, text=text1, color=0x000000, background_color=0xFFFFFF, x=8, y=8)
splash.append(text_area)

history_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF,x=8, y=26)
splash.append(history_area)

text2 = "HEXCALC"
calc_area = label.Label(
    terminalio.FONT, text=text2, scale=2, color=0xFFFFFF, x=9, y=44
)
splash.append(calc_area)

# This is the main input area on the screen
display_buf=""
# This holds the expression to eval()
calc_buf=""
# This holds the digits of the last typed number
num_buf=""
last_position = encoder.position
encoder_button_state = False
curr_feature = 0
active_feature = FEATURES[curr_feature][0]

while True:
    key_event = keys.events.get()
    position = encoder.position
    position_change = position - last_position
    if position_change != 0:
        curr_feature = (curr_feature + position_change) % len(FEATURES)
        text_area.text=menu_text(FEATURES[curr_feature][1])
    last_position = position

    if not encoder_button.value and not encoder_button_state:
        encoder_button_state = True

    if encoder_button.value and encoder_button_state:
        encoder_button_state=False
        active_feature = FEATURES[curr_feature][0]

    if active_feature == "FORTUNE":
        active_feature = None # Infinite loop...
        text_area.text = menu_text(fortune())

    if active_feature == "TWOS":
        active_feature = None
        twos=py2native(hex(twos_comp(int(num_buf))))
        num_buf=twos
        display_buf=twos
        calc_buf=""
        calc_area.text=twos
        continue

    if active_feature == "DEC":
        active_feature = None
        history_area.text = str(int(native2py(display_buf)))

    if key_event and key_event.pressed:
        key = keymap[key_event.key_number]
        if key in ["+", "-", "<", "="]:
            if key == "=":
                calc_buf += native2py(num_buf)
                print("Calculating: %s" % (calc_buf))
                display_buf = py2native(hex(eval(calc_buf)))
                history_area.text=calc_buf
                num_buf = ""
                calc_buf = native2py(display_buf)
            elif key == "<":
                num_buf=""
                calc_buf=""
                display_buf=""
            if key == "-" or key == "+":
                if key == "-":
                    if active_feature == "MULTI":
                        key = "/"
                    if active_feature == "AND":
                        key = "|"
                    if active_feature == "XOR":
                        key = "^"
                if key == "+":
                    if active_feature == "MULTI":
                        key = "*"
                    if active_feature == "AND":
                        key = "&"
                    if active_feature == "XOR":
                        key = "^"

                if len(num_buf)>0:
                    calc_buf += native2py(num_buf)
                    num_buf=""
                calc_buf += key
                display_buf += key
        else:
            display_buf += keymap[key_event.key_number]
            num_buf += keymap[key_event.key_number]
        print("disp: ",display_buf)
        calc_area.text=display_buf[-10:]
        print("num: ",num_buf)
        print("calc: ", calc_buf)
        print("--") 
