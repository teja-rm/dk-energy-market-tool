import logging
import typer
from .fetch import fetch_spot_prices
from .transform import build_parquet
from .report import build_report
from .config import settings

app = typer.Typer(add_help_option=True)
logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

@app.command()
def run(full: bool = typer.Option(False, help="Pull fresh data before analysis")):
    """Main pipeline: fetch → transform → analyse → report."""
    if full:
        fetch_spot_prices()
    df = build_parquet()
    pdf = build_report(df)
    typer.echo(f"✅ Report ready: {pdf}")

if __name__ == "__main__":
    app()
