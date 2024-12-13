from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.student import Student


async def get_student_by_id(
    session: AsyncSession, id: int
) -> Optional[Student]:
    query = select(Student).filter_by(id=id)
    result = await session.execute(query)
    return result.scalar()


async def create_student(
    session: AsyncSession, student_data: dict[str, str | int]
) -> None:
    student = Student(**student_data)
    session.add(student)
    await session.commit()
