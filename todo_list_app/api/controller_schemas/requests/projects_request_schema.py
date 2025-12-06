from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProjectCreateRequest(BaseModel):
    name: str = Field(max_length=30)
    description: Optional[str] = Field(default="", max_length=150)

class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=30)
    description: Optional[str] = Field(None, max_length=150)