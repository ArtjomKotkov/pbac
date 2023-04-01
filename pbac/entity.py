from __future__ import annotations

from typing import Any

from .base import Executable
from .exceptions import NotApplicable, UnknownActorTypeProvided
from .const import ActorType


class Box(Executable):
    def __init__(self, value):
        self._value = value

    def execute(self, *_, **__):
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
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(subject, target, action, context) == self._item2.execute(subject, target, action, context)


class EntityNotCombiner(EntityCombiner):
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(subject, target, action, context) != self._item2.execute(subject, target, action, context)


class EntityLtCombiner(EntityCombiner):
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(subject, target, action, context) < self._item2.execute(subject, target, action, context)


class EntityGtCombiner(EntityCombiner):
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(subject, target, action, context) > self._item2.execute(subject, target, action, context)


class EntityLeCombiner(EntityCombiner):
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(subject, target, action, context) <= self._item2.execute(subject, target, action, context)


class EntityGeCombiner(EntityCombiner):
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(subject, target, action, context) >= self._item2.execute(subject, target, action, context)


class EntityAndCombiner(EntityCombiner):
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(subject, target, action, context) and self._item2.execute(subject, target, action, context)


class EntityOrCombiner(EntityCombiner):
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(subject, target, action, context) or self._item2.execute(subject, target, action, context)


class EntityAttribute(Executable):
    def __init__(self, actor_type: ActorType, attrs: list[str]):
        self._actor_type = actor_type
        self._attrs = attrs

    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        if self._actor_type == ActorType.SUBJECT:
            model = subject
        elif self._actor_type == ActorType.TARGET:
            model = target
        elif self._actor_type == ActorType.CONTEXT:
            model = context
        else:
            raise UnknownActorTypeProvided()

        if model is None:
            raise NotApplicable()

        return self._get_entity_attribute(model)

    def _get_entity_attribute(self, model: Any) -> Any:
        result = model
        # Step by attrs, and try to get attribute, if error occurs then try get item by key.
        # If not attribute or item is not found then make decision than not applicable.
        for attr in self._attrs:
            try:
                result = getattr(result, attr)
            except AttributeError:
                try:
                    result = result[attr]
                except KeyError:
                    raise NotApplicable()

        return result

    def __getattribute__(self, key: str) -> Any:
        if (
            key.startswith('__') and key.endswith('__')
            or key in self.__class__.__dict__.keys()
            or key in self.__dict__.keys()
        ):
            return super().__getattribute__(key)

        return EntityAttribute(self._actor_type, [*self._attrs, key])

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
