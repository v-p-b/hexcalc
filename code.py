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
    12:  "4", 13:  "5", 14:  "6", 15:  "*",
    16:  "1", 17:  "2", 18:  "3", 19:  "=" 
}

while True:
    key_event = keys.events.get()
    if key_event and key_event.pressed:
        print(keymap[key_event.key_number])
        
