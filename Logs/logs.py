from Logs import app
from Logs.models import Event, Data_Creation

def listEvents():
    events = app.session.query(Event).all()
    return events
    app.session.close()

def listDataCreations():
    data_creation = app.session.query(Data_Creation).all()
    return data_creation
    app.session.close()

def listLogsDICT():
    ret_list_1 = []
    el = listEvents()
    for l in el:
        logs_dict_1 = l.to_dictionary()
        ret_list_1.append(logs_dict_1)

    ret_list_2 = []
    dcl = listDataCreations()
    for l in dcl:
        logs_dict_2 = l.to_dictionary()
        ret_list_2.append(logs_dict_2)
    
    return [ret_list_1, ret_list_2]

def newEvent(IP , endpoint):
    lid = Event(IP = IP, endpoint = endpoint)
    try:
        app.session.add(lid)
        app.session.commit()
        print(lid.id)
        app.session.close()
        return lid.id
    except:
        return None

def newDataCreation(data_type , content, user):
    lid = Data_Creation(data_type = data_type, content = content, user=user)
    try:
        app.session.add(lid)
        app.session.commit()
        print(lid.id)
        app.session.close()
        return lid.id
    except:
        return None

   