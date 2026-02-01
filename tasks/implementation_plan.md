# Button Monitor Migration Plan

The goal is to fix the "GPIO not available" error on Raspberry Pi 5 / Bookworm by migrating from the deprecated `RPi.GPIO` library to the modern `gpiod` library, matching the project's reference examples.

## User Review Required

> [!IMPORTANT]
> This change replaces the logic to use `gpiod`. This requires the `gpiod` and `gpiodevice` python packages to be installed on the system. I will verify and update `install_wifi.sh` to ensure these are present.

## Proposed Changes

### Scripts

#### [MODIFY] [button_monitor.py](file:///c:/Users/Lewis/Documents/workspace/inky/scripts/wifi/button_monitor.py)
- Remove `RPi.GPIO` imports.
- Import `gpiod`, `gpiodevice`, `gpiod.line`.
- Initialize GPIO chip using `gpiodevice.find_chip_by_platform()`.
- Request line for GPIO 5 (Button A) with `Direction.INPUT`, `Bias.PULL_UP`, and `Edge.BOTH`.
- Refactor `monitor_loop` to use `request.read_edge_events(timeout=...)` to handle button presses and long-press detection efficiently.

#### [MODIFY] [install_wifi.sh](file:///c:/Users/Lewis/Documents/workspace/inky/scripts/wifi/install_wifi.sh)
- Ensure `gpiod` and `gpiodevice` are installed via `pip` or `apt` as appropriate.
- (Likely adding `gpiod gpiodevice` to the pip install command).

## Verification Plan

### Manual Verification
1.  **Deploy Changes:** Run `deploy_wifi.bat` (or sync files manually).
2.  **Re-run Installer:** Execute `sudo ./scripts/wifi/install_wifi.sh` on the Pi to ensure dependencies are installed.
3.  **Check Logs:** Run `journalctl -u inky-monitor -f` or check `/var/log/inky/monitor.log`.
    - Verify "GPIO not available" warning is GONE.
    - Verify "Button Monitor..." started successfully.
4.  **Test Button:**
    - Press and hold Button A for 5 seconds.
    - Confirm log shows "Long Press Detected".
    - Confirm the service switches (WiFi <-> Main).
