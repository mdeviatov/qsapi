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
from lib import my_env


# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
uri = os.getenv('REMOTE_URI')
workdir = os.getenv('WORKDIR')
certdir = os.getenv('CERT_DIR')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = os.path.join(certdir, 'client.pem')
print(ssl_context.load_verify_locations(localhost_pem))
