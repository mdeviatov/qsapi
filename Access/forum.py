import os
import ssl
from lib import my_env
from websocket import create_connection

# Initialize Environment
projectname = "qlik"
config = my_env.init_env(projectname, __file__)
url = os.getenv('REMOTE_URI')
certdir = os.getenv('CERT_DIR')

privateKeyPath = certdir
# userDirectory and userId can be found at QMC -> Users
userDirectory, userId = "internal", "sa_engine"

certs = ({"ca_certs": privateKeyPath + "root.pem",
          "certfile": privateKeyPath + "client.pem",
          "keyfile": privateKeyPath + "client_key.pem",
          "cert_reqs": ssl.CERT_REQUIRED,
          "server_side": False
          })
ssl.match_hostname = lambda cert, hostname: True

ws = create_connection(url, sslopt=certs,
                       header={'X-Qlik-User: UserDirectory=%s; UserId=%s' % (userDirectory, userId)})
session = ws.recv()
print(session)
