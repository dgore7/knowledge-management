__copyright__ = "Copyright 2017. DePaul University. "
__license__ =  "All rights reserved. This work is distributed pursuant to the Software License for Community Contribution of Academic Work, dated Oct. 1, 2016. For terms and conditions, please see the license file, which is included in this distribution."
__author__ = "Ayadullah Syed, Jose Palacios, David Gorelik, Joshua Smith, Jasmine Farley, Jessica Hua, Steve Saucedo, Serafin Balcazar"

# Definitions file for server API variables/strings.
# Make calls to these variables in code instead of explicit definitions.


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