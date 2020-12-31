from Proxy import app
from os import system


def check_port(port):
    command = "netstat -an | grep 127.0.0.1:" + \
        port + " | grep tcp | grep LISTEN > /dev/null"
    response = system(command)
    # and then check the response...
    if response != 0:
        portstatus = 0
    else:
        portstatus = 1

    return portstatus
