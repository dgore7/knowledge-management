import sys
import socket


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

    # Universal message codes
    SUCCESS = "OK".encode()
    FAILURE = "KO".encode()