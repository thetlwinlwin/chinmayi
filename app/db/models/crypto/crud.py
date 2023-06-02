from fastapi import Depends
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core import exceptions as exc
from app.db.crud_base import CRUDBase
from app.db.get_session import get_db
from app.schema import crypto_schema

from .crypto_model import Crypto


class CryptoCrud(CRUDBase[Crypto, crypto_schema.CryptoDbIn, crypto_schema.CryptoDbIn]):
    def __init__(self, model, db_session):
        super().__init__(model, db_session)

    def save_all(self, input_objs: list[crypto_schema.CryptoDbIn]) -> None:
        input_objs = list(map(lambda x: x.dict(), input_objs))
        try:
            stmt = insert(self.model).values(input_objs)
            print(stmt)
            self._db_session.execute(stmt)
            self._db_session.commit()
        except SQLAlchemyError as e:
            raise exc.BadRequest()


def get_crypto_crud(db_session: Session = Depends(get_db)) -> CryptoCrud:
    return CryptoCrud(model=Crypto, db_session=db_session)
