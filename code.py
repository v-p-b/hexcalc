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
    0:   "D", 1:   "E", 2:   "F", 3:   "0",
    4:   "A", 5:   "B", 6:   "C", 7:   "+",
    8:   "7", 9:   "8", 10:  "9", 11:  "-",
    12:  "4", 13:  "5", 14:  "6", 15:  "<",
    16:  "1", 17:  "2", 18:  "3", 19:  "=" 
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
        
