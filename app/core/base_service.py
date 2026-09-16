class BaseService:

    repository = None

    @classmethod
    def get_all(cls):
        return cls.repository.get_all()

    @classmethod
    def get_by_id(cls, object_id):
        return cls.repository.get_by_id(object_id)

    @classmethod
    def create(cls,**kwargs):

        return cls.repository.create(**kwargs)

    @classmethod
    def update(cls, instance, **kwargs):
        return cls.repository.update(instance,**kwargs)

    
    @classmethod
    def delete(cls,instance):
        return cls.repository.delete(instance)

    
    