from sqlalchemy import Column, String, Integer, BigInteger

from bot.models.base import Base


class Service(Base):
    __tablename__ = "service"
    id = Column(BigInteger, primary_key=True, index=True)
    telegram_id = Column(BigInteger)
    service_name = Column(String)
    login = Column(String)
    password = Column(String)
