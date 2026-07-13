#!/usr/bin/env python3
"""Run the bundled UpScayl CLI with conservative image-type defaults."""
import argparse
import json
import os
import shutil
import subprocess
import sys


APP_BIN = "/Applications/Upscayl.app/Contents/Resources/bin/upscayl-bin"
APP_MODELS = "/Applications/Upscayl.app/Contents/Resources/models"
MODELS = {
    "photo": "high-fidelity-4x",
    "portrait": "high-fidelity-4x",
    "product": "high-fidelity-4x",
    "general": "ultramix-balanced-4x",
    "sharp": "ultrasharp-4x",
    "anime": "digital-art-4x",
    "illustration": "digital-art-4x",
    "text": "high-fidelity-4x",
}


def find_binary() -> str | None:
    return shutil.which("upscayl") or (APP_BIN if os.path.isfile(APP_BIN) else None)


def main() -> int:
    parser = argparse.ArgumentParser(description="Upscale an image with local UpScayl.")
    parser.add_argument("input", help="input JPG, PNG, or WebP path")
    parser.add_argument("output", help="new output path")
    parser.add_argument("--mode", choices=sorted(MODELS), default="general")
    parser.add_argument("--scale", type=int, choices=(2, 3, 4), default=2)
    parser.add_argument("--model", help="override the bundled model name")
    parser.add_argument("--json", action="store_true", help="emit a JSON result")
    args = parser.parse_args()

    binary = find_binary()
    error = None
    if not os.path.isfile(args.input):
        error = f"input file not found: {args.input}"
    elif binary is None:
        error = "UpScayl CLI not found; install UpScayl or provide an upscayl command on PATH"
    elif os.path.abspath(args.input) == os.path.abspath(args.output):
        error = "output must be different from input"
    if error:
        payload = {"ok": False, "error": error}
        print(json.dumps(payload, ensure_ascii=False) if args.json else error, file=sys.stderr)
        return 2

    command = [
        binary,
        "-i", args.input,
        "-o", args.output,
        "-s", str(args.scale),
        "-m", APP_MODELS if os.path.isdir(APP_MODELS) else "models",
        "-n", args.model or MODELS[args.mode],
        "-g", "auto",
        "-v",
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    payload = {
        "ok": completed.returncode == 0 and os.path.isfile(args.output),
        "input": os.path.abspath(args.input),
        "output": os.path.abspath(args.output),
        "mode": args.mode,
        "scale": args.scale,
        "model": args.model or MODELS[args.mode],
        "backend": binary,
        "exit_code": completed.returncode,
    }
    if completed.returncode != 0:
        payload["error"] = (completed.stderr or completed.stdout).strip()[-2000:]
    print(json.dumps(payload, ensure_ascii=False) if args.json else json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
