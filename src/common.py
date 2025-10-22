"""
common.py
----------
Shared helper functions for environment loading, data paths, schema validation, and logging.

Author: David Santana Rivera
Last updated: 10/21/2025
"""

import os
from dotenv import load_dotenv

# ---------- Environment Handling ----------

def load_environment(env_file=None):
    """
    Loads environment variables from the given .env file.
    Default: configs/sandbox.env (for local sandbox testing).
    """
    if env_file is None:
        env_file = os.getenv("ENV_FILE", "configs/sandbox.env")

    if not os.path.exists(env_file):
        raise FileNotFoundError(f"❌ Environment file not found: {env_file}")

    load_dotenv(env_file)
    print(f"✅ Environment loaded from {env_file}")

def get_env_var(key, default=None):
    """Safely get environment variable with optional default."""
    return os.getenv(key, default)

# ---------- Data Path Utilities ----------

def get_data_path(subdir):
    """Returns path to a given data subfolder (e.g., 'raw', 'interim')."""
    return os.path.join("data", subdir)

def validate_schema(df, expected_columns):
    """Ensures dataframe contains all expected columns."""
    missing = set(expected_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
