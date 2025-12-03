#!/usr/bin/env python3
"""Update SHA256 hash registry for config files.

This script scans config directories and updates the hash registry
with SHA256 checksums for all JSON configuration files.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIRECTORIES = [
    "config",
    "system/config",
]

HASH_REGISTRY_FILE = REPO_ROOT / "scripts" / "config_hash_registry.json"


def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 hash of file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def scan_config_files() -> dict[str, dict]:
    """Scan config directories and compute hashes."""
    registry = {}

    for config_dir in CONFIG_DIRECTORIES:
        config_path = REPO_ROOT / config_dir

        if not config_path.exists():
            print(f"Warning: {config_dir} does not exist")
            continue

        for json_file in config_path.rglob("*.json"):
            if "__pycache__" in str(json_file):
                continue

            rel_path = str(json_file.relative_to(REPO_ROOT))

            try:
                sha256 = compute_sha256(json_file)
                file_size = json_file.stat().st_size

                registry[rel_path] = {
                    "sha256": sha256,
                    "size_bytes": file_size,
                    "last_updated": datetime.utcnow().isoformat() + "Z",
                }

                print(f"✓ {rel_path}: {sha256[:16]}...")

            except Exception as e:
                print(f"✗ {rel_path}: Error - {e}")

    return registry


def main():
    """Update hash registry."""
    print("Scanning config files...")
    print()

    registry = scan_config_files()

    print()
    print(f"Found {len(registry)} config files")

    HASH_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HASH_REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, sort_keys=True)

    print(f"\nHash registry updated: {HASH_REGISTRY_FILE}")
    print("Commit this file with your config changes.")


if __name__ == "__main__":
    main()
