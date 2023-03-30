from pydantic import BaseModel


class CreateAppeal(BaseModel):
    surname: str
    name: str
    patronymic: str
    phone_number: str
    appeal_text: str

    class Config:
        orm_mode = True
