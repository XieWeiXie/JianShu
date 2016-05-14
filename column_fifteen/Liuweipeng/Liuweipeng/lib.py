from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True)
    Title = Column(String)
    Time = Column(String)
    Content = Column(String)
    Url = Column(String)
