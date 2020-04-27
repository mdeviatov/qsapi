""""
The purpose of this script is to test a single connection on the QlikSense application.
This is a proof-of-concept for connection using certificate.
The information will be stored in a directory structure (one folder per application) that can be synced in git.
"""

import asyncio
import json
import logging
import os
import ssl
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


async def main():
    async with websockets.connect(uri, ssl=ssl_context, extra_headers=headers) as websocket:
        msg = await websocket.recv()
        logging.info(f"< {msg}")
        logging.info("Continue processing...")
        doclist = await get_doclist(websocket)
    for doc in doclist:
        logging.info(f"Collecting info for {doc}")
        # New websocket connection is required for each open app.
    logging.info("End Application")


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
uri = os.getenv('REMOTE_URI')
workdir = os.getenv('WORKDIR')
certdir = os.getenv('CERT_DIR')
user_directory = os.getenv('USERDIRECTORY')
user_id = os.getenv('USERID')

cert_file = os.path.join(certdir, 'client.pem')
key_file = os.path.join(certdir, 'client_key.pem')
ca_file = os.path.join(certdir, 'root.pem')
qlik_user = f"UserDirectory={user_directory}; UserId={user_id}"
headers = {'X-Qlik-User': qlik_user}

ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=ca_file)
ssl_context.load_cert_chain(cert_file, keyfile=key_file)
# ssl_context.load_verify_locations(cafile=ca_file)
print(ssl_context.cert_store_stats())
print(ssl.get_default_verify_paths())
# raise Exception('OK for now...')
asyncio.run(main())
