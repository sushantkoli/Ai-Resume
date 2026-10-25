from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Resume(Base):
    __tablename__="resumes"

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=True
        )
    
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
        )
    filename: Mapped[str] = mapped_column(
        nullable=False
        )
    content: Mapped[str] = mapped_column(
        nullable=False
        )