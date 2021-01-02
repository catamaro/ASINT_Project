from Stats import app
from Stats.models import User_Stats

def listUser_Stats():
    user_stats = app.session.query(User_Stats).all()
    return user_stats

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
    print("am I here")
    new_user = User_Stats(user=user)
    try:
        app.session.add(new_user)
        app.session.commit()
        print(new_user.id)
        app.session.close()
        return new_user.id
    except:
        return None

def getUser_Stats(user):
    try:
        v = app.session.query(User_Stats).filter(User_Stats.user == user).first()
    except:
        abort(500)
    app.session.close()
    return v


def getUser_StatsDICT(id):
    return getUser_Stats(id).to_dictionary()

def updateUser_Stats(user, data_stats):
    user_stats = app.session.query(User_Stats).filter(User_Stats.user == user).first()
    print(user_stats)
    if data_stats == "video":
        user_stats.n_videos += 1
        n = user_stats.n_videos
    elif data_stats == "view":
        user_stats.n_views += 1
        n = user_stats.n_views
    elif data_stats == "question":
        user_stats.n_question += 1
        n = user_stats.n_question
    elif data_stats == "answer":
        user_stats.n_answers += 1
        n = user_stats.n_answers    
    app.session.commit()
    app.session.close()    
    return n
