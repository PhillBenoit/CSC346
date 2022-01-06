import MySQLdb

# dictionary keys for os.environ
RM_KEY = 'REQUEST_METHOD'
PATH_KEY = 'PATH_INFO'
COOKIE_KEY = "HTTP_COOKIE"

# field keys
ID_FKEY = 'id'
OWNER_FKEY = 'owner'
DESC_FKEY = 'description'
EC2ID_FKEY = 'ec2id'
READY_FKEY = 'ready'
U1PW_FKEY = 'user1pw'
U2PW_FKEY = 'user2pw'
ADDR_FKEY = 'ip address'

# URL keys
USER_URLKEY = 'user'
DESC_URLKEY = 'desc'

# table key
SERVERS_TKEY = 'servers'


# get user from sessions table using session id
def get_user(session_id, connection):
    cursor = connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT user FROM sessions WHERE session_id = %s;", (session_id,))
    user = cursor.fetchall()
    cursor.close()
    if user:
        return user[0]['user']
    else:
        return ""


# get session from sessions table using user id
def get_session_id(user, connection):
    cursor = connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT session_id FROM sessions WHERE user = %s;", (user,))
    session = cursor.fetchall()
    cursor.close()
    if session:
        return session[0]['session_id']
    else:
        return ""


# read cookie from os.environ
def read_id(env):
    if COOKIE_KEY not in env:
        return ""
    else:
        return env[COOKIE_KEY].replace('session_id=', '')


def parse_user(env, connection):

    # get session ID from cookie
    session = read_id(env)

    # if no session exists, return empty
    if session == "":
        return session

    # get user from session id, returns empty if user was not found
    return get_user(session, connection)


# EC2 starting script
USERDATA = '''
#! /bin/bash
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo docker run --detach --name ircd inspircd/inspircd-docker
sudo docker run --detach --name thelounge -p 80:9000 thelounge/thelounge:latest
wget -P /home/ec2-user http://xxxx/config.js
sudo docker cp /home/ec2-user/config.js thelounge:/var/opt/thelounge
sudo docker restart thelounge
'''