"""
Contains the interfaces for API requests and responses.
"""

from uuid import UUID

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for health check."""

    version: str = Field(..., description="Version of the service")
    status: str = Field(..., description="Status of the service")


class DetectRequestPayload(BaseModel):
    """Request model for comment detection."""

    uuid: UUID = Field(None, description="Unique identifier of the comment")
    content: str = Field(..., description="Content of the comment")


class DetectResponse(BaseModel):
    """Response model for comment detection."""

    uuid: UUID = Field(..., description="Unique identifier of the comment")
    is_spam: bool = Field(..., description="Whether the comment is spam or not")


class VideoRequestPayload(BaseModel):
    """Request model for video comment processing."""

    id: str = Field(..., description="YouTube video ID")
    first: int = Field(50, description="Number of comments to process")


class VideoResponse(BaseModel):
    """Response model for video comment processing."""

    id: str = Field(..., description="YouTube video ID")
    nb: int = Field(..., description="Number of comments processed")
    comments: list[DetectResponse] = Field(
        ..., description="List of comment detections"
    )
