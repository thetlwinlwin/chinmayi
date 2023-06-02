from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class PeriodSuffix(Enum):
    sec = "SEC"
    min = "MIN"
    hr = "HRS"
    day = "DAY"


class TimeConfigBody(BaseModel):
    time_start: datetime
    time_end: datetime
    period: int
    period_suffix: PeriodSuffix

    def _period_id(self) -> str:
        return f"{self.period}{self.period_suffix.value}"

    @property
    def get_args(self) -> dict:
        return {
            "time_start": self.time_start.isoformat(timespec="seconds"),
            "time_end": self.time_end.isoformat(timespec="seconds"),
            "period_id": self._period_id(),
        }

    class Config:
        schema_extra = {
            "example": {
                "time_start": "2019-05-18T15:17:08.132263Z",
                "time_end": "2019-05-19T01:05:08.631322Z",
                "period": 1,
                "period_suffix": "DAY",
            }
        }
