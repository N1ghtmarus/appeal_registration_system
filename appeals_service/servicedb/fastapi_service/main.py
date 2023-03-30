from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_session, engine
from models import Appeal
from database import Base
from schemas import CreateAppeal


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/")
def create(details: CreateAppeal, db: Session = Depends(get_session)) -> dict[str, bool]:
    """
    Функция создает новую запись об обращении в базе данных.

    :param details: данные, переданные из формы обращения
    :type details: CreateAppeal
    :param db: сессия базы данных
    :type db: Session
    :return: словарь, содержащий информацию об успешности выполнения операции
    :rtype: dict
    """
    to_create = Appeal(
        surname=details.surname,
        name=details.name,
        patronymic=details.patronymic,
        phone_number=details.phone_number,
        appeal_text=details.appeal_text,
    )
    db.add(to_create)
    db.commit()
    return {"success": True}
