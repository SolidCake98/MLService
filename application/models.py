from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from application.database import Base
import uuid

CASCADE_DELETE = "all, delete"


class User(Base):
    __tablename__ = "user"

    id          = Column(Integer,    primary_key=True)
    username    = Column(String(30), unique=True, nullable=False)
    password    = Column(String(256),nullable=False)
    email       = Column(String(30), unique=True, nullable=False)

    date_joined = Column(DateTime,   default=func.now())
    last_login  = Column(DateTime,   nullable=True)

    groups         = relationship("UserGroup", back_populates="user", cascade=CASCADE_DELETE)
    user_ratings   = relationship("UserRating", back_populates="user", cascade=CASCADE_DELETE)
    datasets       = relationship("DataSet",   back_populates="user", cascade=CASCADE_DELETE)
    dataset_tables = relationship("DataSetTable",   back_populates="user", cascade=CASCADE_DELETE)
    data_charts    = relationship("DataChart",   back_populates="user", cascade=CASCADE_DELETE)


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
    user_ratings = relationship("UserRating", back_populates="dataset", cascade=CASCADE_DELETE)

    tags = relationship("DataSetTag" , back_populates="dataset", cascade=CASCADE_DELETE)
    dataset_meta = relationship("DataSetMeta", back_populates="dataset", cascade=CASCADE_DELETE, lazy='subquery')
    file_types = relationship("DataSetType", back_populates="dataset", cascade=CASCADE_DELETE)

    dataset_tables = relationship("DataSetTable", back_populates="dataset", cascade=CASCADE_DELETE)

    def __repr__(self):
        return str(self.id)


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

    def __repr__(self):
        return str(self.tag_name)


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
    user_id      = Column(Integer,  ForeignKey("user.id"))
    rating       = Column(Float)
    is_favoritre = Column(Boolean, default=False)
    commenatary  = Column(Text)
    create_time  = Column(DateTime,  default=func.now())

    user = relationship("User", back_populates="user_ratings")
    dataset = relationship("DataSet", back_populates="user_ratings")


class UserDataset(Base):
    """
    It's a view
    """
    __tablename__ = "user_dataset"

    id        = Column(Integer, primary_key=True)
    username  = Column(String)
    name      = Column(String)
    title     = Column(String)
    size      = Column(Integer)
    size_name = Column(String)


class CountDataset(Base):
    """
    It's a view
    """
    __tablename__ = "count_dataset"

    id       =  Column(Integer, primary_key=True)
    username = Column(String)
    count    = Column(Integer)
    avg      = Column(Float)


class RatingDataSetLastMonth(Base):
    """
    It's a view
    """
    __tablename__ = "rating_last_month"

    id    = Column(Integer, primary_key=True)
    name  = Column(String)
    title = Column(String)
    count = Column(Integer)
    avg   = Column(Float)


class DataSetTable(Base):

    __tablename__ = "dataset_table"

    id           = Column(Integer, primary_key=True)
    name         = Column(String)
    dataset_id   = Column(Integer, ForeignKey("dataset.id"), nullable=False)
    owner_id     = Column(Integer, ForeignKey("user.id"), nullable=False)
    dataset_file = Column(String(1000), nullable=False)
    is_public    = Column(Boolean,  default=True)
    date_load    = Column(DateTime, default=func.now())
    date_changed = Column(DateTime)

    dataset = relationship("DataSet", back_populates="dataset_tables")
    user = relationship("User", back_populates="dataset_tables")
    dataset_column_sources = relationship("DataSetColumnSource", back_populates="dataset_table")


class Aggregation(Base):
    __tablename__ = "aggregation"

    id   = Column(Integer, primary_key=True)
    name = Column(String)

    data_type_ags = relationship("DataTypeAggregation", back_populates="aggregation")


class DataType(Base):
    __tablename__ = "data_type"

    id   = Column(Integer, primary_key=True)
    name = Column(String)

    data_type_ags = relationship("DataTypeAggregation", back_populates="data_type")


class DataTypeAggregation(Base):
    __tablename__ = "data_type_aggregation"

    id             = Column(Integer, primary_key=True)
    aggregation_id = Column(ForeignKey("aggregation.id"), nullable=False)
    data_type_id   = Column(ForeignKey("data_type.id"), nullable=False)

    aggregation = relationship("Aggregation", back_populates="data_type_ags")
    data_type = relationship("DataType", back_populates="data_type_ags")

    dataset_column_sources = relationship("DataSetColumnSource", back_populates="data_type_aggregation")
    dataset_column_versioned = relationship("DataSetColumnVersioned", back_populates="data_type_aggregation")
 

class DataSetColumnSource(Base):

    __tablename__ = "dataset_column_source"

    id                       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tittle                   = Column(String)
    dataset_table_id         = Column(Integer, ForeignKey("dataset_table.id"), nullable=False)
    data_type_aggregation_id = Column(Integer, ForeignKey("data_type_aggregation.id"), nullable=False)
    index                    = Column(Integer)
    
    dataset_table = relationship("DataSetTable", back_populates="dataset_column_sources")
    data_type_aggregation = relationship("DataTypeAggregation", back_populates="dataset_column_sources")
    dataset_column_versioned = relationship("DataSetColumnVersioned", back_populates="dataset_column_sources")


class DataSetColumnVersioned(Base):
    __tablename__ = "dataset_column_versioned"

    id                       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tittle                   = Column(String)
    dataset_column_source_id = Column(UUID(as_uuid=True), ForeignKey("dataset_column_source.id"), nullable=False)
    data_type_aggregation_id = Column(Integer, ForeignKey("data_type_aggregation.id"), nullable=False)
    index                    = Column(Integer)

    data_type_aggregation = relationship("DataTypeAggregation", back_populates="dataset_column_versioned")
    dataset_column_sources = relationship("DataSetColumnSource", back_populates="dataset_column_versioned")


class ChartType(Base):
    __tablename__ = "chart_type"

    id   = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    data_charts = relationship("DataChart", back_populates="chart_type")


class DataChart(Base):
    __tablename__ = "data_chart"

    id   = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    chart_type_id    = Column(Integer, ForeignKey("chart_type.id"), nullable=False)
    dataset_table_id = Column(Integer, ForeignKey("dataset_table.id"), nullable=False)
    owner_id     = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="data_charts")
    chart_type = relationship("ChartType", back_populates="data_charts")

    x_dataset_column_v_id = Column(UUID(as_uuid=True), ForeignKey("dataset_column_versioned.id"))
    y_dataset_column_v_id = Column(UUID(as_uuid=True), ForeignKey("dataset_column_versioned.id"))

    x_dataset_column_v = relationship("DataSetColumnVersioned", foreign_keys=[x_dataset_column_v_id])
    y_dataset_column_v = relationship("DataSetColumnVersioned", foreign_keys=[y_dataset_column_v_id])


