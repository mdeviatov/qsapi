""""
The purpose of this script is to collect the information related to a specific application.
"""

import asyncio
import json
import logging
import os
import websockets
from lib import my_env
from lib.qlik_methods import *


async def qlik_get_app_info(app_id):
    async with websockets.connect(uri) as websocket:
        msg = await websocket.recv()
        logging.debug(f"< {msg}")
        openDoc['params'] = dict(qDocName=app_id, qNoData=True)
        await websocket.send(json.dumps(openDoc))
        next_msg = await websocket.recv()
        logging.debug(f"< {next_msg}")
        await websocket.send(json.dumps(getAllInfos))
        next_msg = await websocket.recv()
        logging.debug(f"< {next_msg}")
        return next_msg


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
uri = os.getenv('URI')

# workdir = os.getenv('WORKDIR')
app = "C:\\Users\\dvermeylen\\Documents\\Qlik\\Sense\\Apps\\PRO Discovery.qvf"
res = asyncio.get_event_loop().run_until_complete(qlik_get_app_info(app))
info_list = json.loads(res)['result']['qInfos']
for item in info_list:
    print(f"{item['qType']} - {item['qId']}")
logging.info("End Application")
