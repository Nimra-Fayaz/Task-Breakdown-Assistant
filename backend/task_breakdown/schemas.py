"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GuideStepBase(BaseModel):
    """Base schema for guide step."""
    step_number: int
    title: str
    description: str
    detailed_instructions: Optional[str] = None
    estimated_time: Optional[int] = None
    dependencies: Optional[List[int]] = None
    resources: Optional[List[str]] = None
    code_snippets: Optional[List[str]] = None
    tips: Optional[str] = None
    warnings: Optional[str] = None
    verification_steps: Optional[str] = None


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
    title: Optional[str] = None


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: int
    title: Optional[str]
    description: str
    complexity_score: int
    estimated_total_time: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TaskWithGuideResponse(TaskResponse):
    """Schema for task with guide steps."""
    guide_steps: List[GuideStepResponse] = []


class RatingCreate(BaseModel):
    """Schema for creating a rating."""
    task_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = None


class RatingResponse(BaseModel):
    """Schema for rating response."""
    id: int
    task_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class RatingStatsResponse(BaseModel):
    """Schema for rating statistics."""
    task_id: int
    average_rating: float
    total_ratings: int
    ratings: List[RatingResponse]

