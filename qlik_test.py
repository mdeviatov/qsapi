#!/opt/envs/qlik/bin/python
""""
The purpose of this script is to test the doclist for applications that can be read for archiving.
"""

import argparse
from lib.sense_engine_api import *
from pprint import pprint


async def main():
    global sid
    # Connect to engine and collect list of applications
    async with set_connection(**props) as websocket:
        msg = await websocket.recv()
        logging.debug(f"< {msg}")
        doclist_all = await get_doclist(websocket, sid := sid + 1)
    pprint(doclist_all)
    # for doc in doclist_all:
    #     print(f"{doc['qDocName']} - {doc['qMeta']['createdDate']} {doc['qMeta']['privileges']}")
    # doclist = [doc for doc in doclist_all if doc['qMeta']['stream']['name'] != 'BF - Monitoring apps']
    logging.info("End Application")


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
# Configure command line arguments and environment
parser = argparse.ArgumentParser(description="Specify target environment")
parser.add_argument('-t', '--target', type=str, default='Remote', choices=['Local', 'Remote'],
                    help='Please provide the target environment (Local, Remote).')
args = parser.parse_args()
logging.info("Arguments: {a}".format(a=args))
props = init_env(args.target)

sid = 0

asyncio.run(main())
