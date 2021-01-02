from Videos import app
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from Videos.database import Base

class YTVideo(Base):
    __tablename__ = 'YTVideo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(256), unique=True)
    description = Column(String(128))
    views = Column(Integer, default = 0)
    ist_id = Column(String(128))
    name = Column(String(128))
    
    def __repr__(self):
        return "<YouTubeVideo (id=%d Description=%s, URL=%s, Views=%s, ist_id=%s, name=%s>" % (
                                self.id, self.description, self.url,  self.views, self.ist_id, self.name)
    def to_dictionary(self):
        return {"video_id": self.id, "description": self.description, "url": self.url, "views": self.views, "ist_id": self.ist_id, "name": self.name}