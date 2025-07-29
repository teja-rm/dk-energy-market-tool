import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from .config import settings

plt.style.use("seaborn-v0_8-darkgrid")

def price_heatmap(df: pd.DataFrame, area: str) -> Path:
    df_area = df[df.PriceArea == area].copy()
    df_area["date"] = df_area["HourUTC"].dt.date
    df_area["hour"] = df_area["HourUTC"].dt.hour
    pivot = df_area.pivot(index="hour", columns="date", values="DKK_per_MWh")
    fig, ax = plt.subplots(figsize=(14, 7), dpi=120)
    im = ax.imshow(pivot, aspect="auto", origin="lower", cmap="viridis")
    cbar = fig.colorbar(im, ax=ax, label="DKK/MWh")
    ax.set_ylabel("Hour of Day")
    ax.set_xlabel("Date")
    ax.set_title(f"Spot-Price Heatmap {area}")
    fname = settings.report_dir / f"heatmap_{area}.png"
    fname.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(fname, bbox_inches="tight")
    plt.close(fig)
    return fname
