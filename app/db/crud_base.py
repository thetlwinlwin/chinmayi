from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core import exceptions as exc
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType, db_session: Session):
        self.model = model
        self._db_session = db_session

    def create(
        self,
        input_obj: CreateSchemaType,
    ) -> ModelType | None:
        try:
            stmt = insert(self.model).values(input_obj.dict())
            self._db_session.execute(stmt)
            self._db_session.commit()
        except SQLAlchemyError:
            raise exc.BadRequest()

    def update_by_id(
        self,
        id_to_update: int,
        new_vals: UpdateSchemaType,
    ) -> ModelType | None:
        try:
            stmt = (
                update(self.model)
                .where(self.model.id == id_to_update)
                .values(new_vals.dict(exclude_unset=True))
            )
            self._db_session.execute(stmt)
            self._db_session.commit()

        except SQLAlchemyError:
            raise exc.BadRequest()

    def delete_by_id(
        self,
        id: int,
    ) -> None:
        try:
            obj_to_del = self._db_session.get(self.model, id)
            if obj_to_del is None:
                raise exc.NotFound()

            self._db_session.delete(obj_to_del)
            self._db_session.commit()

        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def get_by_id(
        self,
        id: int,
    ) -> ModelType | None:
        try:
            obj = self._db_session.get(self.model, id)
            if obj is None:
                raise exc.NotFound()
            return obj

        except SQLAlchemyError as e:
            raise exc.BadRequest()

    def get_all(
        self,
    ) -> list[ModelType]:
        try:
            results = self._db_session.scalars(select(self.model)).all()
            print(f"result is {results}")
            if results is None:
                raise exc.NotFound()
            return results

        except SQLAlchemyError as e:
            print(e)
            raise exc.BadRequest()
