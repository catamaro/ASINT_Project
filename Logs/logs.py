from Logs import app
from Logs.models import Event, Data_Creation

def listLogs():
    events = app.session.query(Event).all()
    data_creation = app.session.query(Data_Creation).all()

    #data = [events, data_creation]
    return events
    app.session.close()

def listLogsDICT():
    ret_list = []
    ll = listLogs()
    for l in ll:
        logs_dict = l.to_dictionary()
        ret_list.append(logs_dict)
    
    return ret_list

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

   