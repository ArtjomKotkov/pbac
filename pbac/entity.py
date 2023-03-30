from __future__ import annotations

from typing import Any, TypeVar, Generic

from .base import Executable
from .models import EntityPack
from .exceptions import NotApplicable


class Box(Executable):
    def __init__(self, value):
        self._value = value

    def execute(self, _: EntityPack):
        return self._value


class EntityCombiner(Executable):
    def __init__(self, item1: Any, item2: Any):
        self._item1 = self._wrap_value_if_need(item1)
        self._item2 = self._wrap_value_if_need(item2)

    @staticmethod
    def _wrap_value_if_need(value: Any) -> Box | Executable:
        if not isinstance(value, Executable) and not issubclass(type(value), Executable):
            return Box(value)
        else:
            return value

    def __eq__(self, other: Any) -> EntityEqualCombiner:
        return EntityEqualCombiner(self, other)

    def __ne__(self, other: Any) -> EntityNotCombiner:
        return EntityNotCombiner(self, other)

    def __lt__(self, other) -> EntityLtCombiner:
        return EntityLtCombiner(self, other)

    def __gt__(self, other) -> EntityGtCombiner:
        return EntityGtCombiner(self, other)

    def __le__(self, other) -> EntityLeCombiner:
        return EntityLeCombiner(self, other)

    def __ge__(self, other) -> EntityGtCombiner:
        return EntityGtCombiner(self, other)

    def __and__(self, other):
        return EntityAndCombiner(self, other)

    def __or__(self, other):
        return EntityOrCombiner(self, other)


class EntityEqualCombiner(EntityCombiner):
    def execute(self, pack: EntityPack) -> Any:
        return self._item1.execute(pack) == self._item2.execute(pack)


class EntityNotCombiner(EntityCombiner):
    def execute(self, pack: EntityPack) -> Any:
        return self._item1.execute(pack) != self._item2.execute(pack)


class EntityLtCombiner(EntityCombiner):
    def execute(self, pack: EntityPack) -> Any:
        return self._item1.execute(pack) < self._item2.execute(pack)


class EntityGtCombiner(EntityCombiner):
    def execute(self, pack: EntityPack) -> Any:
        return self._item1.execute(pack) > self._item2.execute(pack)


class EntityLeCombiner(EntityCombiner):
    def execute(self, pack: EntityPack) -> Any:
        return self._item1.execute(pack) <= self._item2.execute(pack)


class EntityGeCombiner(EntityCombiner):
    def execute(self, pack: EntityPack) -> Any:
        return self._item1.execute(pack) >= self._item2.execute(pack)


class EntityAndCombiner(EntityCombiner):
    def execute(self, pack: EntityPack) -> Any:
        return self._item1.execute(pack) and self._item2.execute(pack)


class EntityOrCombiner(EntityCombiner):
    def execute(self, pack: EntityPack) -> Any:
        return self._item1.execute(pack) or self._item2.execute(pack)


class EntityAttribute(Executable):
    def __init__(self, model: type[Any], attr: str):
        self._model = model
        self._attr = attr

    def execute(self, pack: EntityPack) -> Any:
        target_entity = next((entity for entity in pack.entities if isinstance(entity, self._model)), None)

        if target_entity is None:
            raise NotApplicable()

        return getattr(target_entity, self._attr)

    def __eq__(self, other: Any) -> EntityEqualCombiner:
        return EntityEqualCombiner(self, other)

    def __ne__(self, other: Any) -> EntityNotCombiner:
        return EntityNotCombiner(self, other)

    def __lt__(self, other) -> EntityLtCombiner:
        return EntityLtCombiner(self, other)

    def __gt__(self, other) -> EntityGtCombiner:
        return EntityGtCombiner(self, other)

    def __le__(self, other) -> EntityLeCombiner:
        return EntityLeCombiner(self, other)

    def __ge__(self, other) -> EntityGtCombiner:
        return EntityGtCombiner(self, other)

    def __and__(self, other):
        return EntityAndCombiner(self, other)

    def __or__(self, other):
        return EntityOrCombiner(self, other)


T = TypeVar('T')


class Entity(Generic[T]):
    def __init__(self, model: type[T]):
        self.model = model

    def __getattribute__(self, key: str) -> Any:
        if key.startswith('__') and key.endswith('__') or key == 'model':
            return super().__getattribute__(key)

        if key in self.model.__annotations__.keys():
            return EntityAttribute(self.model, key)
        else:
            return super().__getattribute__(key)
