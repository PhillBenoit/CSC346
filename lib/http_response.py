# used to mark string replacements
REPLACE_KEY = 'XXXX'

ADDRESS_KEY = 'HTTP_HOST'
PORT_KEY = 'SERVER_PORT'

# keys for the HTML response dictionary
OK_IDX = 200
REDIRECT_IDX = 303
BAD_RQ_IDX = 400
NOT_FOUND_IDX = 404
METHOD_IDX = 405
CONFLICT_IDX = 409

# HTML response dictionary
RESPONSES = {
    OK_IDX: "Status: 200 OK\nContent-Type: text/html\n",
    REDIRECT_IDX: "Status: 303 Redirect\nLocation: " + REPLACE_KEY + "\n",
    BAD_RQ_IDX: "Status: 400 Bad Request\n",
    NOT_FOUND_IDX: "Status: 404 Not Found\n",
    METHOD_IDX: "Status: 405 Method Not Allowed\nAllow: " + REPLACE_KEY + "\n",
    CONFLICT_IDX: "Status: 409 Conflict\n"
}


# return a 303 ridrect to the ui and set the session id cookie
def redirect_set_cookie(address, cookie, connection):
    connection.close()
    print("Status: 303 Redirect\nSet-Cookie: session_id="+cookie+"\nLocation: " + address + "\n")
    exit()


# utilizes HTML response dictionary to create a common endpoint
def respond(num, connection, param=None):
    response = RESPONSES[num]

    # parse HTML responses with variables
    if num == REDIRECT_IDX or num == METHOD_IDX:
        response = response.replace(REPLACE_KEY, param)

    print(response)

    # print data for 200 OK requests
    if num == OK_IDX:
        print(param + "\n")

    connection.close()
    exit()


# get the correct address to use with a 303 redirect from os.environ
def parse_redirect(env, connection):

    # parse OS environment variables
    if ADDRESS_KEY not in env or \
            PORT_KEY not in env:
        respond(NOT_FOUND_IDX, connection)

    # save the address used in the request for redirect
    if env[PORT_KEY] != '80':
        server_and_port = env[ADDRESS_KEY] + ':' + env[PORT_KEY]
    else:
        server_and_port = env[ADDRESS_KEY]
    address = "http://" + server_and_port + "/cgi-bin/ui"

    return server_and_port, address


# special return for debugging
def debug(data):
    print("Status: 200 OK\nContent-Type: text/plain\n")
    print(data)
    exit()
