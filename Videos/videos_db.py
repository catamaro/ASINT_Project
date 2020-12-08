from Videos import app
from Videos.models import YTVideo


def listVideos():
    lv = app.session.query(YTVideo).all()
    app.session.close()
    return lv


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
    try:
        v = app.session.query(YTVideo).filter(YTVideo.id == id).first()
    except:
        abort(500)
    app.session.close()
    return v


def getVideoDICT(id):
    return getVideo(id).to_dictionary()


def newVideoView(id):
    b = app.session.query(YTVideo).filter(YTVideo.id == id).first()
    b.views += 1
    n = b.views
    app.session.commit()
    app.session.close()
    return n


def newVideo(description, url):
    video = YTVideo.query.filter_by(url=url).first()
    if video is not None:
        raise ValidationError('Video already in database.')
        return None

    vid = YTVideo(description=description, url=url)
    try:
        app.session.add(vid)
        app.session.commit()
        #print(vid.id)
        #app.session.close()
        return vid.id
    except Exception as e:
        print(e)
        return None
