from UserManager import app
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from UserManager.database import Base

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ist_id = Column(String(15), unique=True)
    name = Column(String(128))
    admin = Column(Integer, default = 0)
    
    def __repr__(self):
        return "<YouTubeVideo (id=%d ist_id=%s, name=%s, admin=%s>" % (
                                self.id, self.ist_id, self.name,  self.admin)
    def to_dictionary(self):
        return {"user_id": self.id, "ist_id": self.ist_id, "name": self.name, "admin": self.admin}