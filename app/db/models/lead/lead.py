from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_work = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"
