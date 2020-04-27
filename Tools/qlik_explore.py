""""
The purpose of this script is to explore the current situation of a Qlik Sense environment: applications in scope, load
scripts...
The information will be stored in a directory structure (one folder per application) that can be synced in git.
"""

import argparse
import asyncio
import shutil
from lib import my_env
from lib.sense_engine_api import *


async def main():
    # Connect to engine and collect list of applications
    async with set_connection(**props) as websocket:
        sid = 0
        msg = await websocket.recv()
        logging.debug(f"< {msg}")
        sid += 1
        doclist = await get_doclist(websocket, sid)
    # For each application collect the information in the stream\application directory
    for doc in doclist:
        stream_dir = set_stream_dir(args.target, doc['qMeta'], workdir)
        logging.info(f"Collecting info for {doc['qDocName']} on {stream_dir}")
        doc_id = doc['qDocId']
        # New websocket connection is required for each open app.
        async with set_connection(doc_id, **props) as websocket:
            dimension_dict = {}
            sid = 0
            msg = await websocket.recv()
            logging.debug(f"< {msg}")
            sid += 1
            app_handle = await open_app(websocket, sid, doc_id)
            sid += 1
            app_layout = await get_app_layout(websocket, sid, app_handle)
            app_name = app_layout['qTitle']
            app_path = os.path.join(stream_dir, app_name)
            if os.path.isdir(app_path):
                shutil.rmtree(app_path)
            os.mkdir(app_path)
            script = await get_script(websocket, sid, app_handle)
            doc_name = os.path.splitext(doc['qDocName'])[0]
            load_script = os.path.join(app_path, f"{doc_name}.qvs")
            with open(load_script, 'wb') as fh:
                fh.write(str.encode(script))
            # Collect Sheets, dimensions and measures layout
            sid += 1
            objects_handle = await create_app_objectlist(websocket, sid, app_handle)
            sid += 1
            layout = await get_layout(websocket, sid, objects_handle)
            dimensions = layout['qDimensionList']['qItems']
            for dim in dimensions:
                sid += 1
                dimension_handle = await get_dimension(websocket, sid, app_handle, dim['qInfo']['qId'])
                sid += 1
                dimension_data = await get_layout(websocket, sid, dimension_handle)
                title = dimension_data["qMeta"]["title"]
                dimension_dict[title] = dimension_data
            """
            measurements = layout['qMeasureList']['qItems']
            for measure in measurements:
                measure_handle = await get_measure(websocket, sid, app_handle, measure['qInfo']['qId'])
                measure_data = await get_layout(websocket, sid, measure_handle)
                title = measure_data["qMeta"]["title"]
                measure_dict[title] = measure_data
            """
        dimension_str = json.dumps(dimension_dict, ensure_ascii=False, sort_keys=True, indent=4)
        with open(os.path.join(app_path, 'dimensions.json'), 'w', encoding='utf-8') as fh:
            fh.write(dimension_str)
        """
        measure_str = json.dumps(measure_dict, ensure_ascii=False, sort_keys=True, indent=4)
        with open(os.path.join(app_path, 'measures.json'), 'w', encoding='utf-8') as fh:
            fh.write(measure_str)
            """

    logging.info("End Application")


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

asyncio.run(main())
