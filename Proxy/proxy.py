from Proxy import app
from os import system
from Proxy.models import MicroServices


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

def listServices():
    sv = app.session.query(MicroServices).all()
    app.session.close()
    return sv


def listServicesDICT():
    ret_list = []
    ls = listServices()
    for s in ls:
        sv = s.to_dictionary()
        ret_list.append(sv)
    return ret_list
