"""
CCP Pydantic Models — Coach Registry
Task 1.02 — Schema for coach_registry.json with validation.

The coach registry is the source of truth for coach identity,
Person ID generation, and integration credentials references.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CoachRegistry(BaseModel):
    """Registry entry for a single coach instance."""

    coach_name: str = Field(
        ...,
        description="Full name of the coach",
        examples=["Nadia Lefèvre"],
    )
    coach_acronym: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="3-letter unique coach acronym (uppercase)",
        examples=["NDL"],
    )
    coach_id: str = Field(
        ...,
        pattern=r"^[A-Z]{3}-0000$",
        description="Coach's own Person ID (always CCC-0000)",
        examples=["NDL-0000"],
    )
    next_client_id: int = Field(
        default=1,
        ge=1,
        le=9999,
        description="Next available client number for Person ID assignment",
    )
    notion_workspace_id: str = Field(
        default="",
        description="Notion workspace ID for this coach",
    )
    notion_token_ref: str = Field(
        default="",
        description="Environment variable name holding the Notion token",
        examples=["NOTION_TOKEN_NDL"],
    )
    supabase_bucket: str = Field(
        ...,
        description="Supabase Storage bucket name for this coach",
        examples=["coach-ndl"],
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Coach instance creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Last update timestamp",
    )

    @field_validator("coach_acronym")
    @classmethod
    def validate_acronym(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError("Coach acronym must contain only letters")
        return v.upper()

    def assign_next_client_id(self) -> str:
        """Generate the next Person ID and increment the counter.

        Returns:
            Person ID string in format CCC-NNNN (e.g. NDL-0001)
        """
        person_id = f"{self.coach_acronym}-{self.next_client_id:04d}"
        self.next_client_id += 1
        self.updated_at = datetime.now()
        return person_id

    def get_coach_person_id(self) -> str:
        """Return the coach's own Person ID (CCC-0000)."""
        return self.coach_id


class PersonID(BaseModel):
    """A person identifier in the CCP system."""

    coach_acronym: str = Field(..., min_length=3, max_length=3)
    number: int = Field(..., ge=0, le=9999)

    @property
    def full_id(self) -> str:
        return f"{self.coach_acronym}-{self.number:04d}"

    @property
    def is_coach(self) -> bool:
        return self.number == 0

    @classmethod
    def parse(cls, person_id: str) -> "PersonID":
        """Parse a Person ID string (e.g. 'NDL-0001') into a PersonID object."""
        parts = person_id.strip().upper().split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid Person ID format: {person_id}")
        return cls(coach_acronym=parts[0], number=int(parts[1]))

    def __str__(self) -> str:
        return self.full_id
