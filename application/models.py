from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean, Float, Enum
from passlib.hash import pbkdf2_sha256 as sha256

from application.database import Base

class User(Base):
    __tablename__ = "user"

    id          = Column(Integer,    primary_key=True)
    username    = Column(String(30), unique=True, nullable=False)
    password    = Column(String(256),nullable=False)
    email       = Column(String(30), unique=True, nullable=False)

    date_joined = Column(DateTime,   default=func.now())
    last_login  = Column(DateTime,   nullable=True)

    groups       = relationship("UserGroup", back_populates="user", cascade="all, delete-orphan, delete")
    user_ratings = relationship("UserRating", back_populates="user", cascade="all, delete")
    datasets     = relationship("DataSet",   back_populates="user", cascade="all, delete-orphan, delete")


class Group(Base):
    __tablename__ = "group"

    id    = Column(Integer, primary_key=True)
    name  = Column(String(20))
    users = relationship("UserGroup", back_populates="group")


class UserGroup(Base):
    __tablename__ = "user_group"

    id       = Column(Integer, primary_key=True)
    user_id  = Column(Integer, ForeignKey("user.id"))
    group_id = Column(Integer, ForeignKey("group.id"))

    user     = relationship("User",  back_populates="groups")
    group    = relationship("Group", back_populates="users")
    

class DataSet(Base):
    __tablename__ = "dataset"

    id          = Column(Integer,     primary_key=True)
    name        = Column(String(80),  nullable=False)
    title       = Column(String(100), nullable=False)
    description = Column(Text)
    owner_id    = Column(Integer,  ForeignKey("user.id"), nullable=False)
    is_public   = Column(Boolean,  default=True)
    date_load   = Column(DateTime, default=func.now())
    rating      = Column(Float)
    meta_id     = Column(Integer, ForeignKey("dataset_meta.id"), nullable=False, unique=True)
    is_loaded   = Column(Boolean, default=False)

    user = relationship("User", back_populates="datasets")
    user_ratings = relationship("UserRating", back_populates="dataset", cascade="all, delete")

    tags = relationship("DataSetTag" , back_populates="dataset", cascade="all, delete, delete-orphan")
    dataset_meta = relationship("DataSetMeta", back_populates="dataset", cascade="all, delete", lazy='subquery')
    file_types = relationship("DataSetType", back_populates="dataset", cascade="all, delete-orphan, delete")


class DataSetMeta(Base):
    __tablename__ = "dataset_meta"

    id = Column(Integer, primary_key=True)
    path = Column(String(200), nullable=False)
    size = Column(Integer)
    size_name = Column(String(20))

    dataset = relationship("DataSet", back_populates="dataset_meta")


class FileType(Base):
    __tablename__ = "file_type"

    id        = Column(Integer, primary_key=True)
    type_name = Column(String(30))

    datasets = relationship("DataSetType", back_populates="file_type")



class DataSetType(Base):
    __tablename__ = "dataset_type"

    id           = Column(Integer, primary_key=True)
    dataset_id   = Column(Integer,  ForeignKey("dataset.id"), nullable=False)
    file_type_id = Column(Integer,  ForeignKey("file_type.id"), nullable=False)

    dataset      = relationship("DataSet",  back_populates="file_types")
    file_type    = relationship("FileType", back_populates="datasets")


class Tag(Base):
    __tablename__ = "tag"

    id       = Column(Integer, primary_key=True)
    tag_name = Column(String(30))

    datasets = relationship("DataSetTag" , back_populates="tag")


class DataSetTag(Base):
    __tablename__ = "dataset_tag"

    id          = Column(Integer, primary_key=True)
    dataset_id  = Column(Integer, ForeignKey("dataset.id"))
    tag_id      = Column(Integer, ForeignKey("tag.id"))

    dataset     = relationship("DataSet",  back_populates="tags")
    tag         = relationship("Tag", back_populates="datasets")


class UserRating(Base):
    __tablename__ = "user_rating"

    id           = Column(Integer, primary_key=True)
    dataset_id   = Column(Integer, ForeignKey("dataset.id"), nullable=False)
    user_id      = Column(Integer,  ForeignKey("user.id"), nullable=False)
    rating       = Column(Float)
    is_favoritre = Column(Boolean, default=False)
    commenatary  = Column(Text)

    user = relationship("User", back_populates="user_ratings")
    dataset = relationship("DataSet", back_populates="user_ratings")


class UserDataset(Base):
    """
    It's a view
    """
    __tablename__ = "user_dataset"

    id       =  Column(Integer, primary_key=True)
    username = Column(String)
    name     = Column(String)
    title    = Column(String)


class CountDataset(Base):
    """
    It's a view
    """
    __tablename__ = "count_dataset"

    id       =  Column(Integer, primary_key=True)
    username = Column(String)
    count    = Column(Integer)
    avg      = Column(Float)