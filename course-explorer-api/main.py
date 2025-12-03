from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Course Explorer API")

class Course(BaseModel):
    id: int
    title: str
    category: str
    level: str
    instructor_id: int
    rating: float

courses_db = [
    Course(id=1, title="Python for Beginners", category="python", level="beginner", instructor_id=101, rating=4.5),
    Course(id=2, title="Advanced Python", category="python", level="advanced", instructor_id=101, rating=4.8),
    Course(id=3, title="Intro to Machine Learning", category="ml", level="intermediate", instructor_id=102, rating=4.6),
    Course(id=4, title="Deep Learning Basics", category="ml", level="advanced", instructor_id=102, rating=4.7),
    Course(id=5, title="Web Development with FastAPI", category="web", level="intermediate", instructor_id=103, rating=4.9),
]
# -----------------------------
#  Basic Root Endpoint
# -----------------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to Course Explorer API"}

# -----------------------------
#  PATH PARAMETER EXAMPLE
#  Get a single course by ID
#  /courses/3
# -----------------------------
@app.get("/courses/{course_id}", response_model=Course)
def get_course_by_id(course_id: int):
    """
    Path parameter:
    - course_id is part of the URL path and identifies a single course.
    """
    for course in courses_db:
        if course.id == course_id:
            return course
    # Simple error – in real projects, you'd raise HTTPException
    return {"error": f"Course with id {course_id} not found"}

# -----------------------------
#  QUERY PARAMETERS EXAMPLE
#  Filter and paginate courses
#  /courses?category=python&level=beginner&limit=2
# -----------------------------
@app.get("/courses", response_model=List[Course])
def list_courses(
    category: Optional[str] = None,
    level: Optional[str] = None,
    min_rating: float = 0.0,
    limit: int = Query(10, le=50),
):
    """
    Query parameters:
    - category, level, min_rating, limit are NOT part of the path.
    - They refine/filter how we fetch the list of courses.
    """
    results = courses_db

    if category:
        results = [c for c in results if c.category == category]

    if level:
        results = [c for c in results if c.level == level]

    results = [c for c in results if c.rating >= min_rating]

    # simple pagination using 'limit'
    return results[:limit]

# -----------------------------
#  COMBINED USE:
#  PATH + QUERY PARAMETERS
#  /instructors/101/courses?level=advanced
# -----------------------------
@app.get("/instructors/{instructor_id}/courses", response_model=List[Course])
def list_courses_by_instructor(
    instructor_id: int,
    level: Optional[str] = None,
    category: Optional[str] = None,
):
    """
    - Path parameter: instructor_id (which instructor's courses?)
    - Query parameters: level, category (how to filter those courses?)
    """
    results = [c for c in courses_db if c.instructor_id == instructor_id]

    if level:
        results = [c for c in results if c.level == level]

    if category:
        results = [c for c in results if c.category == category]

    return results
