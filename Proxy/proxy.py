from Proxy import app
from os import system
from Proxy.models import MicroServices
import requests


def verify_user(name, ist_id, page):
    if ist_id and name:
        admin = False
        try:
            response = requests.get("http://127.0.0.1:5004/API/user/"+ist_id+"/"+name+"/")
            # this means there was an error or he user doesn't exist if so user is automatically logout
            if response.status_code != 200:
                abort(500)
            if response.json().get("admin") == 1:
                admin = True
        except:
            # if there was a problem retrieving the user information user is automatically logout
            return "index.html", None, None, None, None
        # if everything  is okay goes to main page
        return page, admin, ist_id, name, True
    # if there is no user name or ist_id redirects to login
    else:
        return "index.html", None, None, None, None



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

def deleteService(id):
    app.session.query(MicroServices).filter_by(id=id).delete()
    app.session.commit()
    return {"delete":"success"}