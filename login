#! /usr/bin/python3

"""
Phillip Benoit
CSC346
Project 7 & 8 (FlyRC)
Login simulator for user interface
"""

import random
import cgi
import os
import MySQLdb
from lib import passwd, http_response, strings

connection = MySQLdb.connect(host=passwd.SQL_HOST,
                             user=passwd.SQL_USER,
                             passwd=passwd.SQL_PASS,
                             db=passwd.SQL_DBID)

INSERT_SESSIONS = "INSERT INTO sessions (session_id, user) VALUES (%s, %s);"


def main():

    server_and_port, address = http_response.parse_redirect(os.environ, connection)

    # get arguments
    args = cgi.FieldStorage()

    # make sure user has been passed
    if strings.USER_URLKEY not in args:
        user = ''
        http_response.respond(http_response.REDIRECT_IDX, connection, address)

    # get user
    else:
        user = args[strings.USER_URLKEY].value

    # try to get a session id from the table
    session = strings.get_session_id(user, connection)

    # insert new session
    if session == '':
        session = "%064x" % random.randint(0, 16 ** 64)

        cursor = connection.cursor()
        cursor.execute(INSERT_SESSIONS, (session, user))
        connection.commit()
        cursor.close()

    # redirect and set the cookie
    http_response.redirect_set_cookie(address, session, connection)


main()
