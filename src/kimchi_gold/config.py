"""
Configuration settings for the Kimchi Premium project.
"""
import logging
from pathlib import Path

# -----------------
# PATHS
# -----------------
ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent
DATA_DIR: Path = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# -----------------
# FILENAMES
# -----------------
DATA_FILENAME: str = "kimchi_gold_price_log.csv"
DATA_FILE: Path = DATA_DIR / DATA_FILENAME

# -----------------
# PLOTTING
# -----------------
MONTHS_TO_PLOT: int = 12
PLOT_OUTPUT_FILENAME: str = f"kimchi_gold_price_recent_{MONTHS_TO_PLOT}months.png"
PLOT_OUTPUT_FILE: Path = DATA_DIR / PLOT_OUTPUT_FILENAME

# -----------------
# LOGGING
# -----------------
LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
