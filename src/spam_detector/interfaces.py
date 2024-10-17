"""
Contains the interfaces for API requests and responses.
"""

from uuid import UUID

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for health check."""

    version: str = Field(..., description="Version of the service")
    status: str = Field(..., description="Status of the service")


class Comment(BaseModel):
    """Request model for comment detection."""

    uuid: UUID = Field(..., description="Unique identifier of the comment")
    content: str = Field(..., description="Content of the comment")


class CommentDetectionResponse(BaseModel):
    """Response model for comment detection."""

    uuid: UUID = Field(..., description="Unique identifier of the comment")
    is_spam: bool = Field(..., description="Whether the comment is spam or not")
