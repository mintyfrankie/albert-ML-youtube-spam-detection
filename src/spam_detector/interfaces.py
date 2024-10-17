"""
Contains the interfaces for API requests and responses.
"""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for health check."""

    version: str = Field(..., description="Version of the service")
    status: str = Field(..., description="Status of the service")
