from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, sessionmaker



my_engine =  create_engine('sqlite:///pkufoodlovermain.db', echo=False) 
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=my_engine)
session = Session()

    
def create_db():    
    Base.metadata.create_all(my_engine)



class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key = True)
    name = Column(String, unique=True)
    posts = relationship('Post', backref='account')
    comments = relationship('Comment', backref='account')



class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    caption = Column(String)
    comment_num = Column(Integer)
    like = Column(Integer)
    video = Column(Integer)
    posted_time = Column(DateTime)
    shortcode = Column(String)
    tag_num = Column(Integer)
    comments = relationship('Comment', backref='post')
    account_id = Column(Integer, ForeignKey('account.id'))

class User(Base):
    __tablename__ = 'user'

    id  = Column(Integer, primary_key = True)                    
    name = Column(String, unique=True)                           
    comments = relationship('Comment', backref='user')            
                                                                  

        

class Comment(Base):
    __tablename__ = 'comment'
    
    id = Column(Integer, primary_key=True)
    text = Column(String)
    commented_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    account_id = Column(Integer, ForeignKey('account.id'))

if __name__ == "__main__":
   pass

