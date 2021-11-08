# add the project directory to the pythonpath
import sys
from pathlib import Path
from os.path import dirname, realpath
dir_ = Path(dirname(realpath(__file__)))
sys.path.insert(0, str(dir_.parent))

