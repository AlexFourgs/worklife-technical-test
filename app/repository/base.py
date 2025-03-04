class BaseRepository:
    def __init__(self, model):
        self.model = model

    def _query(self, session, *_, **kwargs):
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        return session.query(self.model).filter(*filters)

    def get(self, session, *_, **kwargs):
        return self._query(session, **kwargs).one_or_none()

    def get_many(self, session, *_, **kwargs):
        return self._query(session, **kwargs).all()

    def create(self, session, obj_in):
        new_obj = self.model(**obj_in.model_dump())
        session.add(new_obj)
        session.flush()
        return {"id": new_obj.id}

    """
    def delete(self, session, *_, **kwargs):
        self._query(session, **kwargs).delete()
    """
