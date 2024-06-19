import os
import urllib.error
from urllib.request import urlretrieve

from moosic.config import PROJ_ROOT, RAW_DATA_DIR, logger

src = os.getenv("DATA_URL")
dst = RAW_DATA_DIR / "3_spotify_5000_songs.csv"
dst.parent.mkdir(parents=True, exist_ok=True)

try:
    download_path = urlretrieve(src, dst)[0]
except urllib.error.HTTPError as e:
    if str(e).startswith("HTTP Error 404"):
        raise FileNotFoundError("Dataset unreachable (error 404).") from None

logger.info(f"Dataset downloaded to {dst.relative_to(PROJ_ROOT)}")
