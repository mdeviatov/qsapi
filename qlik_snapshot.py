#!/opt/envs/qlik/bin/python
import os
from lib.my_env import run_script
my_path = os.path.dirname(__file__)
run_script(my_path, 'qlik_explore.py')
run_script(my_path, 'git_processing.py')
