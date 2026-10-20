"""Plot SiPM single-photon signal amplitude vs. bias voltage."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
CSV_FILE = HERE / "single_photon.csv"
PNG_FILE = HERE / "single_photon.png"


def read_data(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.reader(f) if r and r[0].strip()]
    x_label, y_label = rows[0][0].strip(), rows[0][1].strip()
    x = [float(r[0]) for r in rows[1:]]
    y = [float(r[1]) for r in rows[1:]]
    return x_label, y_label, x, y


def main():
    _, _, voltage, amplitude = read_data(CSV_FILE)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(voltage, amplitude, marker="o")
    ax.set_xlim(25.5, 29.5)
    ax.set_ylim(0.5, 3.5)
    ax.set_xlabel("SiPM Bias voltage (V)")
    ax.set_ylabel("Single photon signal amplitude (mV)")
    ax.set_title("SiPM Single Photon Signal Amplitude")
    ax.grid(True, which="both", alpha=0.4)
    fig.tight_layout()
    fig.savefig(PNG_FILE, dpi=200)
    print(f"Saved plot to {PNG_FILE}")


if __name__ == "__main__":
    main()
