from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqladmin import ModelView

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, nullable=False)
    name = Column(String(55), nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default='user')
    picture_url = Column(String(600), nullable=True)
    logins = Column(Integer, default=0)
    last_ip = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_activity_at = Column(DateTime, nullable=True, onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, name={self.name})>"

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_ru = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    articles_length = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    def __repr__(self):
        return f"<Category(id={self.id}, category={self.name_en})>"
    
    

class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    preview_url = Column(String, nullable=False)
    title_ru = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    content_ru = Column(String, nullable=False)
    content_en = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False, onupdate=func.now())
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    
    user = relationship("User")
    
    def __repr(self):
        return f"<Blog(id={self.id}, title={self.title_en}, category={self.category_id})>"



class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]
    
    
class CategoriesAdmin(ModelView, model=Categories):
    column_list = [Categories.id, Categories.name_en]
    
class BlogAdmin(ModelView, model=Blog):
    column_list = [Blog.id, Blog.title_en, Blog.category_id]
