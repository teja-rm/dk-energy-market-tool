from __future__ import annotations
import json
import logging
from datetime import date, timedelta
from typing import Any

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings

log = logging.getLogger(__name__)
Endpoint = str

@retry(
    stop=stop_after_attempt(settings.max_retries),
    wait=wait_exponential(multiplier=settings.backoff),
)
def _get(url: Endpoint, params: dict[str, Any]) -> dict[str, Any]:
    log.debug("GET %s %s", url, params)
    hdr = {"User-Agent": settings.user_agent}
    r = requests.get(url, params=params, headers=hdr, timeout=25)
    r.raise_for_status()
    return r.json()

def fetch_spot_prices() -> None:
    """Download DK spot prices into raw/*.json files (daily slices)."""
    today = date.today()
    for delta in range(settings.lookback_days):
        day = today - timedelta(days=delta)
        start = f"{day}"
        end = f"{day + timedelta(days=1)}"
        params = {
            "start": start,
            "end": end,
            "filter": json.dumps({"PriceArea": settings.price_area}),
            "sort": "HourDK",
            "limit": 0,
        }
        url = f"{settings.api_base}/{settings.dataset}"
        payload = _get(url, params)
        fname = settings.raw_dir / f"elspot_{day}.json"
        fname.parent.mkdir(parents=True, exist_ok=True)
        fname.write_text(json.dumps(payload))
        log.info("Saved %s (%s records)", fname, len(payload["records"]))
