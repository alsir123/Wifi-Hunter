import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, "core")

for path in (ROOT, CORE):
    if path not in sys.path:
        sys.path.insert(0, path)
