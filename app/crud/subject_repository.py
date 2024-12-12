from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from app.models.subject import SubjectScore


async def get_scores(session: AsyncSession, student_id: int) -> Sequence[SubjectScore]:
    query = select(SubjectScore).filter_by(student_id=student_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_score(
    session: AsyncSession, student_id: int, subject_name: str
) -> Optional[SubjectScore]:
    stmt = select(SubjectScore).where(
        SubjectScore.student_id == student_id,
        SubjectScore.subject_name == subject_name,
    )
    result = await session.execute(stmt)
    return result.scalar()


async def update_score(
    session: AsyncSession, student_id: int, subject_name: str, score: int
) -> None:
    stmt = (
        update(SubjectScore)
        .where(
            SubjectScore.student_id == student_id,
            SubjectScore.subject_name == subject_name,
        )
        .values(score=score)
    )
    await session.execute(stmt)


async def add_score(
    session: AsyncSession, student_id: int, subject_name: str, score: int
) -> None:
    new_score = SubjectScore(
        student_id=student_id,
        subject_name=subject_name,
        score=score,
    )
    session.add(new_score)


async def save_all(session: AsyncSession) -> None:
    await session.commit()
