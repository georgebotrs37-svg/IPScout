# 🌍 IPScout v2.0

Advanced IP Location Finder using Python & [ip-api.com](http://ip-api.com).

## ✨ Features
- 🔎 Look up a **single IP** address (IPv4 **and IPv6**)
- 📋 Look up **multiple IP addresses** at once
- 📍 Detect **your own public IP** and location automatically
- 🗺️ **Interactive map** (Leaflet + OpenStreetMap) opens right in your browser, with markers for every result
- 💾 **Save results** to CSV file
- ✅ IP address **format validation**
- 🎨 Colored terminal output
- 🛡️ Full error handling (timeouts, connection errors, invalid input)

## ⚙️ Installation

```bash
pip install requests
```

## 🚀 Usage

```bash
python ip_scout.py
```

You'll see an interactive menu:

```
[1] Look up a single IP address
[2] Look up multiple IP addresses
[3] Find my own public IP & location
[4] Exit
```

### Example Output

```
IP Address   : 8.8.8.8
Country      : United States
Region       : California
City         : Mountain View
ZIP Code     : 94043
Latitude     : 37.4056
Longitude    : -122.0775
Timezone     : America/Los_Angeles
ISP          : Google LLC
Organization : Google Public DNS
ASN          : AS15169 Google LLC
Map Link     : https://www.google.com/maps?q=37.4056,-122.0775
```

## 🗺️ Interactive Map
After any lookup, choose to open an interactive map (`ipscout_map.html`) — it opens automatically in your default browser with a pin for every IP you looked up.

## 💾 CSV Export
Results can be saved to `ipscout_results.csv`, appending each new lookup so you build a history over time.

## 🌐 IPv4 / IPv6 Support
IPScout validates and accepts both IPv4 (`8.8.8.8`) and IPv6 (`2001:4860:4860::8888`) addresses.

## ⚠️ Accuracy Note
IP geolocation gives an **approximate** location based on the ISP's registration data, not an exact GPS position. Results are usually accurate at the country/region level, and sometimes at the city level, but may not pinpoint smaller towns or exact addresses.

## 📌 Note
This project uses the free [ip-api.com](http://ip-api.com) API (rate limit: 45 requests/minute) and [ipify.org](https://www.ipify.org) for public IP detection.

---

Author: **George Boutrs** |(https://github.com/georgebotrs37-svg)
