import os
import urllib.error
from pathlib import Path
from urllib.request import urlretrieve

import typer
from loguru import logger
from tqdm import tqdm

from moosic.config import RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(output_path: Path = RAW_DATA_DIR / "dataset.csv"):

    src = os.getenv("RAW_DATA_URL")
    dst = Path(output_path)
    dst.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Downloading dataset...")
    try:
        with DownloadProgress(desc="Downloading", unit="B", unit_scale=True, miniters=1) as p:
            urlretrieve(src, dst, p.report)
    except urllib.error.HTTPError as e:
        if str(e).startswith("HTTP Error 404"):
            logger.error("Dataset unreachable (error 404).")
        else:
            logger.exception("An error occurred while downloading the dataset.")
    else:
        logger.success("Downloading dataset complete.")


class DownloadProgress(tqdm):
    """Provides hook to display download progress"""

    def report(self, block_num=1, block_size=1, total_size=None):
        if total_size is not None:
            self.total = total_size
        self.n = min(self.total, block_num * block_size)
        self.update(0)


if __name__ == "__main__":
    app()
