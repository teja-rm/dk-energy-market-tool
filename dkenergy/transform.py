import json
import logging
import pandas as pd
from pathlib import Path

from .config import settings

log = logging.getLogger(__name__)
COLS = ["HourUTC", "PriceArea", "SpotPriceDKK"]

def _read_json(fp: Path) -> pd.DataFrame:
    data = json.loads(fp.read_text())["records"]
    return pd.DataFrame(data)[COLS]

def build_parquet() -> pd.DataFrame:
    frames = []
    for fp in settings.raw_dir.glob("elspot_*.json"):
        frames.append(_read_json(fp))
    df = pd.concat(frames).drop_duplicates().sort_values("HourUTC")
    df["HourUTC"] = pd.to_datetime(df["HourUTC"], utc=True)
    df["DKK_per_MWh"] = df["SpotPriceDKK"]  # clarity alias
    out = settings.parquet_dir / "spot.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    log.info("Parquet written: %s with %s rows", out, len(df))
    return df
