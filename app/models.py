from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True)
    title_hindi = Column(Text, nullable=False)
    description_hindi = Column(Text, nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now())


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, ForeignKey("content.id"))
    language_code = Column(String(5))
    translated_title = Column(Text)
    translated_description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("content_id", "language_code", name="unique_translation"),
    )