#!/opt/envs/qlik/bin/python
""""
The purpose of this script is to explore the current situation of a Qlik Sense environment: applications in scope, load
scripts...
The information will be stored in a directory structure (one folder per application) that can be synced in
git_processing.
"""

import argparse
# import asyncio
import shutil
from lib import my_env
from lib.sense_engine_api import *


async def dimensions(websocket, handle, dim_list, app_path):
    """
    Coroutine to collect dimension information in dictionary with key dimension name and value the dictionary for this
    dimension.

    :param websocket: Websocket connection
    :param handle: Handle to connect to - this is for the app.
    :param dim_list: List with dimensions from the application.
    :param app_path: Path for the Application information.
    :return: Dictionary with key dimension name and value the dictionary for the dimension.
    """
    global sid
    for dim in dim_list:
        dimension_handle = await get_dimension(websocket, sid := sid + 1, handle, dim['qInfo']['qId'])
        dimension_data = await get_properties(websocket, sid := sid + 1, dimension_handle)
        title = dimension_data["qDim"]["title"]
        my_env.dump_structure(dimension_data, os.path.join(app_path, 'QSMasterDimensions'), f"{title}.json")
    return


async def measurements(websocket, handle, measure_list, app_path):
    """
    Coroutine to collect measurement information in dictionary with key measurement name and value the dictionary for
    this measurement.

    :param websocket: Websocket connection
    :param handle: Handle to connect to - this is for the app.
    :param measure_list: List with measurements from the application.
    :param app_path: Path for the Application storage.
    :return: Dictionary with key measurement name and value the dictionary for the measurement.
    """
    global sid
    for measure in measure_list:
        measure_handle = await get_measure(websocket, sid := sid + 1, handle, measure['qInfo']['qId'])
        measure_data = await get_properties(websocket, sid := sid+1, measure_handle)
        title = measure_data['qMeasure']['qLabel']
        my_env.dump_structure(measure_data, os.path.join(app_path, 'QSMasterMeasures'), f"{title}.json")
    return


async def handle_sheets(websocket, handle, sheet_list, app_path):
    """
    Coroutine to collect sheet information and sheet child information.

    :param websocket: Websocket connection
    :param handle: Handle to connect to - this is for the app.
    :param sheet_list: List with measurements from the application.
    :param app_path: Path for application information.
    :return: Dictionary with key measurement name and value the dictionary for the measurement.
    """
    global sid
    for sheet in sheet_list:
        sheet_handle = await get_object(websocket, sid := sid + 1, handle, sheet['qInfo']['qId'])
        sheet_name = sheet['qMeta']['title']
        sheet_path = os.path.join(app_path, sheet_name)
        sheet_layout = await get_layout(websocket, sid := sid + 1, sheet_handle)
        sheet_props = await get_fullpropertytree(websocket, sid := sid + 1, sheet_handle)
        title = sheet_props['qProperty']['qMetaDef']['title']
        my_env.dump_structure(sheet_layout, sheet_path, f'{title}.json')
        sheet_children = sheet_layout['qChildList']['qItems']
        for child in sheet_children:
            try:
                child_id = child['qInfo']['qId']
                child_type = child['qInfo']['qType']
            except KeyError:
                logging.error(f"Issue with child collection on sheet {sheet_name}")
                continue
            else:
                child_path = os.path.join(sheet_path, child_type)
                title = child['qData']['title']
                if isinstance(title, dict) or len(title) == 0:
                    title = child_id
                child_handle = await get_object(websocket, sid := sid + 1, handle, child_id)
                # child_layout = await get_layout(websocket, sid := sid + 1, child_handle)
                child_layout = await get_fullpropertytree(websocket, sid := sid+1, child_handle)
                my_env.dump_structure(child_layout, child_path, f"{title}.json")
    return


async def main():
    global sid
    # Connect to engine and collect list of applications
    async with set_connection(**props) as websocket:
        msg = await websocket.recv()
        logging.debug(f"< {msg}")
        doclist = await get_doclist(websocket, sid := sid+1)
    # For each application collect the information in the stream\application directory
    for doc in doclist:
        app_name = doc['qTitle']
        stream_dir = set_stream_dir(args.target, doc['qMeta'], workdir)
        logging.info(f"Collecting info for {doc['qDocName']} on {stream_dir}")
        # Set and create Application Path
        app_path = os.path.join(stream_dir, app_name)
        if os.path.isdir(app_path):
            shutil.rmtree(app_path)
        os.mkdir(app_path)
        # New websocket connection is required for each open app.
        doc_id = doc['qDocId']
        async with set_connection(doc_id, **props) as websocket:
            sid = 0
            msg = await websocket.recv()
            logging.debug(f"< {msg}")
            # Open Application
            app_handle = await open_app(websocket, sid := sid+1, doc_id)
            if isinstance(app_handle, str):
                # Error message found, app_handle needs to be int
                continue
            # Get App Properties
            app_props = await get_app_properties(websocket, sid := sid+1, app_handle)
            my_env.dump_structure(app_props, app_path, "app_properties.json")
            # Get Script
            script = await get_script(websocket, sid := sid+1, app_handle)
            doc_name = os.path.splitext(doc['qDocName'])[0]
            load_script = os.path.join(app_path, f"{doc_name}.qvs")
            with open(load_script, 'wb') as fh:
                fh.write(str.encode(script))
            # Collect Sheets, dimensions and measures layout
            objects_handle = await create_app_objectlist(websocket, sid := sid+1, app_handle)
            layout = await get_layout(websocket, sid := sid+1, objects_handle)
            # Get variable list
            variables = layout['qVariableList']['qItems']
            my_env.dump_structure(variables, app_path, "variables.json", sort_keys=True)
            connections = await get_connections(websocket, sid := sid+1, app_handle)
            my_env.dump_structure(connections, app_path, "connections.json")
            # Collect master dimension information
            await dimensions(websocket, app_handle, layout['qDimensionList']['qItems'], app_path)
            # Collect master measurement information
            await measurements(websocket, app_handle, layout['qMeasureList']['qItems'], app_path)
            # Collect Sheet Information
            await handle_sheets(websocket, app_handle, layout['qAppObjectList']['qItems'], app_path)
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
workdir = props['workdir']
sid = 0

asyncio.run(main())
