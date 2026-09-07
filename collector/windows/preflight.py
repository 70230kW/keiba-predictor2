"""Validate the local prerequisites without connecting to JRA-VAN."""
import json
import os
import platform
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def inspect_environment(system=None, version=None, pointer_bits=None, sdk_path=None):
    system = system or platform.system()
    version = version or sys.version_info[:2]
    pointer_bits = pointer_bits or struct.calcsize("P") * 8
    sdk_value = sdk_path if sdk_path is not None else os.environ.get("JRA_VAN_SDK_PATH", "")
    sdk = Path(sdk_value) if sdk_value else None
    checks = {
        "windows": system == "Windows",
        "python_3_14_or_newer": tuple(version) >= (3, 14),
        "python_64_bit": pointer_bits == 64,
        "sdk_path_configured": bool(sdk_value),
        "sdk_path_exists": bool(sdk and sdk.is_dir()),
        "common_schema_exists": (ROOT / "ml" / "schema.json").is_file(),
        "active_source_is_jra_van": False,
    }
    active = ROOT / "ml" / "sources" / "active.json"
    if active.is_file():
        try:
            checks["active_source_is_jra_van"] = json.loads(active.read_text(encoding="utf-8")).get("provider") == "jra_van"
        except (OSError, json.JSONDecodeError):
            pass
    return checks


def main():
    checks = inspect_environment()
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    if not all(checks.values()):
        print("準備未完了です。collector/windows/README.mdを確認してください。", file=sys.stderr)
        return 1
    print("ローカル前提条件を確認しました。JV-Link通信はまだ実行していません。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
