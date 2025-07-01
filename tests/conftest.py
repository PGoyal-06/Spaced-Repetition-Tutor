# tests/conftest.py
import sys
import os

# Compute the absolute path to <project root>/src
HERE = os.path.dirname(__file__)
SRC = os.path.abspath(os.path.join(HERE, "..", "src"))

# Prepend it so pytest and your tests see `import src.*`
if SRC not in sys.path:
    sys.path.insert(0, SRC)
