# from Server.models.db import DB
from models import db
db = db.DB()
SUCCESS = "OK".encode()
FAILURE = "KO".encode()
SOCKET_EOF = "\n\r\n\r".encode()
