from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, Date
from src.db.db import Base
from datetime import date


class Contact(Base):
    __tablename__ = 'contacts'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), index=True)
    last_name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), index=True)
    birthday: Mapped[date] = mapped_column(Date)
    additional_info: Mapped[str | None] = mapped_column(String(200), default=None)