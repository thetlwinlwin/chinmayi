from pydantic import BaseModel


class LeadBase(BaseModel):
    first_name: str
    last_name: str
    phone_work: str


class LeadUpdate(LeadBase):
    ...


class LeadCreate(LeadBase):
    ...


class LeadOut(LeadBase):
    id: int

    class Config:
        orm_mode = True
