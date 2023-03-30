from typing import Any

from pydantic import BaseModel

from .const import Actions


class PBacRequest(BaseModel):
    action: Actions
    subject: Any
    target: Any
