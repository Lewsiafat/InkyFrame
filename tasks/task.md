# Task: Debugging WiFi App

- [x] **GPIO Buttons**: Fix `button_monitor.py` to use `gpiod`. <!-- id: 0 -->
    - [x] Analyze reference vs current code.
    - [x] Update `button_monitor.py`.
    - [x] Update `install_wifi.sh` dependencies.
    - [x] **VERIFIED**: User confirmed buttons work.
- [x] **AP Mode IP**: Fix IP address display in Hotspot mode. <!-- id: 1 -->
    - [x] Analyze `network_manager.py` for IP retrieval logic. <!-- id: 2 -->
    - [x] Implement logic to prefer Hotspot IP (e.g. `10.42.0.1` or `192.168.4.1`) when in AP mode. (Fixed in `network_manager.py`). <!-- id: 3 -->
    - [x] Update display/QR code generation to use correct IP. (Implicitly fixed by `get_ip_address` update). <!-- id: 4 -->
- [x] **DHCP**: Fix "Obtaining IP Address" loop. <!-- id: 5 -->
    - [x] Disable system-wide `dnsmasq` in `install_wifi.sh`. <!-- id: 6 -->
    - [x] **VERIFIED**: User confirmed it works. <!-- id: 7 -->
- [x] **Finalize**: Commit and Push. <!-- id: 8 -->
    - [x] Git add/commit. <!-- id: 9 -->
    - [x] Git push. <!-- id: 10 -->
