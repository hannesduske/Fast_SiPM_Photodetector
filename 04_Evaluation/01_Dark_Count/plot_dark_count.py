"""Plot SiPM dark count rate vs. temperature for several bias voltages."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
CSV_FILE = HERE / "dark_count.csv"
PNG_FILE = HERE / "dark_count.png"
WINDOW_INTERVALS = 10  # counts are taken over 10 timebase intervals


def read_data(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    timebase_us = float(rows[0][1])
    header_idx = next(i for i, r in enumerate(rows) if r and r[0].startswith("Temp"))
    labels = [h.strip() for h in rows[header_idx][1:] if h.strip()]

    temps, series = [], {label: [] for label in labels}
    for row in rows[header_idx + 1:]:
        if not row or not row[0].strip():
            continue
        temps.append(float(row[0]))
        for label, value in zip(labels, row[1:]):
            series[label].append(float(value))
    return timebase_us, temps, series


def main():
    timebase_us, temps, series = read_data(CSV_FILE)
    window_s = WINDOW_INTERVALS * timebase_us * 1e-6

    fig, ax = plt.subplots(figsize=(8, 5))
    for label, counts in series.items():
        rate_khz = [c / window_s / 1e3 for c in counts]
        ax.plot(temps, rate_khz, marker="o", label=f"$V_{{bias}}$ = {label}")

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Dark count rate (kHz)")
    ax.set_title(
        f"SiPM Dark Count Rate"
    )
    ax.grid(True, which="both", alpha=0.4)
    ax.legend()
    fig.tight_layout()
    fig.savefig(PNG_FILE, dpi=200)
    print(f"Saved plot to {PNG_FILE}")


if __name__ == "__main__":
    main()
