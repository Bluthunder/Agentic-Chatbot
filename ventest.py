import os
import sys

running_in_virtualenv = bool(os.environ.get("VIRTUAL_ENV"))
if running_in_virtualenv:
    print("Running in a virtual environment.")
else:
    print("Not running in a virtual environment.")

if (sys.base_prefix or getattr(sys, 'real_prefix', None)) != sys.prefix:
    print("Detected virtual environment.")
