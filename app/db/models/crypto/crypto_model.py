from sqlalchemy import Column, DateTime, Enum, Float, Integer

from app.core import config
from app.db.base import Base


class Crypto(Base):
    __tablename__ = "cryptos"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, nullable=False)
    to_currency = Column(Enum(config.CurrencyList), nullable=False)
    rate = Column(Float, nullable=False)
    from_crypto = Column(Enum(config.CryptoList), nullable=False)

    def __repr__(self) -> str:
        return f"{self.from_crypto} is {self.to_currency} at {self.time}"
