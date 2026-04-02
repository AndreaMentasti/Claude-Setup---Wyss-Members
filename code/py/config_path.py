from pathlib import Path

def change_paths():
    """
    Purpose:
        Deduce the project root from THIS file's location and return standard paths.
        Works in scripts and notebooks. Does NOT create folders.

        Data paths use config_local.py (gitignored) for the Dropbox bridge.
        Falls back to repo-relative data/ if config_local.py is absent.
    """
    # config_path.py is in: <root>/code/py/config_path.py -> parents[2] is <root>
    root_dir = Path(__file__).resolve().parents[2]

    # Data root: machine-specific via config_local.py (gitignored)
    try:
        from config_local import DATA_ROOT  # type: ignore[import]
        data_dir = Path(DATA_ROOT)
    except ImportError:
        data_dir = root_dir / "data"

    return {
        "root": root_dir,

        "code": root_dir / "code",
        "python": root_dir / "code" / "py",
        "prompts": root_dir / "code" / "prompts",
        "stata": root_dir / "code" / "stata",

        "data": data_dir,
        "rawdata": data_dir / "rawdata",
        "processed": data_dir / "processed",

        "output": root_dir / "output",
        "tables": root_dir / "output" / "tables",
        "figures": root_dir / "output" / "figures",
        "logs": root_dir / "output" / "logs",
        "maps": root_dir / "output" / "maps",
        "paper": root_dir / "output" / "paper",
    }
