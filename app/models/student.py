import re

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from app.models.base import Base
from config import FIRST_LAST_NAME_REGEX, MAX_NAME_LENGTH


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    last_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)

    scores: Mapped[list["SubjectScore"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )

    @validates("first_name")
    def validate_first_name(self, key, first_name):
        if not re.match(FIRST_LAST_NAME_REGEX, first_name):
            raise ValueError("Invalid first name format")
        return first_name

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        if not re.match(FIRST_LAST_NAME_REGEX, last_name):
            raise ValueError("Invalid last name format")
        return last_name
