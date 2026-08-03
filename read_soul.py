#!/usr/bin/env python3
"""Read SOUL.md content from Mi8 and Mi6"""
import sys

path = "/root/.hermes/SOUL.md"
try:
    with open(path) as f:
        content = f.read()
    print(content)
except FileNotFoundError:
    print("FILE_NOT_FOUND")
