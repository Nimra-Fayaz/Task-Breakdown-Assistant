"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field


class GuideStepBase(BaseModel):
    """Base schema for guide step."""
    step_number: int
    title: str
    description: str
    detailed_instructions: str | None = None
    estimated_time: int | None = None
    dependencies: list[int] | None = None
    resources: list[str] | None = None
    code_snippets: list[str] | None = None
    tips: str | None = None
    warnings: str | None = None
    verification_steps: str | None = None


class GuideStepCreate(GuideStepBase):
    """Schema for creating a guide step."""
    pass


class GuideStepResponse(GuideStepBase):
    """Schema for guide step response."""
    id: int
    task_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    """Schema for creating a task."""
    description: str = Field(..., min_length=10, description="Task description")
    title: str | None = None


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: int
    title: str | None
    description: str
    complexity_score: int
    estimated_total_time: int | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class TaskWithGuideResponse(TaskResponse):
    """Schema for task with guide steps."""
    guide_steps: list[GuideStepResponse] = []


class RatingCreate(BaseModel):
    """Schema for creating a rating."""
    task_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str | None = None


class RatingResponse(BaseModel):
    """Schema for rating response."""
    id: int
    task_id: int
    rating: int
    comment: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class RatingStatsResponse(BaseModel):
    """Schema for rating statistics."""
    task_id: int
    average_rating: float
    total_ratings: int
    ratings: list[RatingResponse]

