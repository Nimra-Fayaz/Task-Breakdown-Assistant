"""Task API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from task_breakdown.database import get_db
from task_breakdown.models import Task, GuideStep
from task_breakdown.schemas import TaskCreate, TaskResponse, TaskWithGuideResponse, GuideStepResponse
from task_breakdown.services.ai_service import generate_task_breakdown

router = APIRouter()


@router.post("", response_model=TaskWithGuideResponse, status_code=201)
@router.post("/", response_model=TaskWithGuideResponse, status_code=201)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task and generate AI-powered breakdown.
    
    This endpoint takes a task description and uses AI to generate
    a detailed, beginner-friendly step-by-step guide.
    """
    try:
        # Generate breakdown using AI
        print(f"Generating breakdown for task: {task.description[:50]}...")  # Debug log
        breakdown = generate_task_breakdown(task.description)
        print(f"Breakdown generated successfully: {len(breakdown.get('steps', []))} steps")  # Debug log
        
        # Create task
        db_task = Task(
            title=task.title or breakdown.get("title", "Untitled Task"),
            description=task.description,
            complexity_score=breakdown.get("complexity_score", 5),
            estimated_total_time=breakdown.get("estimated_total_time")
        )
        db.add(db_task)
        db.flush()  # Get the task ID
        
        # Create guide steps
        steps_data = breakdown.get("steps", [])
        for step_data in steps_data:
            # Normalize code_snippets - convert dicts to strings
            code_snippets_raw = step_data.get("code_snippets", [])
            code_snippets_normalized = []
            if code_snippets_raw:
                for snippet in code_snippets_raw:
                    if isinstance(snippet, dict):
                        # If it's a dict with 'code' key, extract the code
                        if 'code' in snippet:
                            code_snippets_normalized.append(str(snippet['code']))
                        elif 'content' in snippet:
                            code_snippets_normalized.append(str(snippet['content']))
                        else:
                            # Convert entire dict to string representation
                            code_snippets_normalized.append(str(snippet))
                    elif isinstance(snippet, str):
                        code_snippets_normalized.append(snippet)
                    else:
                        # Convert any other type to string
                        code_snippets_normalized.append(str(snippet))
            
            # Normalize dependencies - ensure it's a list of integers
            dependencies_raw = step_data.get("dependencies", [])
            dependencies_normalized = []
            if dependencies_raw:
                for dep in dependencies_raw:
                    if isinstance(dep, int):
                        dependencies_normalized.append(dep)
                    elif isinstance(dep, str) and dep.isdigit():
                        dependencies_normalized.append(int(dep))
                    elif isinstance(dep, (list, tuple)) and len(dep) > 0:
                        # Handle nested lists
                        dependencies_normalized.append(int(dep[0]) if isinstance(dep[0], (int, str)) else 0)
            
            # Normalize resources - ensure it's a list of strings
            resources_raw = step_data.get("resources", [])
            resources_normalized = []
            if resources_raw:
                for res in resources_raw:
                    if isinstance(res, str):
                        resources_normalized.append(res)
                    elif isinstance(res, dict) and 'url' in res:
                        resources_normalized.append(str(res['url']))
                    else:
                        resources_normalized.append(str(res))
            
            db_step = GuideStep(
                task_id=db_task.id,
                step_number=int(step_data.get("step_number", 0)),
                title=str(step_data.get("title", ""))[:255],  # Limit to 255 chars
                description=str(step_data.get("description", "")),
                detailed_instructions=str(step_data.get("detailed_instructions", "")) if step_data.get("detailed_instructions") else None,
                estimated_time=int(step_data.get("estimated_time", 0)) if step_data.get("estimated_time") else None,
                dependencies=dependencies_normalized if dependencies_normalized else None,
                resources=resources_normalized if resources_normalized else None,
                code_snippets=code_snippets_normalized if code_snippets_normalized else None,
                tips=str(step_data.get("tips", "")) if step_data.get("tips") else None,
                warnings=str(step_data.get("warnings", "")) if step_data.get("warnings") else None,
                verification_steps=str(step_data.get("verification_steps", "")) if step_data.get("verification_steps") else None
            )
            db.add(db_step)
        
        db.commit()
        db.refresh(db_task)
        
        # Return task with guide steps
        return TaskWithGuideResponse(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            complexity_score=db_task.complexity_score,
            estimated_total_time=db_task.estimated_total_time,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            guide_steps=[
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
                for step in db_task.guide_steps
            ]
        )
        
    except Exception as e:
        db.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR in create_task: {str(e)}")  # Debug log
        print(f"Traceback: {error_trace}")  # Debug log
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tasks."""
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=TaskWithGuideResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task with its guide steps."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskWithGuideResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        complexity_score=task.complexity_score,
        estimated_total_time=task.estimated_total_time,
        created_at=task.created_at,
        updated_at=task.updated_at,
        guide_steps=[
            GuideStepResponse(
                id=step.id,
                task_id=step.task_id,
                step_number=step.step_number,
                title=step.title,
                description=step.description,
                detailed_instructions=step.detailed_instructions,
                estimated_time=step.estimated_time,
                dependencies=step.dependencies,
                resources=step.resources,
                code_snippets=step.code_snippets,
                tips=step.tips,
                warnings=step.warnings,
                verification_steps=step.verification_steps,
                created_at=step.created_at
            )
            for step in task.guide_steps
        ]
    )


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task and its guide steps."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return None

