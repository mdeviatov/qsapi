""""
The purpose of this script is to explore a single app on the QlikSense server.
The information will be stored in a directory structure (one folder per application) that can be synced in git.
"""

import asyncio
import os
import websockets
from lib import my_env
from lib.sense_engine_api import *


async def main(app_id):
    logging.info(f"Collecting info for {app_id}")
    # New websocket connection is required for each open app.
    async with websockets.connect(uri) as websocket:
        msg = await websocket.recv()
        logging.info(f"< {msg}")
        app_handle = await open_app(websocket, sid, app_id)
        sheets_handle = await create_app_objectlist(websocket, sid, app_handle)
        layout = await get_layout(websocket, sid, sheets_handle)
        dimensions = layout['qDimensionList']['qItems']
        for dim in dimensions:
            dimension_handle = await get_dimension(websocket, sid, app_handle, dim['qInfo']['qId'])
            dimension_data = await get_layout(websocket, sid, dimension_handle)
            print(f"Field: {dimension_data['qDim']['qFieldDefs']}, Label: {dimension_data['qDim']['qFieldLabels']}")
        measurements = layout['qMeasureList']['qItems']
        for measure in measurements:
            measure_handle = await get_measure(websocket, sid, app_handle, measure['qInfo']['qId'])
            measure_data = await get_layout(websocket, sid, measure_handle)
            print(f"Label: {measure_data['qMeasure']['qLabel']}, Def: {measure_data['qMeasure']['qDef']}")
    logging.info("End Application")


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
uri = os.getenv('URI')
workdir = os.getenv('WORKDIR')
app = 'C:\\Users\\dvermeylen\\Documents\\Qlik\\Sense\\Apps\\BF - Communes V2.qvf'
sid = 1
asyncio.run(main(app))
