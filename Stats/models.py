from Stats import app
from sqlalchemy import Column, Integer, String, DateTime, PickleType
from sqlalchemy.types import Date
from Stats.database import Base
import datetime

class User_Stats(Base):
    __tablename__ = 'User_Stats'
    id = Column(Integer, primary_key=True)
    user = Column(String(128))
    n_videos = Column(Integer, default = 0)
    n_views = Column(Integer, default = 0)
    n_question = Column(Integer, default = 0)
    n_answers = Column(Integer, default = 0)

    def __repr__(self):
        return "<Stats (id=%d user=%s n_videos=%d, n_views=%d, n_question=%d, n_answers=%d>" % (
                                self.id, self.user, self.n_videos, self.n_views, self.n_question,  self.n_answers)
    def to_dictionary(self):
        return {"id": self.id, "user": self.user, "type": self.n_videos, "n_views": self.n_views, "n_question": self.n_question, "n_answers": self.n_answers}