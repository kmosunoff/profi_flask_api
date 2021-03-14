from sqlalchemy import Column, Integer, String
from database import Base


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String)
    content = Column(String)

    def __init__(self, title=None, content=None):
        self.title = title
        self.content = content

    def __repr__(self):
        return f"Note id={self.id}, title={self.title}, content={self.content}"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }
