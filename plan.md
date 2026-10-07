# Halloween Costume

## Goal

- Two adults attend a costume party where we will walk around, eat food, play board and card games.
- Our costumes are funny and entertaining. We have a geeky sense of humor as do others at the party.
- We would like to dress as travellers from the future who have integrated with computers.
- We might include a joke that we are Skynet tech support.
- I am a software engineer wth experience in Javascript and Linux.
- My partner is interested in AI projects
- We want to learn about programming embedded devices.

## Requirements

- We have colorful programmable banks of LED lights. Some ideas for locations are a headband, jewlery, badges, and patches that we attach to our clothing.
- I have long hair, anything to light up the hair could be fun.
- We can control the lights with hand gestures.

## Budget

- Prefer $500 but can be $1000 for an amazing project that we can reuse.

### BOM

| Item                                             |              Qty | Recommended Part                                                           | DigiKey Part Number                               | Notes                                                                                                                                                |
| ------------------------------------------------ | ---------------: | -------------------------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Main controller (one per wearer)                 |                2 | Adafruit Circuit Playground Bluefruit (MPN 4333)                           | 1528-4333-ND (use MPN 4333 if SKU format differs) | Best beginner fit: built-in accelerometer, buttons, BLE, and strong CircuitPython docs.                                                              |
| Addressable LED strip for chest modules          |        2 m total | Adafruit NeoPixel RGBW strip 60 LED/m, 1 m length (MPN 4689)               | 1528-4689-ND                                      | Start with 1 m per person, cut to fit chest patch geometry. RGBW gives cleaner white channel but needs RGBW pixel config in code.                    |
| Spare LED strip                                  |              1 m | Same as above                                                              | 1528-4689-ND                                      | Spare for repairs and backup testing.                                                                                                                |
| Short alligator lead set (bring-up/testing)      | 1 set (12 leads) | Adafruit short wire alligator clips (MPN 1592)                             | 1528-1592AD-ND                                    | Speeds up bench testing before sewing/soldering final wiring. One pack is enough to start; add a second pack only if you want parallel bench setups. |
| Battery holder option (AAA fallback bench power) |                2 | Adafruit 3xAAA holder with switch + JST (MPN 727)                          | 1528-727-ND                                       | Optional fallback power for quick tests; USB power bank remains primary runtime path.                                                                |
| USB power bank                                   |                2 | 10000 mAh class bank (Anker/Belkin/etc.)                                   | N/A (consumer item)                               | Choose reputable brand with stable 5V output.                                                                                                        |
| USB cables (data + power)                        |                4 | USB A to micro-B (or board-compatible cable)                               | Varies                                            | Include at least 2 short and 2 routed cables for wearable setup.                                                                                     |
| Momentary buttons for dev test mode              |              4-6 | Through-hole tactile push buttons, normally open                           | Varies                                            | Development-only hard-button state forcing while tuning gesture logic.                                                                               |
| JST pigtails/connectors                          |            1 kit | JST-PH 2-pin pigtail/connector kit                                         | Varies                                            | For clean serviceable power connections.                                                                                                             |
| Wire                                             |          1 spool | Silicone stranded hook-up wire (22-26 AWG mix)                             | Varies                                            | Flexible wire is more wearable-friendly and strain resistant.                                                                                        |
| Heat-shrink tubing                               |            1 kit | Mixed ratio tubing kit                                                     | Varies                                            | Insulation and strain relief.                                                                                                                        |
| Inline switch + fuse holder                      |           2 each | Inline SPST switch + low-current inline fuse holder                        | Varies                                            | Recommended for safer wearable power distribution.                                                                                                   |
| Diffuser material                                |            1 set | Frosted TPU/fabric diffuser sheets                                         | N/A                                               | Needed so high-visibility states are readable without glare.                                                                                         |
| Mounting supplies                                |            1 set | Industrial Velcro, fabric tape, strain-relief clips, cable sleeves         | N/A                                               | Keep modules removable for repair and software iteration.                                                                                            |
| Build tools (if needed)                          |            1 set | Soldering iron, lead-free solder, flux pen, stripper, multimeter, heat gun | Varies                                            | Required for reliable assembly and troubleshooting.                                                                                                  |

#### Ordering Notes (DigiKey)

- Use Adafruit MPN search first (for example: `4333`, `4689`, `1592`, `727`) if a direct SKU does not resolve.
- DigiKey listings can vary by region/packaging; confirm exact listing title before checkout.
- For timeline safety, buy one spare controller and spare LED strip in the first order.
- Prioritize documentation-friendly parts over lowest cost so software learning stays smooth.

#### BOM Addendum: Concrete Options For "Varies" Items

| Item                              |          Qty | Concrete Option (MPN)                                 | DigiKey Search Key            | Why This Choice                                                                    |
| --------------------------------- | -----------: | ----------------------------------------------------- | ----------------------------- | ---------------------------------------------------------------------------------- |
| Momentary buttons (dev test mode) |            6 | E-Switch TL1105SPF160Q                                | `TL1105SPF160Q`               | Standard 6x6 mm tactile button, easy breadboard/proto use for state forcing tests. |
| JST-PH 2-pin board headers        |           10 | JST B2B-PH-K-S (LF)(SN)                               | `B2B-PH-K-S(LF)(SN)`          | Common JST-PH header for clean low-current power connectors.                       |
| JST-PH 2-pin housings             |           20 | JST PHR-2                                             | `PHR-2`                       | Matching 2-position housing for battery/power harnesses.                           |
| JST-PH crimp terminals            |           50 | JST SPH-002T-P0.5S                                    | `SPH-002T-P0.5S`              | Matching terminals for a serviceable custom harness.                               |
| Hook-up wire (power/data)         | 1 spool each | Alpha Wire 3051 (22 AWG) and Alpha Wire 3050 (24 AWG) | `Alpha 3051` and `Alpha 3050` | Durable PVC hook-up wire with common gauges for wearable routing.                  |
| Heat-shrink tubing kit            |        1 kit | 3M FP-301 assortment                                  | `3M FP-301 assortment`        | Reliable general-purpose tubing for insulation and strain relief.                  |
| Inline fuse holder (low voltage)  |            2 | Littelfuse 0FHM0001ZXJ                                | `0FHM0001ZXJ`                 | Compact inline holder for basic short-circuit protection on power path.            |
| Fast-acting fuse assortment       |       1 pack | Littelfuse 0251 series (for 5V low-current projects)  | `Littelfuse 0251`             | Easy to source and suitable for low-current protection tuning.                     |
| Inline SPST power switch          |            2 | C&K OS102011MA1QN1                                    | `OS102011MA1QN1`              | Simple durable on/off slide switch for wearable master power control.              |
| USB data/power cable              |            4 | Tripp Lite U050 series micro-USB cable                | `U050 micro usb`              | Reputable cable line; use short lengths for less cable drag.                       |
| Cable sleeve                      |       1 pack | Techflex Flexo PET sleeving                           | `Techflex Flexo PET`          | Clean wearable cable bundling with abrasion resistance.                            |

Notes:

- For these parts, DigiKey stock may change by package size or equivalent vendor, so use the MPN search key first and then choose in-stock equivalents.
- Keep one consistent connector family (JST-PH 2-pin) across both costumes to reduce wiring mistakes.

#### Power Notes

- AAA packs are not required for v1. Keep them only as optional fallback bench power.
- USB power banks are the recommended primary power source for party use.
- Controller input voltage tolerance is fairly flexible, but the RGBW LED strip expects a 5V-style supply for reliable behavior.
- Treat the full system as a 5V design: common ground, short power runs, and brightness/current limiting in software.
- Prefer power banks with low-current/always-on mode so they do not auto-shut off during low-brightness animations.

#### Diffuser Ideas

thermoplastic - mouldable
crinoline tubes like https://www.amazon.com/YYCRAFT-Wreaths-Cyberlox-Crafts-8-Inch/dp/B075D5VJGK/ref=sr_1_1?crid=2P0O4F0E3TFJC&dib=eyJ2IjoiMSJ9.d3coBXvidpGzpheRP2wD5ckAQ_iI-iwCntCBAjzTVzBA4M4z_UHgudX9Ff8wkBKkYnvjt4BVDlkFaWZf3IIR-Y4y5gN0XwYmPBZ5VimySaAIjxUq1h6yEWzlGTBH8APz12oJh3OZpJeCWf66s2QJPEa2zPEELjjgMY8h9dj82izqr4FPwiOj8bWT25g_TWMt3zu6Z1QAC1bm_2h1kuTtM_KVlb23wOwIbW96zXJExzyDyL1HxgahRFXFUsY2t64FdYoPG41WipeFxugtczZQ3nBouzH5Bi-ChS28WK2Cgz8.s2zrsFMwSaBEK_uV-1r4aymG59lPubDTHqZPnjVj6Pk&dib_tag=se&keywords=crinoline%2Btubing&qid=1789338525&sprefix=crinoline%2Btubing%2Caps%2C184&sr=8-1&th=1 is awesome for a wig or pipes if we can find a led strip narrow enough. Inside diameter is 8mm.

#### Learn Bluefruit and write hello world

1. Power and data communications with unit
2. Blink the LED on the board?
3. Get data from accelorometer and any other available motion data
4. Learn how to push program to board

Notes:

To make Bluefruit connect to mac, double click the center reset button.
CPLAYBOOT shows up in Finder.

If CPLAYBTBOOT appears: the USB mass-storage hardware path works, and CircuitPython itself just isn't presenting CIRCUITPY — likely needs CircuitPython (re)installed. Download the latest .uf2 for the Circuit Playground Bluefruit from circuitpython.org and drag it onto CPLAYBTBOOT; the board will reboot and CIRCUITPY should then mount normally.

https://circuitpython.org/board/circuitplayground_bluefruit/
https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/circuitpython

## Gesture-to-Light Firmware Plan

Reads the LIS3DH accelerometer (incl. hardware tap engine) to classify tap, double tap, fist bump, and
jazz hands, then drives the 10-pixel NeoPixel ring with a matching non-blocking light response. Pure
gesture/response logic is kept free of hardware imports so it's pytest-testable on the Mac.

**Decisions**

- Non-blocking main loop; sensing continues while a response animates.
- Tap/double tap via LIS3DH's hardware click engine (may need raw `CLICK_SRC` register bits to tell them apart).
- Fist bump (magnitude spike-then-stop, any direction) and jazz hands (axis oscillation/zero-crossing) are custom, hardware-import-free detectors.
- Gesture priority order + cooldown window resolves overlapping matches.
- BLE/cross-board comms out of scope for this phase.
- Debug mode toggled by **Button A** (not double tap, to avoid overloading it): solid-lights the onboard red LED and prints raw accel + gesture events to serial.
- Colors: tap = white single flash; double tap = cyan double flash; jazz hands = rainbow chase; fist bump = orange arc / red opposite arc, 3x blink.

**Structure** (new `firmware/costume/`, separate from `firmware/blink/`)

- `hardware/` — only layer touching `board`/`neopixel`/`adafruit_lis3dh` (board_io.py, config.py)
- `gestures/` — pure-logic detectors (tap.py, fist_bump.py, jazz_hands.py) + manager.py (priority/cooldown)
- `responses/` — non-blocking tick-based animations + manager.py
- `debug.py`, `main.py`, `code.py` — wiring and entry point
- `tests/` — desktop pytest suite with synthetic accel waveforms, not copied to the board

**Phases**: A) hardware layer → B) gesture detection (parallel w/ A) → C) light responses (parallel w/ A/B) → D) integration (needs A+B+C) → E) desktop pytest suite (needs B) → F) on-board tuning (needs D).

**Risks**: jazz hands may be physically weak to detect if the rotation axis is near-vertical (gravity-aligned); tap vs double-tap may need raw register reads; "opposite quarters" pixel groups are placeholders until confirmed against the physical ring.
