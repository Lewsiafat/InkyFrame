# Inky Impression 7.3" Hardware Specification

**Product Name:** Inky Impression 7.3" (Spectra 6 Edition)  
**Model:** E673  
**Manufacturer:** Pimoroni  
**Display Technology:** E Ink Spectra 6®

---

## Display Specifications

### Physical Characteristics

| Parameter | Value |
|-----------|-------|
| **Screen Size** | 7.3 inches (diagonal) |
| **Resolution** | 800 × 480 pixels |
| **Active Area** | ~162mm × 97mm |
| **Pixel Pitch** | ~0.202mm |
| **Aspect Ratio** | 5:3 (1.67:1) |
| **Viewing Angle** | Ultra-wide (nearly 180°) |
| **Display Type** | Reflective E Ink (electrophoretic) |

### Board Dimensions

| Parameter | Value |
|-----------|-------|
| **PCB Size** | 174mm × 123mm |
| **Mounting Holes** | M2 at corners |
| **Recommended Frame** | 180mm × 130mm (IKEA compatible) |

---

## Color Capabilities

### Spectra 6 Technology

The display supports **6 colors** using E Ink Spectra 6® technology:

| Color Index | Color Name | RGB Value (Desaturated) | RGB Value (Saturated) |
|-------------|------------|-------------------------|------------------------|
| 0 | Black | (0, 0, 0) | (0, 0, 0) |
| 1 | White | (255, 255, 255) | (161, 164, 165) |
| 2 | Yellow | (255, 255, 0) | (208, 190, 71) |
| 3 | Red | (255, 0, 0) | (156, 72, 75) |
| 5 | Blue | (0, 0, 255) | (61, 59, 94) |
| 6 | Green | (0, 255, 0) | (58, 91, 70) |

> **Note:** Color index 4 is not used in the display mapping.

### Color Saturation

The driver supports adjustable saturation (0.0 to 1.0):
- **0.0:** Pure desaturated colors (vivid primaries)
- **0.5:** Balanced blend (default)
- **1.0:** Fully saturated colors (more realistic, muted tones)

---

## Electrical Specifications

### Power Requirements

| Parameter | Value |
|-----------|-------|
| **Operating Voltage** | 3.3V (from Raspberry Pi) |
| **Power Consumption (Active)** | ~0.5W during refresh |
| **Power Consumption (Idle)** | ~0mW (image persists without power) |
| **Peak Current** | ~150mA during refresh |

### GPIO Pin Configuration

| Pin Function | BCM Pin | Physical Pin | Default |
|--------------|---------|--------------|---------|
| **RESET** | GPIO 27 | Pin 13 | High |
| **BUSY** | GPIO 17 | Pin 11 | Pull-up |
| **DC (Data/Command)** | GPIO 22 | Pin 15 | Low |
| **CS (Chip Select)** | GPIO 8 (CE0) | Pin 24 | High |
| **MOSI** | GPIO 10 | Pin 19 | SPI |
| **SCLK** | GPIO 11 | Pin 23 | SPI |

---

## Communication Interface

### SPI Configuration

| Parameter | Value |
|-----------|-------|
| **Interface** | SPI0 |
| **Bus** | 0 |
| **Chip Select** | CE0 (GPIO 8) |
| **Clock Speed** | 1 MHz (1,000,000 Hz) |
| **Mode** | SPI Mode 0 (CPOL=0, CPHA=0) |
| **Bit Order** | MSB First |
| **Bits per Word** | 8 |
| **Chip Select Control** | Software (GPIO controlled) |

### I2C (EEPROM)

| Parameter | Value |
|-----------|-------|
| **Interface** | I2C1 |
| **EEPROM Address** | 0x50 |
| **Purpose** | Display identification and configuration |
| **Display Variant ID** | 22 |

---

## Display Controller

### Controller Chip: E673

The display uses a custom E Ink controller with the following command set:

| Command | Hex Code | Purpose |
|---------|----------|---------|
| PSR | 0x00 | Panel Setting Register |
| PWR | 0x01 | Power Setting |
| POF | 0x02 | Power Off |
| POFS | 0x03 | Power Off Sequence |
| PON | 0x04 | Power On |
| BTST1 | 0x05 | Booster Soft Start 1 |
| BTST2 | 0x06 | Booster Soft Start 2 |
| DSLP | 0x07 | Deep Sleep |
| BTST3 | 0x08 | Booster Soft Start 3 |
| DTM1 | 0x10 | Data Transmission Mode 1 |
| DSP | 0x11 | Data Stop |
| DRF | 0x12 | Display Refresh |
| PLL | 0x30 | PLL Control |
| CDI | 0x50 | VCOM and Data Interval |
| TCON | 0x60 | Temperature Sensor Control |
| TRES | 0x61 | Resolution Setting |
| REV | 0x70 | Revision |
| VDCS | 0x82 | VCOM DC Setting |
| PWS | 0xE3 | Power Saving |

### Initialization Sequence

```python
# Unlock command
0xAA: [0x49, 0x55, 0x20, 0x08, 0x09, 0x18]

# Power and panel settings
PWR (0x01): [0x3F]
PSR (0x00): [0x5F, 0x69]

# Booster settings
BTST1 (0x05): [0x40, 0x1F, 0x1F, 0x2C]
BTST3 (0x08): [0x6F, 0x1F, 0x1F, 0x22]
BTST2 (0x06): [0x6F, 0x1F, 0x17, 0x17]

# Display configuration
POFS (0x03): [0x00, 0x54, 0x00, 0x44]
TCON (0x60): [0x02, 0x00]
PLL (0x30): [0x08]
CDI (0x50): [0x3F]
TRES (0x61): [0x03, 0x20, 0x01, 0xE0]  # 800x480
PWS (0xE3): [0x2F]
VDCS (0x82): [0x01]
```

---

## Performance Characteristics

### Refresh Timing

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Core Refresh Time** | ~12 seconds | At 25°C - 50°C |
| **Total Refresh Cycle** | 20-25 seconds | Including data transfer and ready state |
| **Busy Wait Timeout** | 32 seconds | Maximum wait for display update |
| **Temperature Impact** | Slower at lower temps | Refresh time increases below 25°C |

### Display Lifespan

| Parameter | Estimated Value |
|-----------|----------------|
| **Refresh Cycles** | ~1,000,000+ cycles |
| **Image Retention** | Indefinite (no power required) |
| **Ghosting** | Minimal with proper refresh cycles |

---

## Physical Features

### Connectors

- **40-pin GPIO Header:** Connects to Raspberry Pi
- **2× Qw/ST Connectors:** Qwiic/STEMMA QT compatible for I2C breakouts
- **Expansion Header:** For additional hardware

### Buttons

- **4× Rear-Mounted Buttons** (November 2025+ models)
  - Previous models had side-mounted buttons
  - Improved durability during shipping

### Mounting Hardware

**Included:**
- M2.5 standoffs
- M2.5 screws
- 40-pin extension header (for full-size Raspberry Pi clearance)

---

## Compatibility

### Supported Raspberry Pi Models

| Model | Compatible | Notes |
|-------|-----------|-------|
| Raspberry Pi 5 | ✅ Yes | Full support |
| Raspberry Pi 4 | ✅ Yes | Full support |
| Raspberry Pi 3 | ✅ Yes | Full support |
| Raspberry Pi Zero 2 W | ✅ Yes | Requires extension header |
| Raspberry Pi Zero W | ✅ Yes | Requires extension header |
| Raspberry Pi 2 | ✅ Yes | Full support |

**Requirements:**
- 40-pin GPIO header
- SPI and I2C enabled
- Python 3.7+

---

## Software Driver Details

### Python Library

**Repository:** https://github.com/pimoroni/inky

**Class:** `InkyE673` (from `inky_e673.py`)

**Import:**
```python
from inky import InkyE673
display = InkyE673(resolution=(800, 480))
```

### Key Methods

```python
# Initialize display
display = InkyE673(resolution=(800, 480))

# Set image with saturation control
display.set_image(image, saturation=0.5)

# Set individual pixel
display.set_pixel(x, y, color)

# Update display
display.show(busy_wait=True)

# Set border color
display.set_border(color)
```

### Color Constants

```python
display.BLACK   # 0
display.WHITE   # 1
display.YELLOW  # 2
display.RED     # 3
display.BLUE    # 4
display.GREEN   # 5
```

---

## Data Format

### Pixel Encoding

- **Bits per Pixel:** 4 bits (16 colors, 6 used)
- **Packing:** Two pixels per byte (nibble-packed)
- **Buffer Size:** 800 × 480 ÷ 2 = 192,000 bytes
- **Byte Order:** Big-endian (MSB first)

### Image Processing

1. **Input:** PIL Image (any format)
2. **Quantization:** 6-color palette with Floyd-Steinberg dithering
3. **Remapping:** Sequential palette → display native (skip index 4)
4. **Packing:** Nibble-pack two pixels per byte
5. **Transfer:** SPI transmission to display controller

---

## Environmental Specifications

### Operating Conditions

| Parameter | Range |
|-----------|-------|
| **Temperature (Operating)** | 0°C to 50°C |
| **Temperature (Optimal)** | 25°C to 40°C |
| **Humidity** | 35% to 65% RH (non-condensing) |
| **Storage Temperature** | -25°C to 70°C |

### Display Characteristics

- **Sunlight Readable:** Yes (reflective display)
- **Backlight:** None (reflective technology)
- **Power in Sunlight:** 0W (image persists) |
- **Eye Strain:** Minimal (no flicker, no backlight)

---

## Mechanical Specifications

### Weight

| Component | Weight |
|-----------|--------|
| Display + PCB | ~95g |
| With mounting hardware | ~105g |

### Fragility

> **⚠️ WARNING:** The display is made from glass and is fragile.
> - Do not drop or apply pressure to the screen
> - Handle by PCB edges only
> - Not a touchscreen - do not press on display surface

---

## Use Cases

### Ideal Applications

- ✅ Home automation dashboards
- ✅ Electronic photo frames
- ✅ Weather stations
- ✅ Calendar displays
- ✅ Information kiosks
- ✅ E-readers
- ✅ Digital signage (indoor)
- ✅ Battery-powered displays

### Not Recommended For

- ❌ Video playback
- ❌ Real-time animations
- ❌ Gaming
- ❌ High-frequency updates
- ❌ Touchscreen applications

---

## Advantages of Spectra 6

### Improvements Over Previous Generation

| Feature | Previous Gen | Spectra 6 |
|---------|-------------|-----------|
| **Refresh Time** | ~15-20s | ~12s |
| **Color Saturation** | Lower | Higher |
| **Color Accuracy** | Good | Excellent |
| **Available Sizes** | Limited | Extended range |
| **Power Efficiency** | Good | Better |

---

## Schematic and Resources

### Official Documentation

- **Schematic (7.3" Spectra):** [PDF Link](https://cdn.shopify.com/s/files/1/0174/1800/files/inky_impression_73_spectra_schematic.pdf)
- **Mechanical Drawing:** [PNG Link](https://cdn.shopify.com/s/files/1/0174/1800/files/inky-impression-7-3-drawing.png)
- **Product Page:** [Pimoroni Shop](https://shop.pimoroni.com/products/inky-impression-7-3)
- **Getting Started Guide:** [Learn Article](https://learn.pimoroni.com/article/getting-started-with-inky-impression)
- **Python Library:** [GitHub](https://github.com/pimoroni/inky)

---

## Package Contents

- 1× Inky Impression 7.3" display with PCB
- 1× 40-pin extension header
- 4× M2.5 standoffs
- 8× M2.5 screws
- Quick start guide

---

## Regulatory Information

- **RoHS Compliant:** Yes
- **CE Marked:** Yes
- **FCC Compliant:** Yes (as Raspberry Pi accessory)

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| Nov 2025 | v2.0 | Rear-mounted buttons (improved durability) |
| 2024 | v1.0 | Initial Spectra 6 release |

---

## Technical Support

- **GitHub Issues:** https://github.com/pimoroni/inky/issues
- **Forums:** https://forums.pimoroni.com
- **Email:** support@pimoroni.com

---

*This specification is based on the Pimoroni Inky Impression 7.3" Spectra 6 Edition (E673 controller) as of January 2026.*
