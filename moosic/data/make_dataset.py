import os
import urllib.error
from pathlib import Path
from urllib.request import urlretrieve

from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    src = os.getenv("DATA_URL")
    root = Path(__file__).parents[2]
    dst = root / "data" / "raw" / "3_spotify_5000_songs.csv"
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        download_path = urlretrieve(src, dst)[0]
    except urllib.error.HTTPError as e:
        if str(e).startswith("HTTP Error 404"):
            raise FileNotFoundError("Dataset unreachable (error 404).") from None
    print("Dataset downloaded to", Path(download_path).relative_to(root))
