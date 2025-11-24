"""Guide API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from task_breakdown.database import get_db
from task_breakdown.models import GuideStep, Task
from task_breakdown.schemas import GuideStepResponse

router = APIRouter()


@router.get("/{task_id}", response_model=list[GuideStepResponse])
async def get_guide(task_id: int, db: Session = Depends(get_db)):
    """Get guide steps for a specific task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    steps = db.query(GuideStep).filter(GuideStep.task_id == task_id).order_by(GuideStep.step_number).all()

    return [
        GuideStepResponse(
            id=step.id,
            task_id=step.task_id,
            step_number=step.step_number,
            title=step.title,
            description=step.description,
            detailed_instructions=step.detailed_instructions,
            estimated_time=step.estimated_time,
            dependencies=step.dependencies or [],
            resources=step.resources or [],
            code_snippets=step.code_snippets or [],
            tips=step.tips,
            warnings=step.warnings,
            verification_steps=step.verification_steps,
            created_at=step.created_at
        )
        for step in steps
    ]

