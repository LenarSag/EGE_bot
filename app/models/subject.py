from enum import Enum as PyEnum

from sqlalchemy import (
    CheckConstraint,
    Enum,
    ForeignKey,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from config import MAX_SCORE, MIN_SCORE


class SubjectName(PyEnum):
    MATH = "математика"
    RUSSIAN = "русский язык"
    INFORMATICS = "информатика"
    PHYSICS = "физика"
    CHEMISTRY = "химия"
    BIOLOGY = "биология"


class SubjectScore(Base):
    __tablename__ = "subject_score"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="CASCADE")
    )
    subject_name: Mapped[SubjectName] = mapped_column(
        Enum(SubjectName, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )
    score: Mapped[int] = mapped_column(
        SmallInteger,
        CheckConstraint(f"score >= {MIN_SCORE} AND score <= {MAX_SCORE}"),
        nullable=False,
    )

    student: Mapped["Student"] = relationship(back_populates="scores")

    _table_args__ = (
        UniqueConstraint(
            "student_id", "subject_name", name="uq_student_subject"
        ),
    )
