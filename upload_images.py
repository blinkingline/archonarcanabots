#!/usr/bin/python
# -*- coding: utf8 -*-
"""Upload all images from a directory to the wiki.

Usage: python3 upload_images.py <directory> [--ext png,jpg]
"""

import os
import sys
import argparse
import connections

parser = argparse.ArgumentParser(description="Upload images from a local directory to the wiki")
parser.add_argument("directory", help="Path to directory containing images")
parser.add_argument("--ext", type=str, default="png,jpg,jpeg,gif,svg", help="Comma-separated list of extensions to upload")
args = parser.parse_args()

extensions = tuple("." + e.lstrip(".").lower() for e in args.ext.split(","))
images = sorted(
    f for f in os.listdir(args.directory)
    if os.path.splitext(f)[1].lower() in extensions
)

if not images:
    print(f"No images found in {args.directory}")
    sys.exit(1)

print(f"Found {len(images)} images to upload.")
wp = connections.get_wiki()

for i, filename in enumerate(images):
    path = os.path.join(args.directory, filename)
    print(f"[{i+1}/{len(images)}] {filename} ...", end=" ", flush=True)
    try:
        with open(path, "rb") as f:
            result = wp.upload(f, filename)
        upload_result = result.get("upload", {}).get("result", "")
        if upload_result == "Success":
            print("OK")
        elif upload_result == "Warning":
            warnings = result.get("upload", {}).get("warnings", {})
            print(f"Warning: {warnings}")
        else:
            print(f"Unexpected result: {result}")
    except Exception as e:
        print(f"ERROR: {e}")

print("Done.")
