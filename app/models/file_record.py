from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.database import Base


class FileRecord(Base):
    __tablename__ = "files"

    id = Column(
        String(36),
        primary_key=True,
        index=True,
    )

    filename = Column(
        String(255),
        nullable=False,
    )

    file_type = Column(
        String(20),
        nullable=False,
    )

    feature_count = Column(
        Integer,
        nullable=False,
    )

    crs = Column(
        String(100),
        nullable=True,
    )

    measurement_crs = Column(
        String(100),
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
    )

    features_json = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )