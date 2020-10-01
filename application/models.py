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

    # first_name  = Column(String(30), nullable=False)
    # last_name   = Column(String(30), nullable=False)

    date_joined = Column(DateTime,   default=func.now())
    last_login  = Column(DateTime,   nullable=True)

    groups      = relationship("UserGroup", back_populates="user")
    datasets    = relationship("DataSet",   back_populates="user")


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

    id          = Column(Integer,    primary_key=True)
    title       = Column(String(80), nullable=False)
    description = Column(Text)
    owner_id    = Column(Integer,  ForeignKey("user.id"), nullable=False)
    is_public   = Column(Boolean,  default=True)
    date_load   = Column(DateTime, default=func.now())
    rating      = Column(Float)
    meta_id     = Column(Integer, ForeignKey("dataset_meta.id"), nullable=False, unique=True)

    user = relationship("User", back_populates="datasets")
    tags = relationship("DataSetTag" , back_populates="dataset")
    dataset_meta = relationship("DataSetMeta", back_populates="dataset")

    

class DataSetMeta(Base):
    __tablename__ = "dataset_meta"

    id = Column(Integer, primary_key=True)
    path = Column(String(200), nullable=False)
    size = Column(Integer)
    type = Column(Enum("other", "csv", "json", name="dataset_enum", create_type=False))

    dataset = relationship("DataSet", back_populates="dataset_meta")


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
