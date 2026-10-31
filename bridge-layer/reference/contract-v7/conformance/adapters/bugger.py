#!/usr/bin/env python3
"""Adapter for the `bugger` box (R4: same setup, another machine). See _peer.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _peer import main  # noqa: E402

sys.exit(main("bugger"))
