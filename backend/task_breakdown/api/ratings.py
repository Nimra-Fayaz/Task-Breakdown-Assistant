"""Rating API endpoints."""


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from task_breakdown.database import get_db
from task_breakdown.models import Rating, Task
from task_breakdown.schemas import RatingCreate, RatingResponse, RatingStatsResponse

router = APIRouter()

# Constants
MAX_RATING = 5
MIN_RATING = 1


@router.post("/", response_model=RatingResponse, status_code=201)
async def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    """Create a rating for a task guide."""
    # Verify task exists
    task = db.query(Task).filter(Task.id == rating.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Validate rating
    if rating.rating < MIN_RATING or rating.rating > MAX_RATING:
        raise HTTPException(status_code=400, detail=f"Rating must be between {MIN_RATING} and {MAX_RATING}")

    # Create rating
    db_rating = Rating(
        task_id=rating.task_id,
        rating=rating.rating,
        comment=rating.comment
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)

    return RatingResponse(
        id=db_rating.id,
        task_id=db_rating.task_id,
        rating=db_rating.rating,
        comment=db_rating.comment,
        created_at=db_rating.created_at
    )


@router.get("/{task_id}", response_model=RatingStatsResponse)
async def get_ratings(task_id: int, db: Session = Depends(get_db)):
    """Get rating statistics for a task."""
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get ratings
    ratings = db.query(Rating).filter(Rating.task_id == task_id).all()

    if not ratings:
        return RatingStatsResponse(
            task_id=task_id,
            average_rating=0.0,
            total_ratings=0,
            ratings=[]
        )

    # Calculate average
    average = sum(r.rating for r in ratings) / len(ratings)

    return RatingStatsResponse(
        task_id=task_id,
        average_rating=round(average, 2),
        total_ratings=len(ratings),
        ratings=[
            RatingResponse(
                id=r.id,
                task_id=r.task_id,
                rating=r.rating,
                comment=r.comment,
                created_at=r.created_at
            )
            for r in ratings
        ]
    )

