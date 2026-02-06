from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    title: str
    content: Optional[str] = None
    status: str
    created_at: datetime
    due_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    parent_id: Optional[str] = None
    depends_on: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)
    note: Optional[str] = None
