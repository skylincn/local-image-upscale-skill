#!/usr/bin/env python3
"""Report locally available image upscaling backends without changing the system."""
import argparse
import json
import os
import shutil


COMMANDS = (
    ("realesrgan_ncnn_vulkan", "realesrgan-ncnn-vulkan"),
    ("upscayl", "upscayl"),
    ("magick", "magick"),
    ("convert", "convert"),
    ("python3", "python3"),
    ("ffmpeg", "ffmpeg"),
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    found = {name: shutil.which(command) for name, command in COMMANDS}
    app_bin = "/Applications/Upscayl.app/Contents/Resources/bin/upscayl-bin"
    app_models = "/Applications/Upscayl.app/Contents/Resources/models"
    found["upscayl_app_bin"] = app_bin if os.path.isfile(app_bin) else None
    found["upscayl_app_models"] = app_models if os.path.isdir(app_models) else None
    if args.json:
        print(json.dumps(found, ensure_ascii=False, indent=2))
        return
    for name, path in found.items():
        print(f"{name}: {path or 'missing'}")
    if not found["realesrgan_ncnn_vulkan"] and not found["upscayl"] and not found["upscayl_app_bin"]:
        print("status: no dedicated AI super-resolution backend detected")
        print("fallback: use ImageMagick/Pillow resize only, or install a backend after approval")
    else:
        print("status: dedicated AI super-resolution backend detected")


if __name__ == "__main__":
    main()
