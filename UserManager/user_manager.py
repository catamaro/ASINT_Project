from UserManager import app, fenix_blueprint
from UserManager.models import User

def newUser(ist_id, name):
    user = app.session.query(User).filter_by(ist_id=ist_id).first()
    if user is not None:
        return None
    
    uid = User(ist_id=ist_id, name=name)
    try:
        app.session.add(uid)
        app.session.commit()
        u_id = uid.u_id
        app.session.close()
        return u_id
    except Exception as e:
        print(e)
        return None

