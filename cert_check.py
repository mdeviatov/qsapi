"""
This script prints certificate information
"""

import logging
import os
import ssl
import pprint
from lib import my_env

# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
certdir = os.getenv('CERT_DIR')

cert_file = 'root.pem'
ffn = os.path.join(certdir, cert_file)
try:
    cert_dict = ssl._ssl._test_decode_cert(ffn)
except Exception as e:
    logging.fatal(f"Error decoding certificate: {e}")
else:
    print(f"Certificate {cert_file} data: \n")
    pprint.pprint(cert_dict)
