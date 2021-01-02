from Stats import app
from Stats.models import User_Stats

def listUser_Stats():
    user_stats = app.session.query(User_Stats).all()
    return user_stats
    app.session.close()

def listStatsDICT():
    ret_list = []
    lu = listUser_Stats()
    for u in lu:
        stats_dict_1 = u.to_dictionary()
        ret_list.append(stats_dict_1)    
    return ret_list

def newUser_Stats(user):
    stats = app.session.query(User_Stats).filter_by(user=user).first()
    if stats is not None:
        return None
    new_user = User_Stats(user=user)
    try:
        app.session.add(new_user)
        app.session.commit()
        print(new_user.id)
        app.session.close()
        return new_user.id
    except:
        return None

def getUser_Stats(id):
    try:
        v = app.session.query(User_Stats).filter(User_Stats.id == id).first()
    except:
        abort(500)
    app.session.close()
    return v


def getUser_StatsDICT(id):
    return getUser_Stats(id).to_dictionary()

def updateUser_Stats(user, data_stats):
    user_stats = getUser_Stats(id)
    print(user_stats)
    print(user_stats.data_stats +"\n\n\n")
    user_stats.data_stats += 1
    n = user_stats.data_stats
    app.session.commit()
    app.session.close()    
    return user_stats
