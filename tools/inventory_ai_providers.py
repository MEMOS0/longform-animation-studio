"""Write the current AI provider inventory without exposing credentials."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio.providers import write_inventory


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", default="data/processed/ai_provider_inventory.json")
    parser.add_argument("--output-md", default="data/processed/ai_provider_inventory.md")
    args = parser.parse_args()
    rows = write_inventory(Path(args.output_json), Path(args.output_md))
    print({"providers": len(rows), "output": args.output_md})


if __name__ == "__main__":
    main()
