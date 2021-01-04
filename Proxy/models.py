from Proxy import app
from sqlalchemy import Column, Integer, String
from Proxy.database import Base

class MicroServices(Base):
    __tablename__ = 'microservices'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    port = Column(String(64))
    endpoint = Column(String(256))

    def __repr__(self):
        return "<Microservice (id=%d, port=%s, name=%s, endpoint=%s>" % (
                                self.id, self.port, self.name, self.endpoint)
    def to_dictionary(self):
        return {"id": self.id, "port": self.port, "name": self.name, "endpoint": self.endpoint}
