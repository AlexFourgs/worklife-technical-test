from app.model import TeamModel
from app.repository.base import BaseRepository


class _TeamRepository(BaseRepository):
    def get_by_id(self, session, team_id):
        return session.query(self.model).filter(self.model.id == team_id)

    def get_by_name(self, session, team_name):
        return session.query(self.model).filter(self.model.name == team_name)


TeamRepository = _TeamRepository(model=TeamModel)
