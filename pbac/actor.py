from __future__ import annotations

from typing import Any, TypeVar

from .base import Executable
from .const import ActorType
from .exceptions import UnknownActorTypeProvided
from .entity import Entity


class MetaActor(type):
    _actor_type: ActorType

    def __eq__(self, other: type[Any]):
        return ActorResolver(self._actor_type, other)


class Actor(metaclass=MetaActor):
    _actor_type = None


class Target(Actor):
    _actor_type = ActorType.TARGET


class Subject(Actor):
    _actor_type = ActorType.SUBJECT


T = TypeVar('T')


class ActorResolver(Executable):
    def __init__(self, type_: ActorType, entity: Entity[T]):
        self._type = type_
        self._model = entity.model

    def execute(self, target: Any, subject: Any):
        return self._is_correspond(target, subject)

    def _is_correspond(self, target: Any, subject: Any):
        if self._type == ActorType.TARGET:
            model = target
        elif self._type == ActorType.SUBJECT:
            model = subject
        else:
            raise UnknownActorTypeProvided()

        return isinstance(model, self._model)

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
    def execute(self, target: Any, subject: Any) -> Any:
        return self._item1.execute(target, subject) and self._item2.execute(target, subject)


class ActorOrCombiner(ActorCombiner):
    def execute(self, target: Any, subject: Any) -> Any:
        return self._item1.execute(target, subject) or self._item2.execute(target, subject)
