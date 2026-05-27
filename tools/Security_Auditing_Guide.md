# Security Auditing Field Guide: Essential Tools & Techniques

This guide provides an overview of the industry-standard tools used for network discovery, vulnerability assessment, and security auditing. 

---

## 1. Nmap (Network Mapper)
**Purpose:** Network discovery and security auditing. It identifies what devices are on a network and what services they are running.

### Basic Scan (Ping Sweep)
Find "live" hosts on a local network without deep scanning.
```bash
nmap -sn 192.168.1.0/24
```

### Service and OS Detection
Identifies the version of software running on open ports and guesses the operating system.
```bash
nmap -A 192.168.1.100
```

---

## 2. Burp Suite
**Purpose:** Web application security testing. It acts as a proxy between your browser and the target server.

### How to use:
1. **Intercept:** Turn on Intercept in the 'Proxy' tab.
2. **Analyze:** Look at the raw HTTP requests your browser sends.
3. **Repeater:** Send a request to the 'Repeater' tab to modify parameters and see how the server responds (great for finding bugs in forms or APIs).

---

## 3. Metasploit Framework
**Purpose:** A platform for developing, testing, and executing exploit code against a remote target.

### Standard Workflow:
1. **Search:** `search type:exploit name:service_name`
2. **Select:** `use exploit/path/to/exploit`
3. **Configure:** Set options like `RHOSTS` (Target IP) and `LHOST` (Your IP).
4. **Audit:** Use check commands to see if the target is vulnerable before attempting any action.

---

## 4. Wireshark
**Purpose:** A graphical network protocol analyzer. It lets you see what’s happening on your network at a microscopic level.

### Key Use Cases:
* **Troubleshooting:** Identifying why a connection is failing.
* **Security:** Spotting unencrypted sensitive data (like passwords) being sent over protocols like HTTP or FTP.

---

## 5. Hashcat
**Purpose:** The world's fastest password recovery tool. Used to audit the strength of password hashes.

### Audit Example:
Test how long it takes to crack a common MD5 hash.
```bash
hashcat -m 0 -a 0 hashes.txt wordlist.txt
```

---

## 6. Bluetooth Auditing (Recon & Analysis)
**Purpose:** Identifying Bluetooth devices in range and auditing their security profiles (Classic and BLE).

### Discovery with bluetoothctl
The built-in Linux utility for managing Bluetooth.
```bash
bluetoothctl
[bluetooth]# power on
[bluetooth]# scan on
```

### Advanced Recon with Bettercap
Used for sniffing BLE (Bluetooth Low Energy) devices and mapping their services.
```bash
sudo bettercap
> ble.recon on
> ble.show
```

### Sniffing with Btlejack
The "Swiss-army knife" for BLE auditing, used to sniff or hijack active connections.
```bash
# Sniff all BLE advertisements
btlejack -s
```

---

## 🛡️ Professional & Ethical Standards
1. **Written Permission:** Never use these tools on a network or system you do not own without explicit, written authorization.
2. **The Goal is Defense:** Use these tools to find weaknesses so they can be fixed, not to cause harm.
3. **Privacy:** Respect the data and privacy of others at all times during an audit.
