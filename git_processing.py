#!/opt/envs/qlik/bin/python
import argparse
import datetime
import git
import logging
from lib import my_env
from lib.sense_engine_api import init_env

# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
# Configure command line arguments and environment
parser = argparse.ArgumentParser(description="Specify target environment")
parser.add_argument('-t', '--target', type=str, default='Local', choices=['Local', 'Remote'],
                    help='Please provide the target environment (Local, Remote).')
args = parser.parse_args()
logging.info("Arguments: {a}".format(a=args))
props = init_env(args.target)
workdir = props['workdir']

# Add commit username and password.
# Print commit result
# Push
my_repo = git.Repo(workdir)
if my_repo.is_dirty(untracked_files=True):
    logging.info("Preparing git update")
    my_repo.index.add('*')
    now_obj = datetime.datetime.now()
    now = "{now:%d-%m-%Y %H:%M:%S}".format(now=now_obj)
    msg = f"Snapshot from {now}"
    res = my_repo.index.commit(msg)
    my_repo.remotes.origin.push('master')
else:
    logging.info("No changes detected")
