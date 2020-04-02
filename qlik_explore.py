""""
The purpose of this script is to explore the current situation of a Qlik Sense environment: applications in scope, load
scripts...
The information will be stored in a directory structure (one folder per application) that can be synced in git.
"""

import asyncio
import json
import logging
import os
import websockets
from lib import my_env


async def get_doclist(websocket):
    """
    Call GetDocList method from Global Class.

    :param websocket: Websocket connection handler.
    :return: List of application dictionaries.
    """
    doclist = dict(
        jsonrpc='2.0',
        handle=-1,
        id=1,
        method='GetDocList',
        params=[]
    )
    await websocket.send(json.dumps(doclist))
    docstr = await websocket.recv()
    logging.info(f"< {docstr}")
    docjson = json.loads(docstr)
    return docjson['result']['qDocList']


async def open_app(websocket, app_id):
    """
    Calls the OpenDoc method from the Global class.

    :param websocket: Websocket connection handler
    :param app_id: Application ID for application to open.
    :return: Application handle ID.
    """
    opendoc = dict(
        jsonrpc='2.0',
        handle=-1,
        id=1,
        method='OpenDoc',
        params=dict(
            qDocName=app_id,
            qNoData=True
        )
    )
    await websocket.send(json.dumps(opendoc))
    appstr = await websocket.recv()
    logging.info(f"< {appstr}")
    appjson = json.loads(appstr)
    handle = appjson['result']['qReturn']['qHandle']
    return handle


async def get_script(websocket, handle):
    """
    Calls the GetScript method from the Doc class.

    :param websocket: Websocket connection handler
    :param handle: Handle ID for the method.
    :return: App script in bytestream format.
    """
    getscript = dict(
        jsonrpc='2.0',
        handle=handle,
        id=1,
        method='GetScript',
        params={}
    )
    await websocket.send(json.dumps(getscript))
    script_str = await websocket.recv()
    logging.info(f"< {script_str}")
    script_json = json.loads(script_str)
    script = script_json['result']['qScript']
    return script


async def main():
    async with websockets.connect(uri) as websocket:
        msg = await websocket.recv()
        logging.info(f"< {msg}")
        doclist = await get_doclist(websocket)
    for doc in doclist:
        logging.info(f"Collecting info for {doc}")
        # New websocket connection is required for each open app.
        async with websockets.connect(uri) as websocket:
            msg = await websocket.recv()
            logging.info(f"< {msg}")
            handle = await open_app(websocket, doc['qDocId'])
            script = await get_script(websocket, handle)
            doc_name = os.path.splitext(doc['qDocName'])[0]
            load_script = os.path.join(workdir, f"{doc_name}.qvs")
            with open(load_script, 'wb') as fh:
                fh.write(str.encode(script))
    logging.info("End Application")


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
uri = os.getenv('URI')
workdir = os.getenv('WORKDIR')

asyncio.run(main())
