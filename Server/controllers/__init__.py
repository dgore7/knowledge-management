from Server.models.db import DB

db = DB()
SUCCESS = "OK".encode()
FAILURE = "KO".encode()
SOCKET_EOF = "\n\r\n\r".encode()
