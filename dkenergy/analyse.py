import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from .config import settings

def descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("PriceArea")["DKK_per_MWh"]
    stats = g.agg(
        mean="mean",
        median="median",
        stdev="std",
        skew="skew",
        kurt=lambda x: x.kurtosis(),
        max="max",
        min="min",
    )
    stats["pct_range"] = (stats["max"] - stats["min"]) / stats["mean"]
    return stats.round(2)

def arima_forecast(df: pd.DataFrame, area: str, hours: int = 24) -> pd.Series:
    ts = (
        df[df.PriceArea == area]
        .set_index("HourUTC")["DKK_per_MWh"]
        .asfreq("1h")
        .interpolate()
    )
    model = ARIMA(ts, order=(1, 1, 1))
    result = model.fit()
    forecast = result.forecast(steps=hours)
    return forecast
