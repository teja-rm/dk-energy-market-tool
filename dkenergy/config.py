from pathlib import Path
from pydantic import BaseModel, Field

class Settings(BaseModel):
    api_base: str = Field(
        "https://api.energidataservice.dk/dataset", description="EDS root URL"
    )
    dataset: str = Field("Elspotprices", description="Primary dataset name")
    price_area: list[str] = Field(default_factory=lambda: ["DK1", "DK2"])
    lookback_days: int = 365
    raw_dir: Path = Path("data/raw")
    parquet_dir: Path = Path("data/parquet")
    report_dir: Path = Path("data/reports")
    user_agent: str = "DK-Energy-Tool/1.0 (https://github.com/<your-handle>)"
    max_retries: int = 5
    backoff: float = 0.5

settings = Settings()  # singleton-style import
