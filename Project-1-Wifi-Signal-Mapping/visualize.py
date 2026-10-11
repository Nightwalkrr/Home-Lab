#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_data(filename="wifi_scan_results.csv",top_n=30):
	try:
		df = pd.read_csv(filename)
	except FileNotFoundError:
		print("No data file found. Run WiFi_scan.py .")
		return

	# Convert Signal to numeric
	df["Signal"] = pd.to_numeric(df["Signal"], errors="coerce")
	df = df.dropna(subset=["Signal"])

	# Average signal strength per SSID
	avg_signal = (
		df.groupby("SSID")["Signal"]
		.mean()
		.sort_values(ascending=False)
		.head(top_n)
	)

	plt.figure(figsize=(12, 6))
	avg_signal.plot(kind="bar",color="grey")
	plt.title(f"Average Wi-Fi Signal Strength by SSID (Top {top_n} SSIDs)")
	plt.ylabel("Signal Strenth (%)")
	plt.xlabel("SSID")
	plt.xticks(rotation=0, ha="center")
	plt.tight_layout()
	plt.savefig("average_signal.png", dpi=150)
	plt.close()

	# Single Distribution readings (Top N only)
	top_ssids = avg_signal.index.tolist()
	df_top = df[df["SSID"].isin(top_ssids)]

	plt.figure(figsize=(12, 6))
	sns.boxplot(data=df, x="SSID", y="Signal", fliersize=0)
	sns.stripplot(data=df, x="SSID", y="Signal", color="Pink", alpha=0.5, size=3)
	plt.title(f"Wi-Fi Signal Strength Distribution (Top {top_n} SSIDs)")
	plt.xticks(rotation=0, ha="center")
	plt.tight_layout()
	plt.savefig("signal_distribution.png", dpi=150)
	plt.close()

	# Bonus: Average Signal by LOcation
	if "Location" in df.columns:
		loc_avg = df.groupby("Location")["Signal"].mean().sort_values(ascending=False)

	plt.figure(figsize=(10,5))
	loc_avg.plot(kind="bar", color="lightgreen")
	plt.title("Average Signal Strength by Location")
	plt.ylabel("Signal Strength (%)")
	plt.xticks(rotation=0, ha="center")
	plt.tight_layout()
	plt.savefig("signal_by_location.png")
	plt.close()

	print("Graphs saved:\n - average_signal.png\n - signal_distribution.png\n - signal_by_location.png")

if __name__ == "__main__":
	visualize_data(top_n=15)
