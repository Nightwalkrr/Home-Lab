#!/usr/bin/env python3
import subprocess
import csv
import time
from datetime import datetime
import os
import re

def scan_wifi():
	"""Scan Available WiFi Networks using nmcli"""
	try:
		result = subprocess.check_output(
			["nmcli","-t","-f","SSID,SIGNAL,BARS,CHAN,SECURITY","dev","wifi"],
			universal_newlines=True
		)
		return result.strip().split("\n")
	except Exception as e:
		print(f"Error scanning Wifi: {e}")
		return []

def save_to_csv(data, location, filename="wifi_scan_results.csv"):
	"""Save scan results to CSV with Location"""
	file_exists = os.path.isfile(filename)

	with open(filename, mode="a", newline="") as file:
		writer = csv.writer(file)

		# Write header only if file is new 
		if not file_exists:
			writer.writerow(["Timestamp", "Location", "SSID", "Signal", "Bars", "Channel", "Security"])
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		for line in data:
			if not line.strip():
				continue
				# Split with a negative lookbehind regex on unescaped colons olny
			parts = re.split(r'(?<!\\):',line)
			if len(parts) >= 5:
				# Unescaped any remaining \: in the SSID
				ssid = parts[0].replace('\\:',':')
				signal = parts[1]
				bars = parts[2]
				channel = parts[3]
				security = parts[4]
				writer.writerow([timestamp, location, ssid, signal, bars, channel, security])

def main():
	title = "Wifi - Signal Mapping Tool"
	print("=" * 70)
	print(f" {title} ".center(70, "="))
	print("=" * 70)
	print("\n\nPress 'R' + Enter to scan repeatedly on same location\n")
	print("Press 'Q' + Enter to quit\n")

	while True:
		user_input = input("Ready to scan ? (R = repeat mode/ Enter = single scan / Q = quit): ").strip().upper()

		if user_input == "Q":
			print("Exiting...")
			break

		# Ask for location everytime before scanning 
		location = input("Enter the Location (e.g. Office_floor, canteen. ) : ").strip()
		if not location:
			location = "Unknow"

		if user_input == "R":
			try:
				seconds_input=input("\n Scan in how many seconds? (e.g. 0.5, 5) : \n")
				scan_delay=float(seconds_input)
				print(f"\n[Repeat Mode] Location: {location} | Scanning every {scan_delay} seconds.\n Press Ctrl + C to stop.\n")
				while True:
					data = scan_wifi()
					save_to_csv(data,location)
					print(f"[{datetime.now().strftime('%H:%M:%S')}] Location: {location} | {len(data)} networks found")
					time.sleep(scan_delay)
			except ValueError:
			        print("\n[!] Error: Please enter a valid number (e.g., 30 or 1.5)\n\n")

			except KeyboardInterrupt:
				print(f"\n[+] Continuous scan stopped by user.\n")

		else:
			"""Single scan"""
			data = scan_wifi()
			save_to_csv(data,location)
			print(f"Scan Complete - Location: {location} | {len(data)} network found and saved.")
if __name__ == "__main__":
	main()
