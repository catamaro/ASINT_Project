from UserManager import app, fenix_blueprint
from UserManager.models import User


def newUser(ist_id, name):
    user = app.session.query(User).filter_by(ist_id=ist_id).first()
    if user is not None:
        user.auth = True
        return None
    
    uid = User(ist_id=ist_id, name=name, auth=True)
    try:
        app.session.add(uid)
        app.session.commit()
        u_id = uid.id
        app.session.close()
        return u_id
    except Exception as e:
        print(e)
        return None

def getUser(ist_id, name):
    name.replace("%20", " ")
    try:
        v = app.session.query(User).filter_by(ist_id=ist_id, name=name).first()
    except:
        abort(500)
    app.session.close()
    return v

def getUserDICT(ist_id, name):
    return getUser(ist_id, name).to_dictionary()
