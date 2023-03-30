from sqlalchemy import Integer, String, Text
from sqlalchemy.sql.schema import Column
from database import Base


class Appeal(Base):
    __tablename__ = 'appeals'

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False)
    phone_number = Column(Integer(), nullable=False)
    appeal_text = Column(Text, nullable=False)

    # validation of columns not working at this level of program
    # (https://stackoverflow.com/questions/33192062/how-does-nullable-false-work-in-sqlalchemy)