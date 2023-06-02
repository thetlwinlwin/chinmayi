from datetime import datetime

from pydantic import BaseModel

from app.core.config.all_currencies import CryptoList, CurrencyList


class CryptoDbIn(BaseModel):
    time: datetime
    to_currency: CurrencyList
    rate: float
    from_crypto: CryptoList


class CryptoDbOut(CryptoDbIn):
    id: int

    class Config:
        orm_mode = True


class CryptoBase(BaseModel):
    time: datetime
    asset_id_quote: CurrencyList
    rate: float


class CryptoToCurrency(CryptoBase):
    asset_id_base: CryptoList

    def convert_to_db_type(self) -> CryptoDbIn:
        return CryptoDbIn(
            from_crypto=self.asset_id_base,
            to_currency=self.asset_id_quote,
            rate=self.rate,
            time=self.time,
        )


class CryptoToAllCurrencies(BaseModel):
    asset_id_base: CryptoList
    rates: list[CryptoBase]


class CryptoHistoryBase(BaseModel):
    time_period_start: datetime
    time_period_end: datetime
    time_open: datetime
    time_close: datetime
    rate_open: float
    rate_high: float
    rate_low: float
    rate_close: float

    def convert_to_db_type(
        self,
        crypto: CryptoList,
        currency: CurrencyList,
    ) -> CryptoDbIn:
        return CryptoDbIn(
            from_crypto=crypto,
            to_currency=currency,
            rate_close=self.rate_close,
            time=self.time_close,
        )


class CryptoHistoryCreate(CryptoHistoryBase):
    pass


class CryptoHistoryUpdate(CryptoHistoryBase):
    pass
