from abc import ABC
from application.database import db_session, Base


class AbstractFacade(ABC):

    def __init__(self, cls):
        self.cls = cls

    def create(self, entity: Base):
        db_session.add(entity)
        db_session.commit()
        db_session.refresh(entity)

    def change(self, entity: Base):
        db_session.merge(entity)
        db_session.commit()
        db_session.refresh(entity)
    
    def remove(self, entity: Base):
        db_session.delete(entity)
        db_session.commit()

    def get_entity(self, id: int):
        return self.cls.query.filter_by(id=id).first()

    def get_all(self):
        return self.cls.query.order_by(self.cls.id).all()

    def get_in_range(self, offset: int = 0, limit: int = 20):
        return self.cls.query.offset(offset).limit(limit).all()