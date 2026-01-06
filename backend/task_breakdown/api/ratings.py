"""Rating API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from task_breakdown.config.logging_config import get_logger
from task_breakdown.database import get_db
from task_breakdown.models import Rating, Task
from task_breakdown.schemas import RatingCreate, RatingResponse, RatingStatsResponse

logger = get_logger(__name__)
router = APIRouter()

# Constants
MAX_RATING = 5
MIN_RATING = 1


@router.post("/", response_model=RatingResponse, status_code=201)
async def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    """Create a rating for a task guide."""
    logger.debug(f"Creating rating for task {rating.task_id} with rating {rating.rating}")
    try:
        # Verify task exists
        task = db.query(Task).filter(Task.id == rating.task_id).first()
        if not task:
            logger.warning(f"Task {rating.task_id} not found when creating rating")
            raise HTTPException(status_code=404, detail="Task not found")

        # Validate rating
        if rating.rating < MIN_RATING or rating.rating > MAX_RATING:
            logger.warning(
                f"Invalid rating value: {rating.rating} (must be between {MIN_RATING} and {MAX_RATING})"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Rating must be between {MIN_RATING} and {MAX_RATING}",
            )

        # Create rating
        logger.debug(
            f"Creating rating object: task_id={rating.task_id}, rating={rating.rating}, has_comment={bool(rating.comment)}"
        )
        db_rating = Rating(task_id=rating.task_id, rating=rating.rating, comment=rating.comment)
        db.add(db_rating)
        logger.debug("Rating added to database session, committing...")
        db.commit()
        db.refresh(db_rating)
        logger.info(f"Rating {db_rating.id} created successfully for task {rating.task_id}")

        return RatingResponse(
            id=db_rating.id,
            task_id=db_rating.task_id,
            rating=db_rating.rating,
            comment=db_rating.comment,
            created_at=db_rating.created_at,
        )
    except HTTPException:
        # Re-raise HTTP exceptions without logging as error
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating rating for task {rating.task_id}: {e}")
        logger.critical(f"Critical database error while creating rating for task {rating.task_id}")
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.get("/{task_id}", response_model=RatingStatsResponse)
async def get_ratings(task_id: int, db: Session = Depends(get_db)):
    """Get rating statistics for a task."""
    logger.debug(f"Fetching rating statistics for task {task_id}")
    try:
        # Verify task exists
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            logger.warning(f"Task {task_id} not found when fetching ratings")
            raise HTTPException(status_code=404, detail="Task not found")

        # Get ratings
        logger.debug(f"Querying ratings for task {task_id}")
        ratings = db.query(Rating).filter(Rating.task_id == task_id).all()

        if not ratings:
            logger.debug(f"No ratings found for task {task_id}")
            logger.warning(f"Task {task_id} has no ratings yet")
            return RatingStatsResponse(
                task_id=task_id, average_rating=0.0, total_ratings=0, ratings=[]
            )

        # Calculate average
        logger.debug(f"Calculating average rating from {len(ratings)} ratings")
        average = sum(r.rating for r in ratings) / len(ratings)
        rating_distribution = {}
        for r in ratings:
            rating_distribution[r.rating] = rating_distribution.get(r.rating, 0) + 1
        logger.debug(f"Rating distribution: {rating_distribution}")
        logger.info(f"Retrieved {len(ratings)} ratings for task {task_id}, average: {average:.2f}")

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
                    created_at=r.created_at,
                )
                for r in ratings
            ],
        )
    except HTTPException:
        # Re-raise HTTP exceptions without logging as error
        raise
    except Exception as e:
        logger.error(f"Error fetching ratings for task {task_id}: {e}")
        logger.critical(f"Critical database error while fetching ratings for task {task_id}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
