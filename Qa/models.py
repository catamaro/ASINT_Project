from Qa import app
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.types import Date
from Qa.database import Base

class Question(Base):
    __tablename__ = 'Question'
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer)
    curr_time = Column(Float)
    user = Column(String(256))
    text = Column(String)
    def __repr__(self):
        return "<Question (id=%d video_id=%d, current_time=%f, user=%s, text=%s>" % (
                                self.id, self.video_id, self.curr_time,  self.user, self.text)
    def to_dictionary(self):
        return {"Question": self.id, "video_id": self.video_id, "curr_time": self.curr_time, "user": self.user, "text": self.text}

class Answer(Base):
    __tablename__ = 'Answer'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)#, ForeignKey('question.id'))
    a_user = Column(String(256))
    a_text = Column(String)
    def __repr__(self):
        return "<Answer (id=%d question_id=%d, a_user=%s, a_text=%s>" % (
                                self.id, self.question_id, self.a_user, self.a_text)
    def to_dictionary(self):
        return {"Answer": self.id, "question_id": self.question_id, "a_user": self.a_user, "a_text": self.a_text}