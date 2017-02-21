import sys
import socket

if __name__ == '__main__':
    print("enter a query:")
    port = 8001 if len(sys.argv) != 2 else sys.argv[1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", int(port)))
    message = "query:" + sys.stdin.readline()
    sock.send(message.encode())
    # sock.close()


# Definitions file for server API variables/strings.
# Make calls to these variables in code instead of explicit definitions.
class client_api:
    data_separator = "|"

    # Client message codes
    login_code = "login"
    register_code = "register"
    upload_code = "upload"
    retrieve_code = "retrieve"
    search_code = "search"
    delete_code = "delete"

    # Server message codes
    login_status_code = "login_status"
    login_status_good = "ok"
    login_status_bad = "bad"