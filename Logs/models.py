from Logs import app
from sqlalchemy import Column, Integer, String, DateTime, PickleType
from sqlalchemy.types import Date
from Logs.database import Base
import datetime

class Event(Base):
    __tablename__ = 'Events'
    id = Column(Integer, primary_key=True)
    IP = Column(String(128))
    endpoint = Column(String(256))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Log event (id=%d IP=%s, endpoint=%s, timestamp=%s>" % (
                                self.id, self.IP, self.endpoint,  self.timestamp)
    def to_dictionary(self):
        return {"log_id": self.id, "IP": self.IP, "endpoint": self.endpoint, "timestamp": self.timestamp}

class Data_Creation(Base):
    __tablename__ = 'Data_Creation'
    id = Column(Integer, primary_key=True)
    data_type = Column(String(128))
    content = Column(PickleType)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user = Column(String(128))

    def __repr__(self):
        return "<Log event (id=%d type=%s, content=%s, timestamp=%s, user=%s>" % (
                                self.id, self.data_type, self.content,  self.timestamp, self.user)
    def to_dictionary(self):
        return {"log_id": self.id, "type": self.data_type, "content": self.content, "timestamp": self.timestamp, "user": self.user}