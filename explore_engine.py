""""
The purpose of this script is to explore a single app on the QlikSense server in the same way as is done on the Engine
API Explorer.
"""

import asyncio
import os
import websockets
from lib import my_env
from lib.sense_engine_api import *
from urllib.parse import quote


async def main(app_id):
    logging.info(f"Collecting info on {uri} for {app_id}")
    async with websockets.connect(uri) as websocket:
        sid = 0
        msg = await websocket.recv()
        logging.info(f"< {msg}")
        sid += 1
        app_handle = await open_app(websocket, sid, app_id)
        sid += 1
        await get_all_infos(websocket, sid, app_handle)
        sid += 1
        dimension_handle = await get_dimension(websocket, sid, app_handle, 'd1')
        sid += 1
        await get_layout(websocket, sid, dimension_handle)
    logging.info("End Application")


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
uri = os.getenv('LOCAL_URI')
workdir = os.getenv('WORKDIR')
app = 'C:\\Users\\dvermeylen\\Documents\\Qlik\\Sense\\Apps\\BF - Communes V2.qvf'
uri = uri + quote(app)
asyncio.run(main(app))
