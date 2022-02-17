import venv
import tempfile
import subprocess
from os import path
import sys
import shutil

tmp_dir = tempfile.mkdtemp(prefix='venv_')
venv.create(tmp_dir, with_pip=True)
subprocess.run([path.join(tmp_dir, 'bin', 'pip'), 'install', 'pyfiglet', '--no-cache-dir'], stdout=subprocess.DEVNULL)
subprocess.run([path.join(tmp_dir, 'bin', 'python'), '-m', 'figdate', *(sys.argv[1:])])
shutil.rmtree(tmp_dir)
