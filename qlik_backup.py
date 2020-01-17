""""
The purpose of this script is to collect the current situation of a Qlik Sense environment: applications in scope, load
scripts...
The information will be stored in a directory structure (one folder per application) that can be synced in git.
"""

import asyncio
import json
import logging
import os
import websockets
from lib import my_env
from lib.qlik_methods import *


async def get_doclist():
    async with websockets.connect(uri) as websocket:
        msg = await websocket.recv()
        logging.debug(f"< {msg}")
        await websocket.send(json.dumps(getDocList))
        docstr = await websocket.recv()
        docjson = json.loads(docstr)
        return docjson['result']['qDocList']


async def qlik_get_script(app_id):
    async with websockets.connect(uri) as websocket:
        msg = await websocket.recv()
        logging.debug(f"< {msg}")
        openDoc['params'] = dict(qDocName=app_id, qNoData=True)
        await websocket.send(json.dumps(openDoc))
        next_msg = await websocket.recv()
        logging.debug(f"< {next_msg}")
        await websocket.send(json.dumps(getScript))
        next_msg = await websocket.recv()
        logging.debug(f"< {next_msg}")
        return next_msg


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
uri = os.getenv('URI')

# Collect doclist
doclist = asyncio.get_event_loop().run_until_complete(get_doclist())

workdir = os.getenv('WORKDIR')
for doc in doclist:
    res = asyncio.get_event_loop().run_until_complete(qlik_get_script(doc['qDocId']))
    script = json.loads(res)['result']['qScript']
    doc_name = os.path.splitext(doc['qDocName'])[0]
    load_script = os.path.join(workdir, f"{doc_name}.txt")
    logging.info(f"Working on {doc_name}")
    fh = open(load_script, 'wb')
    fh.write(str.encode(script))
    fh.close()
logging.info("End Application")
