from typing import Any

from pydantic import BaseModel

from const import Actions


class EntityPack(BaseModel):
    action: Actions
    entities: list[Any]


