from fastapi import Depends
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core import exceptions as exc
from app.db.crud_base import CRUDBase
from app.db.get_session import get_db
from app.schema import lead_schema

from .lead import Lead


class LeadCrud(CRUDBase[Lead, lead_schema.LeadCreate, lead_schema.LeadUpdate]):
    def __init__(self, model, db_session):
        super().__init__(model, db_session)

    def save_all(self, input_objs: list[lead_schema.LeadCreate]) -> None:
        input_objs = list(map(lambda x: x.dict(), input_objs))
        try:
            self._db_session.execute(insert(self.model).values(input_objs))
            self._db_session.commit()
        except SQLAlchemyError:
            raise exc.BadRequest()


def get_lead_crud(db_session: Session = Depends(get_db)):
    return LeadCrud(model=Lead, db_session=db_session)
