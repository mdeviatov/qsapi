import certifi
import os
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = True
ssl_context.load_default_certs()

# if platform.system().lower() == 'darwin':
ssl_context.load_verify_locations(
    cafile=os.path.relpath(certifi.where()),
    capath=None,
    cadata=None)
openssl_dir, openssl_cafile = os.path.split(ssl.get_default_verify_paths().openssl_cafile)
# no content in this folder
os.listdir(openssl_dir)
# non existent file
print(openssl_dir)
print(openssl_cafile)
print(os.path.exists(openssl_cafile))
