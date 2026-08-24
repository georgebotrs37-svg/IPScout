#!/usr/bin/env python3
# ==========================================================
#  IPScout - Advanced IP Location Finder
#  By The Cyber Bite
#  Powered by ip-api.com
# ==========================================================

import requests
import socket
import csv
import os
import webbrowser


# ---------------- Colors for terminal output ----------------
class Colors:
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


API_URL = "http://ip-api.com/json/{}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,timezone,query"


# ---------------- Core Functions ----------------

def is_valid_ip(ip_address):
    """Check if the given string is a valid IPv4 or IPv6 address."""
    if not ip_address:
        return False
    try:
        socket.inet_pton(socket.AF_INET, ip_address)
        return True
    except socket.error:
        pass
    try:
        socket.inet_pton(socket.AF_INET6, ip_address)
        return True
    except socket.error:
        return False


def get_my_ip():
    """Get the public IP address of the current machine."""
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json().get("ip")
    except requests.RequestException:
        return None


def get_location(ip_address):
    """Fetch geolocation data for a given IP address (IPv4 or IPv6)."""
    if not is_valid_ip(ip_address):
        return {"status": "fail", "message": "Invalid IP address format (IPv4/IPv6)"}

    try:
        response = requests.get(API_URL.format(ip_address), timeout=8)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "fail", "message": f"HTTP Error {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Failed to connect to the API"}
    except requests.exceptions.Timeout:
        return {"status": "fail", "message": "Request timed out"}
    except requests.RequestException as e:
        return {"status": "fail", "message": str(e)}


def display_result(data):
    """Pretty print the location result."""
    c = Colors
    if data.get("status") == "success":
        print(f"\n{c.GREEN}{'='*45}{c.RESET}")
        print(f"{c.BOLD}{c.CYAN}IP Address   : {c.RESET}{data.get('query')}")
        print(f"{c.BOLD}Country      : {c.RESET}{data.get('country')}")
        print(f"{c.BOLD}Region       : {c.RESET}{data.get('regionName')}")
        print(f"{c.BOLD}City         : {c.RESET}{data.get('city')}")
        print(f"{c.BOLD}ZIP Code     : {c.RESET}{data.get('zip')}")
        print(f"{c.BOLD}Latitude     : {c.RESET}{data.get('lat')}")
        print(f"{c.BOLD}Longitude    : {c.RESET}{data.get('lon')}")
        print(f"{c.BOLD}Timezone     : {c.RESET}{data.get('timezone')}")
        print(f"{c.BOLD}ISP          : {c.RESET}{data.get('isp')}")
        print(f"{c.BOLD}Organization : {c.RESET}{data.get('org')}")
        print(f"{c.BOLD}ASN          : {c.RESET}{data.get('as')}")
        lat, lon = data.get("lat"), data.get("lon")
        if lat and lon:
            print(f"{c.BOLD}Map Link     : {c.RESET}{c.MAGENTA}https://www.google.com/maps?q={lat},{lon}{c.RESET}")
        print(f"{c.GREEN}{'='*45}{c.RESET}")
    else:
        print(f"{c.RED}[!] Error: {data.get('message', 'Unknown error')}{c.RESET}")


def save_to_csv(results, filename="ipscout_results.csv"):
    """Save a list of result dicts to a CSV file."""
    if not results:
        print(f"{Colors.YELLOW}[!] No results to save.{Colors.RESET}")
        return

    file_exists = os.path.isfile(filename)
    fields = ["query", "country", "regionName", "city", "zip", "lat", "lon",
              "timezone", "isp", "org", "as", "status"]

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        for r in results:
            writer.writerow(r)

    print(f"{Colors.GREEN}[+] Results saved to {filename}{Colors.RESET}")


def generate_map_html(results, filename="ipscout_map.html"):
    """Generate an interactive HTML map (Leaflet + OpenStreetMap) for one or more results."""
    points = [r for r in results if r.get("status") == "success" and r.get("lat") and r.get("lon")]
    if not points:
        print(f"{Colors.YELLOW}[!] No valid locations to plot on the map.{Colors.RESET}")
        return

    center_lat = points[0]["lat"]
    center_lon = points[0]["lon"]

    markers_js = ""
    for p in points:
        popup = (
            f"{p.get('query')}<br>{p.get('city')}, {p.get('country')}<br>"
            f"ISP: {p.get('isp')}"
        ).replace("'", "\\'")
        markers_js += (
            f"L.marker([{p['lat']}, {p['lon']}]).addTo(map)"
            f".bindPopup('{popup}');\n"
        )

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>IPScout - Interactive Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        html, body, #map {{ height: 100%; margin: 0; padding: 0; }}
        #title {{
            position: absolute; top: 10px; left: 50px; z-index: 1000;
            background: #111; color: #0f0; font-family: monospace;
            padding: 8px 16px; border-radius: 6px; border: 1px solid #0f0;
        }}
    </style>
</head>
<body>
    <div id="title">🌍 IPScout - Interactive Map</div>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([{center_lat}, {center_lon}], {6 if len(points) == 1 else 2});
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap contributors'
        }}).addTo(map);
        {markers_js}
    </script>
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"{Colors.GREEN}[+] Interactive map saved to {filename}{Colors.RESET}")
    try:
        webbrowser.open(f"file://{os.path.abspath(filename)}")
    except Exception:
        pass


# ---------------- Menu Actions ----------------

def action_single_lookup():
    ip = input(f"\n{Colors.CYAN}Enter an IP address (IPv4 or IPv6): {Colors.RESET}").strip()

    if not ip:
        print(f"{Colors.RED}[!] You didn't enter anything. Please type an IP address.{Colors.RESET}")
        return

    data = get_location(ip)
    display_result(data)
    if data.get("status") == "success":
        save = input(f"\n{Colors.YELLOW}Save result to CSV? (y/n): {Colors.RESET}").strip().lower()
        if save == "y":
            save_to_csv([data])
        show_map = input(f"{Colors.YELLOW}Open on interactive map? (y/n): {Colors.RESET}").strip().lower()
        if show_map == "y":
            generate_map_html([data])


def action_bulk_lookup():
    print(f"\n{Colors.CYAN}Enter multiple IP addresses separated by commas:{Colors.RESET}")
    raw = input("> ").strip()
    ip_list = [ip.strip() for ip in raw.split(",") if ip.strip()]

    if not ip_list:
        print(f"{Colors.RED}[!] No IP addresses provided.{Colors.RESET}")
        return

    all_results = []
    for ip in ip_list:
        print(f"\n{Colors.YELLOW}Looking up: {ip}...{Colors.RESET}")
        data = get_location(ip)
        display_result(data)
        all_results.append(data)

    save = input(f"\n{Colors.YELLOW}Save all results to CSV? (y/n): {Colors.RESET}").strip().lower()
    if save == "y":
        save_to_csv(all_results)

    show_map = input(f"{Colors.YELLOW}Open all on interactive map? (y/n): {Colors.RESET}").strip().lower()
    if show_map == "y":
        generate_map_html(all_results)


def action_my_ip():
    print(f"\n{Colors.CYAN}Fetching your public IP address...{Colors.RESET}")
    my_ip = get_my_ip()
    if not my_ip:
        print(f"{Colors.RED}[!] Could not determine your public IP.{Colors.RESET}")
        return
    print(f"{Colors.GREEN}Your public IP is: {my_ip}{Colors.RESET}")
    data = get_location(my_ip)
    display_result(data)
    if data.get("status") == "success":
        show_map = input(f"\n{Colors.YELLOW}Open on interactive map? (y/n): {Colors.RESET}").strip().lower()
        if show_map == "y":
            generate_map_html([data])


def show_banner():
    c = Colors
    print(f"""{c.GREEN}{c.BOLD}
+==========================================+
|              IPScout v2.0                 |
|      Advanced IP Location Finder          |
|      IPv4 / IPv6 - Interactive Map        |
|           By The Cyber Bite               |
+==========================================+{c.RESET}
    """)


def show_menu():
    c = Colors
    print(f"""{c.CYAN}
[1] Look up a single IP address
[2] Look up multiple IP addresses
[3] Find my own public IP & location
[4] Exit
{c.RESET}""")


# ---------------- Main Program ----------------

def main():
    show_banner()
    while True:
        show_menu()
        choice = input(f"{Colors.YELLOW}Choose an option (1-4): {Colors.RESET}").strip()

        if choice == "1":
            action_single_lookup()
        elif choice == "2":
            action_bulk_lookup()
        elif choice == "3":
            action_my_ip()
        elif choice == "4":
            print(f"{Colors.MAGENTA}Goodbye!{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}[!] Invalid choice, try again.{Colors.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.MAGENTA}\nInterrupted. Goodbye!{Colors.RESET}")