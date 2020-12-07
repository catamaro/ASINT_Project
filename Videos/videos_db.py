from Videos import app
from Videos.models import YTVideo

def listVideos():
    return app.session.query(YTVideo).all()
    app.session.close()

def listVideosDICT():
    ret_list = []
    lv = listVideos()
    for v in lv:
        vd = v.to_dictionary()
        del(vd["url"])
        del(vd["views"])
        ret_list.append(vd)
    return ret_list

def getVideo(id):
     v =  app.session.query(YTVideo).filter(YTVideo.id==id).first()
     app.session.close()
     return v

def getVideoDICT(id):
    return getVideo(id).to_dictionary()

def newVideoView(id):
    b = app.session.query(YTVideo).filter(YTVideo.id==id).first()
    b.views+=1
    n = b.views
    app.session.commit()
    app.session.close()
    return n


def newVideo(description , url):
    vid = YTVideo(description = description, url = url)
    try:
        app.session.add(vid)
        app.session.commit()
        print(vid.id)
        app.session.close()
        return vid.id
    except:
        return None
