"""Guide API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from task_breakdown.config.logging_config import get_logger
from task_breakdown.database import get_db
from task_breakdown.models import GuideStep, Task
from task_breakdown.schemas import GuideStepResponse

logger = get_logger(__name__)
router = APIRouter()


@router.get("/{task_id}", response_model=list[GuideStepResponse])
async def get_guide(task_id: int, db: Session = Depends(get_db)):
    """Get guide steps for a specific task."""
    logger.debug(f"Fetching guide steps for task {task_id}")
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            logger.warning(f"Task {task_id} not found when fetching guide steps")
            raise HTTPException(status_code=404, detail="Task not found")

        logger.debug(f"Querying guide steps for task {task_id}")
        steps = (
            db.query(GuideStep)
            .filter(GuideStep.task_id == task_id)
            .order_by(GuideStep.step_number)
            .all()
        )

        if not steps:
            logger.warning(f"No guide steps found for task {task_id}")
        else:
            logger.info(f"Retrieved {len(steps)} guide steps for task {task_id}")
            logger.debug(
                f"Guide steps range: step {min(s.step_number for s in steps)} to {max(s.step_number for s in steps)}"
            )

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
                created_at=step.created_at,
            )
            for step in steps
        ]
    except HTTPException:
        # Re-raise HTTP exceptions (like 404) without logging as error
        raise
    except Exception as e:
        logger.error(f"Error fetching guide steps for task {task_id}: {e}")
        logger.critical(f"Critical database error while fetching guide steps for task {task_id}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
