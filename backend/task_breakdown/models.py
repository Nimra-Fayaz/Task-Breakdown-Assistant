"""Database models."""

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from task_breakdown.database import Base


class Task(Base):
    """Task model - stores task descriptions and metadata."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    complexity_score = Column(Integer, default=5)  # 1-10 scale
    estimated_total_time = Column(Integer, nullable=True)  # in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    guide_steps = relationship(
        "GuideStep", back_populates="task", cascade="all, delete-orphan"
    )
    ratings = relationship(
        "Rating", back_populates="task", cascade="all, delete-orphan"
    )


class GuideStep(Base):
    """Guide step model - stores individual steps in a task breakdown."""

    __tablename__ = "guide_steps"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    detailed_instructions = Column(Text, nullable=True)
    estimated_time = Column(Integer, nullable=True)  # in minutes
    dependencies = Column(JSON, nullable=True)  # List of step numbers this depends on
    resources = Column(JSON, nullable=True)  # List of resources/links
    code_snippets = Column(JSON, nullable=True)  # Code examples for this step
    tips = Column(Text, nullable=True)
    warnings = Column(Text, nullable=True)
    verification_steps = Column(Text, nullable=True)  # How to verify step completion
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    task = relationship("Task", back_populates="guide_steps")


class Rating(Base):
    """Rating model - stores user ratings for guides."""

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    task = relationship("Task", back_populates="ratings")
