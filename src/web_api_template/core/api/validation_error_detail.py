from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class ValidationErrorDetail(BaseModel):
    type: str
    loc: List[str]
    msg: str
    input: Any
    ctx: Optional[Dict[str, Any]] = None
    url: Optional[str] = None
