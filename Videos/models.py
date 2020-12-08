from Videos import app
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from Videos.database import Base

class YTVideo(Base):
    __tablename__ = 'YTVideo'
    id = Column(Integer, primary_key=True)
    url = Column(String(256), unique=True)
    description = Column(String(128))
    views = Column(Integer, default = 0)
    
    def __repr__(self):
        return "<YouTubeVideo (id=%d Description=%s, URL=%s, Views=%s>" % (
                                self.id, self.description, self.url,  self.views)
    def to_dictionary(self):
        return {"video_id": self.id, "description": self.description, "url": self.url, "views": self.views}