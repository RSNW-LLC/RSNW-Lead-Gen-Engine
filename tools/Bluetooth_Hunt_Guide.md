# How to Find a "Hidden" Bluetooth Device (RSSI Hunting)

This method uses the **RSSI (Received Signal Strength Indicator)** to find the physical location of a device. It's like playing a game of "Hot or Cold" with your terminal.

---

## Step 1: Initialize the Hunt
Open your terminal and enter the Bluetooth control center:
```bash
bluetoothctl
```

Inside the prompt, turn on the power and start scanning:
```bash
power on
scan on
```

---

## Step 2: Identify your Target
Look for the list of devices appearing. You will see their **MAC Address** (e.g., `AA:BB:CC:11:22:33`) and their **Name**.

If you see a device you don't recognize, that's your target.

---

## Step 3: Monitor Signal Strength (The "Hot/Cold" Method)
Bluetooth signal strength is measured in **RSSI**. 
* **-90 to -100:** Very Weak (Far away or behind a wall)
* **-70 to -80:** Moderate (Same room)
* **-40 to -50:** Very Strong (You are standing right next to it!)

### How to Hunt:
1. Pick your target MAC address.
2. Slowly move around your house.
3. Watch the RSSI number in the terminal.
4. If the number gets **closer to 0** (e.g., goes from -80 to -50), you are getting **HOTTER**.
5. If the number drops (e.g., -50 to -90), you are getting **COLDER**.

---

## Step 4: Advanced Search (For BLE/Trackers)
Many hidden devices (like AirTags or Tile trackers) use **BLE (Bluetooth Low Energy)**. For these, use `bettercap`:

```bash
sudo bettercap
> ble.recon on
> ble.show
```

Bettercap will show you a "Last Seen" timer and much more detailed signal data.

---

### 🛡️ Safety Tip:
If you find a tracker (like an AirTag) that doesn't belong to you, be aware that many of these have "anti-stalking" features that may notify the owner if you tamper with them. Use this knowledge for your own device management and security audits only.
