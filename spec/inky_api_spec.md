# Inky E-Ink Display API Specification

> **Version:** 2.2.1  
> **Project:** Pimoroni Inky E-Ink Display Driver  
> **Purpose:** Reference specification for developing e-ink display applications

---

## Overview

The Inky library provides a Python interface for controlling Pimoroni e-ink displays. It supports multiple display types with various resolutions and color capabilities, using SPI communication and GPIO control.

### Supported Display Types

| Display Type | Resolution | Colors | Controller |
|-------------|-----------|--------|-----------|
| **InkyPHAT** | 212×104 | Black/White/Red or Yellow | Legacy |
| **InkyPHAT_SSD1608** | 250×122 | Black/White/Red or Yellow | SSD1608 |
| **InkyWHAT** | 400×300 | Black/White/Red or Yellow | Legacy |
| **InkyWHAT_SSD1683** | 400×300 | Black/White/Red or Yellow | SSD1683 |
| **Inky7Colour (UC8159)** | 600×448, 640×400 | 7-color | UC8159 |
| **Inky_Impressions_7** | 800×480 | 7-color | AC073TC1A |
| **InkyEL133UF1** | 1600×1200 | 6-color (Spectra) | EL133UF1 |
| **InkyE673** | 800×480 | 6-color (Spectra) | E673 |
| **InkyE640** | 600×400 | 6-color (Spectra) | E640 |
| **InkyJD79661** | 250×122 | Red/Yellow | JD79661 |
| **InkyJD79668** | 400×300 | Red/Yellow | JD79668 |

---

## Core API

### Auto-Detection

#### `auto(i2c_bus=None, ask_user=False, verbose=False)`

Automatically detect the connected Inky display via EEPROM and return the appropriate driver instance.

**Parameters:**
- `i2c_bus` (optional): SMBus object for I2C communication. If `None`, uses `smbus2.SMBus(1)`
- `ask_user` (bool): If `True`, fall back to command-line arguments when auto-detection fails
- `verbose` (bool): Enable verbose output for debugging

**Returns:** Instance of the appropriate Inky display class

**Example:**
```python
from inky import auto

display = auto(verbose=True)
```

**Raises:**
- `RuntimeError`: If no EEPROM detected and `ask_user=False`

---

### Base Display Class: `Inky`

The base class for all Inky displays. Generally, use specific display classes (InkyPHAT, InkyWHAT, etc.) instead.

#### Constants

```python
WHITE = 0
BLACK = 1
RED = 2
YELLOW = 2
```

#### Constructor

```python
Inky(resolution=(400, 300), colour="black", cs_pin=8, dc_pin=22, 
     reset_pin=27, busy_pin=17, h_flip=False, v_flip=False,
     spi_bus=None, i2c_bus=None, gpio=None)
```

**Parameters:**
- `resolution` (tuple): Display resolution (width, height) in pixels
  - Supported: `(212, 104)`, `(250, 122)`, `(400, 300)`, `(600, 448)`, `(800, 480)`
- `colour` (str): Display color variant - `"red"`, `"black"`, or `"yellow"`
- `cs_pin` (int): Chip-select pin for SPI (default: 8)
- `dc_pin` (int): Data/Command pin (default: 22)
- `reset_pin` (int): Reset pin (default: 27)
- `busy_pin` (int): Busy/Wait pin (default: 17)
- `h_flip` (bool): Enable horizontal flip (default: False)
- `v_flip` (bool): Enable vertical flip (default: False)
- `spi_bus` (optional): Custom SPI bus object
- `i2c_bus` (optional): Custom I2C bus object
- `gpio` (deprecated): Legacy GPIO parameter

**Raises:**
- `ValueError`: If resolution or colour not supported
- `ValueError`: If EEPROM dimensions don't match supplied dimensions

---

### Core Methods

#### `setup()`

Initialize GPIO pins and reset the display. Called automatically before first use.

**Example:**
```python
display.setup()
```

---

#### `set_image(image)`

Copy a PIL Image to the display buffer. Image will be automatically resized to match display resolution.

**Parameters:**
- `image` (PIL.Image): Image to display. Will be converted to palette mode with appropriate colors

**Example:**
```python
from PIL import Image
from inky import InkyWHAT

display = InkyWHAT("red")
image = Image.open("photo.jpg")
display.set_image(image)
display.show()
```

**Notes:**
- Image is automatically resized to display resolution
- Non-palette images are converted using display's color palette
- Supports BLACK, WHITE, and RED/YELLOW colors

---

#### `set_pixel(x, y, v)`

Set a single pixel in the display buffer.

**Parameters:**
- `x` (int): X coordinate (0 to width-1)
- `y` (int): Y coordinate (0 to height-1)
- `v` (int): Color value - `WHITE`, `BLACK`, `RED`, or `YELLOW`

**Example:**
```python
display.set_pixel(100, 50, display.BLACK)
display.set_pixel(101, 50, display.RED)
```

---

#### `show(busy_wait=True)`

Update the physical display with the current buffer contents.

**Parameters:**
- `busy_wait` (bool): If `True`, block until display update completes (default: True)

**Example:**
```python
display.show()  # Blocking update
display.show(busy_wait=False)  # Non-blocking update
```

**Notes:**
- Display update takes several seconds to complete
- Applies `h_flip`, `v_flip`, and rotation transformations
- Uses two buffers: one for black/white, one for red/yellow

---

#### `set_border(colour)`

Set the border color around the display.

**Parameters:**
- `colour` (int): Border color - `WHITE`, `BLACK`, `RED`, or `YELLOW`

**Example:**
```python
display.set_border(display.BLACK)
```

---

### Display-Specific Classes

#### InkyPHAT

Small form-factor display (212×104 pixels).

```python
from inky import InkyPHAT

display = InkyPHAT(colour='red')
```

**Parameters:**
- `colour` (str): `"red"`, `"black"`, or `"yellow"` (default: `"black"`)

**Attributes:**
- `WIDTH = 212`
- `HEIGHT = 104`

---

#### InkyPHAT_SSD1608

Updated pHAT with SSD1608 controller (250×122 pixels).

```python
from inky import InkyPHAT_SSD1608

display = InkyPHAT_SSD1608(colour='yellow')
```

**Parameters:**
- `colour` (str): `"red"`, `"black"`, or `"yellow"`

**Attributes:**
- `WIDTH = 250`
- `HEIGHT = 122`

---

#### InkyWHAT

Larger display (400×300 pixels).

```python
from inky import InkyWHAT

display = InkyWHAT(colour='red')
```

**Parameters:**
- `colour` (str): `"red"`, `"black"`, or `"yellow"` (default: `"black"`)

**Attributes:**
- `WIDTH = 400`
- `HEIGHT = 300`

---

#### Inky7Colour

7-color display with UC8159 controller.

```python
from inky import Inky7Colour

display = Inky7Colour(resolution=(600, 448))
```

**Parameters:**
- `resolution` (tuple): `(600, 448)` or `(640, 400)`

**Supported Colors:**
- Black, White, Green, Blue, Red, Yellow, Orange

---

## EEPROM Module

### EPDType Class

Represents display configuration stored in EEPROM.

#### Constructor

```python
EPDType(width, height, color, pcb_variant, display_variant, write_time=None)
```

**Parameters:**
- `width` (int): Display width in pixels
- `height` (int): Display height in pixels
- `color` (str): Color variant - `"black"`, `"red"`, `"yellow"`, `"7colour"`, `"spectra6"`, `"red/yellow"`
- `pcb_variant` (int): PCB version identifier
- `display_variant` (int): Display type identifier (see DISPLAY_VARIANT list)
- `write_time` (str, optional): Timestamp of EEPROM write

#### Methods

##### `read_eeprom(i2c_bus=None)`

Read EEPROM data from connected display.

**Parameters:**
- `i2c_bus` (optional): SMBus object. If `None`, creates `SMBus(1)`

**Returns:** `EPDType` instance or `None` if no EEPROM detected

**Example:**
```python
from inky import eeprom

epd_data = eeprom.read_eeprom()
if epd_data:
    print(f"Display: {epd_data.width}x{epd_data.height}")
    print(f"Color: {epd_data.get_color()}")
    print(f"Variant: {epd_data.get_variant()}")
```

##### `get_color()`

Get the display color as a string.

**Returns:** Color string or `None`

##### `get_variant()`

Get the display variant name.

**Returns:** Variant name string or `None`

---

## Hardware Interface

### GPIO Pins

Default pin configuration (BCM numbering):

| Pin | Function | Default |
|-----|----------|---------|
| CS | Chip Select | 8 |
| DC | Data/Command | 22 |
| RESET | Reset | 27 |
| BUSY | Busy/Wait | 17 |

### SPI Configuration

- **Bus:** 0
- **Speed:** 488 kHz
- **Mode:** SPI Mode 0
- **Bits:** 8-bit
- **Chip Select:** Software controlled (no_cs=True)

---

## Usage Examples

### Basic Display Update

```python
from inky import auto
from PIL import Image, ImageDraw, ImageFont

# Auto-detect display
display = auto()

# Create image
img = Image.new("P", (display.width, display.height))
draw = ImageDraw.Draw(img)

# Draw content
draw.rectangle((0, 0, display.width, display.height), fill=display.WHITE)
draw.text((10, 10), "Hello, Inky!", fill=display.BLACK)

# Update display
display.set_image(img)
display.set_border(display.WHITE)
display.show()
```

### Manual Display Selection

```python
from inky import InkyWHAT
from PIL import Image

# Create specific display instance
display = InkyWHAT("red")

# Load and display image
image = Image.open("artwork.png")
display.set_image(image)
display.show()
```

### Pixel-by-Pixel Drawing

```python
from inky import InkyPHAT

display = InkyPHAT("black")

# Draw a red diagonal line
for i in range(min(display.WIDTH, display.HEIGHT)):
    display.set_pixel(i, i, display.RED)

display.show()
```

### Non-Blocking Update

```python
from inky import auto
import time

display = auto()

# Set image
display.set_image(my_image)

# Start non-blocking update
display.show(busy_wait=False)

# Do other work while display updates
print("Display updating in background...")

# Wait for completion manually if needed
time.sleep(10)  # Typical update time
```

---

## Mock Displays (Testing)

For development without hardware:

```python
from inky.mock import InkyMockPHAT, InkyMockWHAT

# Create mock display (opens window)
display = InkyMockPHAT("red")
display.set_image(image)
display.show()

# Window stays open until closed
display.wait_for_window_close()
```

**Available Mock Classes:**
- `InkyMockPHAT`
- `InkyMockWHAT`
- `InkyMockPHATSSD1608`
- `InkyMockImpression`

---

## Display Variants Reference

| ID | Variant Name |
|----|--------------|
| 1 | Red pHAT (High-Temp) |
| 2 | Yellow wHAT |
| 3 | Black wHAT |
| 4 | Black pHAT |
| 5 | Yellow pHAT |
| 6 | Red wHAT |
| 7 | Red wHAT (High-Temp) |
| 8 | Red wHAT |
| 10 | Black pHAT (SSD1608) |
| 11 | Red pHAT (SSD1608) |
| 12 | Yellow pHAT (SSD1608) |
| 14 | 7-Colour (UC8159) 600×448 |
| 15 | 7-Colour (UC8159) 640×400 |
| 16 | 7-Colour (UC8159) 640×400 |
| 17 | Black wHAT (SSD1683) |
| 18 | Red wHAT (SSD1683) |
| 19 | Yellow wHAT (SSD1683) |
| 20 | 7-Colour 800×480 (AC073TC1A) |
| 21 | Spectra 6 13.3" 1600×1200 (EL133UF1) |
| 22 | Spectra 6 7.3" 800×480 (E673) |
| 23 | Red/Yellow pHAT (JD79661) |
| 24 | Red/Yellow wHAT (JD79668) |
| 25 | Spectra 6 4.0" 600×400 (E640) |

---

## Technical Notes

### Display Update Process

1. **Setup Phase:** Initialize GPIO and SPI
2. **Buffer Preparation:** Convert image to two binary buffers (black/white + color)
3. **SPI Transfer:** Send buffers to display controller
4. **Physical Update:** E-ink particles move (takes 5-15 seconds)
5. **Busy Wait:** Monitor BUSY pin until complete

### Color Palette

Images are converted to a 3-color palette:
- **Index 0:** White (255, 255, 255)
- **Index 1:** Black (0, 0, 0)
- **Index 2:** Red/Yellow (varies by display)
  - Red: (255, 0, 0)
  - Yellow: (255, 255, 0)

### Performance Considerations

- Display updates are **slow** (5-15 seconds)
- Use `busy_wait=False` for non-blocking updates
- Minimize update frequency to extend display lifespan
- E-ink displays have **ghosting** - use full refresh cycles periodically

### Power Consumption

- E-ink displays only consume power during updates
- Image persists without power
- Ideal for battery-powered applications

---

## Dependencies

```python
# Required
numpy
Pillow (PIL)
gpiod
spidev
smbus2  # For EEPROM reading

# Optional
gpiodevice  # For GPIO abstraction
```

---

## Error Handling

### Common Exceptions

```python
# Invalid resolution
ValueError: Resolution 123x456 not supported!

# Invalid color
ValueError: Colour purple is not supported!

# EEPROM mismatch
ValueError: Supplied width/height do not match Inky: 400x300

# No EEPROM detected
RuntimeError: No EEPROM detected! You must manually initialise your Inky board.

# Missing dependencies
ImportError: This library requires the smbus2 module
```

---

## Best Practices

1. **Use Auto-Detection:** Prefer `auto()` for production code
2. **Handle Errors:** Wrap display operations in try-except blocks
3. **Optimize Images:** Pre-process images to display resolution
4. **Limit Updates:** Minimize refresh cycles to extend display life
5. **Test with Mocks:** Use mock displays during development
6. **Border Management:** Set borders to match your design aesthetic
7. **Busy Wait:** Use blocking updates unless you have concurrent work

---

## Migration Guide

### From Legacy to SSD1608

```python
# Old
from inky import InkyPHAT
display = InkyPHAT("red")

# New (if you have SSD1608 hardware)
from inky import InkyPHAT_SSD1608
display = InkyPHAT_SSD1608("red")

# Best (auto-detect)
from inky import auto
display = auto()
```

---

## Additional Resources

- **GitHub:** https://github.com/pimoroni/inky
- **Shop:** https://shop.pimoroni.com/products/inky-phat
- **Tutorial:** https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat
- **Pinout:** https://pinout.xyz/pinout/inky_phat

---

## License

This specification documents the Pimoroni Inky library (v2.2.1).  
Refer to the original project for licensing information.
