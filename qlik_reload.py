#!/opt/envs/qlik/bin/python
""""
The purpose of this script is to reload Qlik applications. Applications are reloaded in sequence.
"""

import argparse
import asyncio
from lib import my_env
from lib.sense_engine_api import *


async def main(dryrun=False):
    global sid, config
    # Connect to engine and collect list of applications
    async with set_connection(**props) as websocket:
        msg = await websocket.recv()
        logging.debug(f"< {msg}")
        doclist = await get_doclist(websocket, sid := sid+1)
    # Convert doclist into dictionary with key title and value ID of the document.
    application = {}
    duplicates = []
    for doc in doclist:
        app_name = doc['qTitle']
        doc_id = doc['qDocId']
        if app_name in application:
            duplicates.append(app_name)
        else:
            application[app_name] = doc_id
    reload_group = config['Reload']["apps"]
    reload_list = reload_group.split(",")
    reload_list = [app.strip() for app in reload_list]
    for app in reload_list:
        logging.info(f"App {app} reload started.")
        try:
            doc_id = application[app]
        except KeyError:
            logging.fatal(f"App {app} not found in Qlik")
            break
        if app in duplicates:
            logging.warning(f"Duplicate entries found for app {app}, docId {doc_id} is used.")
        async with set_connection(doc_id, **props) as websocket:
            msg = await websocket.recv()
            logging.debug(f"< {msg}")
            # Open Application
            app_handle = await open_app(websocket, sid := sid+1, doc_id)
            if isinstance(app_handle, str):
                # Error message found, app_handle needs to be int
                logging.fatal(f"Cannot open app {app} for reload, exiting...")
                break
            if not dryrun:
                res = await do_reload(websocket, sid := sid+1, app_handle)
                if res:
                    logging.info(f"App {app} reload done.")
                else:
                    logging.fatal(f"Issue with reload of app {app}, exiting.")
                    break
    logging.info("End Application")


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
# Configure command line arguments and environment
parser = argparse.ArgumentParser(description="Specify target environment")
parser.add_argument('-t', '--target', type=str, default='Local', choices=['Local', 'Remote'],
                    help='Please provide the target environment (Local, Remote).')
parser.add_argument('-d', '--dryrun', action='store_true',
                    help="If set then Dry Run - test on existence of app on engine only but do not reload.")
args = parser.parse_args()
logging.info("Arguments: {a}".format(a=args))
props = init_env(args.target)
workdir = props['workdir']
sid = 0

asyncio.run(main(args.dryrun))
