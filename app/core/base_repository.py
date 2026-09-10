from app.core.extensions import db



class BaseRepository:


    model = None

    @classmethod
    def get_all(cls):

        return cls.model.query.all()


    @classmethod
    def get_by_id(cls, object_id):

        return db.session.get(cls.model, object_id)

    @classmethod
    def add(cls,instance , commit=True):
        db.session.add(instance)
        if commit:
            db.session.commit()

        return instance
    
    @classmethod
    def update(cls, instance, commit=True, **kwargs):
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        if commit:
            db.session.commit()

        return instance

    @classmethod
    def delete(cls,instance, commit=True):
        db.session.delete(instance)
        if commit:
            db.session.commit()

        return instance

    @classmethod
    def count(cls):
        return cls.model.query.count()

    @classmethod
    def exists(cls, **kwargs):
        return (
            cls.model.query.filter_by((**kwargs).first() is not None)
        )

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.model.query.filter_by(**kwargs)

    @classmethod
    def first(cls,**kwargs):
        return (
            cls.model.query.filter_by(**kwargs).first()
        )

    @classmethod
    def save(cls):
        db.session.commit()

    @classmethod
    def rollback(cls):
        db.session.rollback()



