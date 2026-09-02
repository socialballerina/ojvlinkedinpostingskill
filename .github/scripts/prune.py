#!/usr/bin/env python3
"""Keep the last 20 run folders. Older ones are only clutter in a public repo."""
import os
import shutil

KEEP = 20
root = "runs"
if os.path.isdir(root):
    dirs = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))
    # runs/latest.json is a file, not a folder, so it is never pruned
    for d in dirs[:-KEEP]:
        shutil.rmtree(os.path.join(root, d))
        print("pruned runs/%s" % d)
