from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class Workout(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: str
    duration: float
    calories: float
    weight: float
    date: datetime


class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    weight: float