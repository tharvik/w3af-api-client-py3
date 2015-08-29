from w3af_api_client import Connection

conn = Connection('http://10.108.114.195:5000/')
print(conn.get_version())
