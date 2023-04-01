from __future__ import annotations

from typing import Any

from .base import Executable
from .const import ActorType
from .exceptions import UnknownActorTypeProvided
from .entity import EntityAttribute


class MetaActor(type):
    _actor_type: ActorType

    def __eq__(self, other: type[Any]):
        return ActorResolver(self._actor_type, other)

    def __getattribute__(self, key: str) -> Any:
        if (
            key.startswith('__') and key.endswith('__')
            or key in self.__class__.__dict__.keys()
            or key in self.__dict__.keys()
        ):
            return super().__getattribute__(key)

        return EntityAttribute(self._actor_type, [key])


class Actor(metaclass=MetaActor):
    _actor_type = None


class Target(Actor):
    _actor_type = ActorType.TARGET


class Subject(Actor):
    _actor_type = ActorType.SUBJECT


class Context(Actor):
    _actor_type = ActorType.CONTEXT


class ActorResolver(Executable):
    def __init__(self, type_: ActorType, entity: Any):
        self._type = type_
        self._entity = entity

    def execute(self, subject: Any, target: Any, action: str, context: Any):
        return self._is_correspond(target, subject)

    def _is_correspond(self, target: Any, subject: Any):
        if self._type == ActorType.TARGET:
            model = target
        elif self._type == ActorType.SUBJECT:
            model = subject
        else:
            raise UnknownActorTypeProvided()

        if isinstance(model, type):
            # If provided model is a class, we compare it with the model of the entity directly.
            return model == self._entity

        return isinstance(model, self._entity)

    def __and__(self, other):
        return ActorAndCombiner(self, other)

    def __or__(self, other):
        return ActorOrCombiner(self, other)


class ActorCombiner(Executable):
    def __init__(self, item1: ActorResolver | ActorCombiner, item2: ActorResolver | ActorCombiner):
        assert isinstance(item1, (ActorResolver, ActorCombiner)) and isinstance(item2, (ActorResolver, ActorCombiner))

        self._item1 = item1
        self._item2 = item2


class ActorAndCombiner(ActorCombiner):
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(target, subject, action, context) and self._item2.execute(target, subject, action, context)


class ActorOrCombiner(ActorCombiner):
    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Any:
        return self._item1.execute(target, subject, action, context) or self._item2.execute(target, subject, action, context)
