from datetime import datetime
from pathlib import Path

import jinja2
import pandas as pd
import weasyprint

from .analyse import descriptive_stats, arima_forecast
from .visuals import price_heatmap
from .config import settings

TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: Helvetica, sans-serif; margin: 2rem; }
    h1 { color: #003366; }
    table { border-collapse: collapse; width: 100%%; }
    th, td { border: 1px solid #ddd; padding: .5rem; text-align: right; }
    th { background: #efefef; }
    img { max-width: 100%%; }
  </style>
</head>
<body>
  <h1>Danish Energy Market Report – {{ ts }}</h1>

  <h2>1. Descriptive Statistics</h2>
  {{ stats_html | safe }}

  <h2>2. Forecast (Next 24 hours)</h2>
  {% for area, fc_path in forecast_plots.items() %}
    <h3>{{ area }}</h3>
    <img src="{{ fc_path }}" />
  {% endfor %}

  <h2>3. Intraday Heatmaps</h2>
  {% for area, hm_path in heatmaps.items() %}
    <h3>{{ area }}</h3>
    <img src="{{ hm_path }}" />
  {% endfor %}
</body>
</html>
"""

def build_report(df: pd.DataFrame) -> Path:
    env = jinja2.Environment(autoescape=True)
    tmpl = env.from_string(TEMPLATE)

    stats_df = descriptive_stats(df)
    stats_html = stats_df.to_html(classes="tbl", float_format="{:.2f}".format)

    # Forecast plots
    forecast_plots: dict[str, str] = {}
    heatmaps: dict[str, str] = {}
    for area in settings.price_area:
        fc = arima_forecast(df, area)
        ax = fc.plot(title=f"ARIMA Forecast – {area}", figsize=(10, 4))
        fpath = settings.report_dir / f"forecast_{area}.png"
        ax.figure.savefig(fpath, bbox_inches="tight")
        ax.figure.clf()
        # Ensure forecast image path is a file URI
        forecast_plots[area] = fpath.resolve().as_uri()

        hm_path = price_heatmap(df, area)
        # Ensure heatmap image path is a file URI
        if isinstance(hm_path, Path):
            heatmaps[area] = hm_path.resolve().as_uri()
        else:
            heatmaps[area] = Path(hm_path).resolve().as_uri()

    html = tmpl.render(
        ts=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        stats_html=stats_html,
        forecast_plots=forecast_plots,
        heatmaps=heatmaps,
    )

    out_html = settings.report_dir / f"market_report_{datetime.utcnow():%Y%m%d}.html"
    out_html.parent.mkdir(parents=True, exist_ok=True)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"INFO: HTML report generated at {out_html}")
    return out_html
