import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_PARENT = os.path.dirname(PROJECT_ROOT)

if PROJECT_PARENT not in sys.path:
    sys.path.insert(0, PROJECT_PARENT)
