"""
config.py — Project path configuration for Populism and Narratives.

Two-folder design:
  - Repo paths (code, output) are always relative to this file's location.
  - Data paths are machine-specific: set DATA_ROOT in config_local.py (gitignored).

Usage in NEW scripts:
    import config as cfg
    df = pd.read_csv(cfg.DATA_RAW / "virality/tweets/all_main_data_with_location_info.csv")
    fig.savefig(cfg.FIGURES / "fig_name.png", dpi=300, bbox_inches='tight')
    df.to_stata(cfg.DATA_PROCESSED / "tweets/file.dta", write_index=False)

Note: Existing scripts use config_path.change_paths() instead. Both modules
read DATA_ROOT from config_local.py, so they resolve to the same Dropbox path.
"""
from pathlib import Path

# --- Repo root (always derived from this file's location) ---
# config.py lives at <repo_root>/code/py/config.py → parents[2] is repo root
REPO_ROOT    = Path(__file__).resolve().parents[2]
OUTPUT       = REPO_ROOT / "output"
FIGURES      = OUTPUT / "figures"
TABLES       = OUTPUT / "tables"
LOGS         = OUTPUT / "logs"
MAPS         = OUTPUT / "maps"
PAPER        = OUTPUT / "paper"
CODE         = REPO_ROOT / "code"
CODE_PY      = REPO_ROOT / "code" / "py"
CODE_STATA   = REPO_ROOT / "code" / "stata"
PROMPTS      = REPO_ROOT / "code" / "prompts"
QUALITY      = REPO_ROOT / "quality_reports"
TEMPLATES    = REPO_ROOT / "templates"
EXPLORATIONS = REPO_ROOT / "explorations"

# --- Data root: machine-specific via config_local.py (gitignored) ---
# config_local.py must define:
#   DATA_ROOT = Path(r"C:\Users\YourName\Dropbox\populism_and_narratives\data")
# Falls back to repo-relative data/ if config_local.py is absent.
try:
    from config_local import DATA_ROOT  # type: ignore[import]
    DATA_ROOT = Path(DATA_ROOT)
except ImportError:
    DATA_ROOT = REPO_ROOT / "data"

DATA_RAW       = DATA_ROOT / "rawdata"
DATA_PROCESSED = DATA_ROOT / "processed"


