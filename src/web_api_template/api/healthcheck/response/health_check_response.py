from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """Health check response"""

    status: str = Field(
        ...,
        json_schema_extra={"description": "Health check status", "example": "Healthy"},
    )
    version: str = Field(
        ..., json_schema_extra={"description": "API version", "example": "1.0.0"}
    )
