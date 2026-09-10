from datetime import datetime, timezone
from sqlalchemy import or_
from app.core.extensions import db

def utc_now():

    return datetime.now(timezone.utc)

class CoreMixin:

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False
    )


class CRUDMixin:

    @classmethod
    def create(cls, commit=True, **kwargs):

        instance = cls(**kwargs)

        db.session.add(instance)

        if commit:
            db.session.commit()

        return instance
    
    def update(self, commit=True, **kwargs):

        for attr, value in kwargs.items():

            if hasattr(self, attr):
                setattr(self, attr, value)

        if commit:
            db.session.commit()

        return self

    def delete(self,commit=True):
        db.session.delete(self)

        if commit:
            db.session.commit()

        return self

    @classmethod
    def all(cls):
        return cls.qeury.all()
    
    @classmethod
    def get_by_id(cls, object_id):

        return db.session.get(cls, object_id)
    
    @classmethod
    def exists(cls,**kwargs):
        return (
            cls.query.filter_by(**kwargs).first() is not None
        )
    
    @classmethod
    def count(cls,**kwargs):

        query = cls.query

        for key,value in kwargs.items():

            if hasattr(cls,key):
                query = query.filter(
                    getattr(cls, key) == value
                )
        
        return query.count()


class SoftDeleteMixin:

    is_deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    deleted_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True
    )

    def soft_delete(self, commit=True):

        self.is_deleted = True
        self.deleted_at = utc_now()

        if commit:
            db.session.commit()

        return self

    def restore(self,commit=True):

        self.is_deleted = False
        self.deleted_at = None

        if commit:
            db.session.commit()

        return self
    
    @classmethod
    def active(cls):
        return cls.query.filter_by(
            is_deleted=False
        )
    

    @classmethod
    def deleted(cls):

        return cls.query.filter_by(
            is_deleted=True
        )


class SearchMixin:

    @classmethod
    def search(cls, keyword,*fields):

        if not keyword or not fields:
            return cls.query
        
        filters = []

        for field in  fields:
            if hasattr(cls,field):
                column = getattr(cls,field)

                filters.append(
                    column.ilike(f'%{keyword}%')
                )

        if not filters:
            return cls.query
        
        return cls.query.filter(
            or_(
                *filters
            )
        )
        
class SerializerMixin:

    def to_dict(
            self,
            exclude=None
    )

    exclude = set(exclude or [])

    data = {}

    for column in self.__table__.columns:
        for column.name in exclude:
            continue

        value = getattr(
            self, column.name
        )

        if isinstance(value, datetime):
            value = value.isoformat()

        data[column.name] = value

        return data
    


class BaseModel(
    CoreMixin,
    CRUDMixin,
    SoftDeleteMixin,
    SearchMixin,
    SerializerMixin,
    db.Model
):
    __abstract__ =  True


    






