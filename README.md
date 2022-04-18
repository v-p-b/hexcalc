Calculator with Hexadecimal Numpad
==================================

[HP-16C](https://en.wikipedia.org/wiki/HP-16C) for hackers, who don't mind wasting CPU cycles and RAM for comfort.

![hexcalc front](/p0rn/1.jpg)

Parts
-----

* [NeoKey 5x6 Ortho Snap-Apart Mechanical Key Switches](https://www.adafruit.com/product/5157) - Finally a PCB with enough (but not too many) buttons!
* [Black Adafruit Feather RP2040](https://www.adafruit.com/product/4884) - Less powerful boards will probably do the basic functionality but I wanted to make sure my OLED is nice
* [Adafruit 128x64 OLED FeatherWing](https://learn.adafruit.com/adafruit-128x64-oled-featherwing)
* 20x MX compatible keyswitches and caps
* Screws: M2.5 for the FeatherWing, M3 for the keypad
* Incremental encoder with push button
* Male and female pin headers to connect the Feather with the display. Careful when following tutorials advising the use of breadboards for soldering: my breadboard didn't exactly match the distance of pin lines, making the headers tilt!

Inspired by
-----------

* [Adafruit Macropad RP2040](https://learn.adafruit.com/adafruit-macropad-rp2040) - It took me a long time to realize, that these kinds of things are called "macropads" - a keyword that made googling for parts much easier!
* [Numpad 4000](https://learn.adafruit.com/numpad-4000-mechanical-keyswitch-data-entry-device/overview) - A great project, but decimal is [BORING](https://www.youtube.com/watch?v=qf-hpusjxfw)!

Wiring
------

The RP2040 Feather has 21 GPIO pins, I use 16:
- 9 for the keyboard (4x5)
- 2 for the display I2C
- 3 for the display buttons, 1 is in active use for the encoder switch
- 2 for the encoder

![hexcalc back](/p0rn/2.jpg)

The box
-------

I cut out the base from 2mm plexi sheets (polystyrol, sold as "hobbyglas" - a perfect name for a product, that is not actually made of glass...), because they were the only fitting plastic material I could find available. It's transparent, which I think is pretty cool for this project.

Cutting the sheets is relatively easy [using a razor tool, then snapping it](https://www.youtube.com/watch?v=Axo_bTyl1gQ). 

The surface is really slippery, so be careful when measuring!

For drilling I used a 3mm masonry drill head in an electric screwdriver set on a relatively slow speed. This way I could avoid cracks, but had to pause multiple times to let the plastic resolidify and clean the head. I fixed multiple imprefect drills with a 4mm head.

Keys
----

I used an acrylic pen to draw signs on black plastic.

Software
--------

The basic idea is to have a reprogrammable numpad, and feed any input to Python's eval() to get results. This way basic and boolean arithmethic in multiple number systems are available out of the box.

### Number format

- `[0-9A-F]+` - Hexadecimal (default)
- `0D[0-9]+` - Decimal
- `0B[01]+` - Binary
- `0C[0-7]` - Octal (sry, we don't have an 'o') 

### Modes

These can be set using the encoder.

- FORTUNE: This is the basic mode. Can add and subtract.
- MULTI: `+` -> `*` and `-` -> `/` (division untested, pbbly will break things)
- AND: `+` -> `&` and `-` -> `|` 
- XOR: Both `+` and `-` become `^`
- DEC: Convert the currently displayed number to decimal (according to notation)
- TWOS: Two's complement, because signed bytes in Java suck. This takes the currently displayed number as _8-bit_decimal_ and displays two's complement in _hexadecimal_!

### Challenge

I'm willing to offer a bottle of fine booze to anyone (original idea required) who demonstrates arbitrary Python code execution using the implemented functionality and the 20 available buttons!

Planned developments
--------------------

* A proper box

