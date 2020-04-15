""""
The purpose of this script is to explore a single app on the QlikSense server.
The information will be stored in a directory structure (one folder per application) that can be synced in git.
"""

import asyncio
import os
import shutil
import websockets
from lib import my_env
from lib.sense_engine_api import *
from urllib.parse import quote


async def main(app_id):
    logging.info(f"Collecting info for {app_id} on {uri}")
    dimension_dict = {}
    measure_dict = {}
    # New websocket connection is required for each open app.
    async with websockets.connect(uri) as websocket:
        sid = 0
        msg = await websocket.recv()
        logging.info(f"< {msg}")
        sid += 1
        app_handle = await open_app(websocket, sid, app_id)
        sid += 1
        app_layout = await get_app_layout(websocket, sid, app_handle)
        app_name = app_layout['qTitle']
        app_path = os.path.join(workdir, app_name)
        if os.path.isdir(app_path):
            shutil.rmtree(app_path)
        os.mkdir(app_path)
        sid += 1
        sheets_handle = await create_app_objectlist(websocket, sid, app_handle)
        sid += 1
        layout = await get_layout(websocket, sid, sheets_handle)
        sheets = layout['qAppObjectList']['qItems']
        for sheet in sheets:
            sheet_handle = await get_object(websocket, sid, app_handle, sheet['qInfo']['qId'])
            sheet_name = sheet['qMeta']['title']
            sheet_path = os.path.join(app_path, sheet_name)
            os.mkdir(sheet_path)
            sheet_children = await get_child_infos(websocket, sid, sheet_handle)
            for child in sheet_children:
                if child['qType'] == 'table':
                    print(child['qId'])
        """
        dimensions = layout['qDimensionList']['qItems']
        for dim in dimensions:
            sid += 1
            dimension_handle = await get_dimension(websocket, sid, app_handle, dim['qInfo']['qId'])
            sid += 1
            dimension_data = await get_layout(websocket, sid, dimension_handle)
            title = dimension_data["qMeta"]["title"]
            dimension_dict[title] = dimension_data
        measurements = layout['qMeasureList']['qItems']
        for measure in measurements:
            measure_handle = await get_measure(websocket, sid, app_handle, measure['qInfo']['qId'])
            measure_data = await get_layout(websocket, sid, measure_handle)
            title = measure_data["qMeta"]["title"]
            measure_dict[title] = measure_data
    dimension_str = json.dumps(dimension_dict, ensure_ascii=False, sort_keys=True, indent=4)
    with open(os.path.join(app_path, 'dimensions.json'), 'w', encoding='utf-8') as fh:
        fh.write(dimension_str)
    measure_str = json.dumps(measure_dict, ensure_ascii=False, sort_keys=True, indent=4)
    with open(os.path.join(app_path, 'measures.json'), 'w', encoding='utf-8') as fh:
        fh.write(measure_str)
    """
    logging.info("End Application")


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
uri = os.getenv('LOCAL_URI')
workdir = os.getenv('WORKDIR')
# app = 'C:\\Users\\dvermeylen\\Documents\\Qlik\\Sense\\Apps\\BF - Communes V2.qvf'
app = 'C:\\Users\\dvermeylen\\Documents\\Qlik\\Sense\\Apps\\ansible.qvf'
uri = uri + quote(app)
asyncio.run(main(app))
