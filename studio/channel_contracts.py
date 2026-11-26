"""Machine-readable channel/audience contract fit checks."""
from __future__ import annotations

import json
import re
import importlib.resources
from pathlib import Path
from typing import Any

REPO_PATH = Path(__file__).resolve().parents[1] / "knowledge" / "market" / "channel_contracts.json"
DEFAULT_PATH = REPO_PATH if REPO_PATH.exists() else importlib.resources.files("studio") / "package_data" / "channel_contracts.json"


def load_contracts(path: Path = DEFAULT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_channel_fit(premise_text: str, contract_id: str, path: Path = DEFAULT_PATH) -> dict[str, Any]:
    contracts = load_contracts(path)
    if not contract_id:
        return {"contract_id": "", "status": "unspecified", "warnings": ["channel/audience contract is unspecified"], "matched_positive_signals": [], "missing_positive_signals": []}
    if contract_id not in contracts:
        return {"contract_id": contract_id, "status": "unknown", "warnings": ["unknown contract id"], "matched_positive_signals": [], "missing_positive_signals": []}
    contract = contracts[contract_id]
    low = premise_text.lower()
    matched = [signal for signal in contract["positive_signals"] if re.search(rf"\b{re.escape(signal.lower())}\b", low)]
    missing = [signal for signal in contract["positive_signals"] if signal not in matched]
    warnings = []
    if len(matched) < 2:
        warnings.append("surface premise has weak fit with the selected channel contract")
    return {
        "contract_id": contract_id,
        "status": "attention" if warnings else "pass",
        "reference_channels": contract["reference_channels"],
        "matched_positive_signals": matched,
        "missing_positive_signals": missing[:8],
        "opening_rules": contract["opening_rules"],
        "risk_patterns": contract["risk_patterns"],
        "thumbnail_rules": contract["thumbnail_rules"],
        "warnings": warnings,
        "evidence": contract["evidence"],
    }
