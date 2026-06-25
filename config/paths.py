# -*- coding: utf-8 -*-
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

NUMBER_FILE_PATH = DATA_DIR / "number_file.json"
PERMUTATIONS_FILE_PATH = DATA_DIR / "permutations_file.json"
