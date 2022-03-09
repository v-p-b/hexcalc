import board
import keypad

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

def py2native(input):
    return input.replace("0x","").upper()

def native2py(input):
    # TODO handle decimal, binary, octal representations
    return "0x"+input

display_buf=""
calc_buf=""
num_buf=""
while True:
    key_event = keys.events.get()
    if key_event and key_event.pressed:
        key = keymap[key_event.key_number]
        if key in ["+", "-", "<", "="]:
            calc_buf += native2py(num_buf)
            if key == "=":
                print("Calculating: %s" % (calc_buf))
                display_buf = py2native(hex(eval(calc_buf)))
                calc_buf=""
                num_buf = display_buf
            elif key == "<":
                num_buf=""
                calc_buf=""
                display_buf=""
            else:
                calc_buf += key
                num_buf = ""
                display_buf += key
        else:
            display_buf += keymap[key_event.key_number]
            num_buf += keymap[key_event.key_number]
        print(display_buf)
        #print(num_buf)
        #print(calc_buf)
        
