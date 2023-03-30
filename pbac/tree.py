from typing import Iterable, Self, Optional, Type

from const import *
from entity import EntityCombiner, EntityAttribute
from actor import ActorCombiner, ActorResolver
from request import PBacRequest
from combine_resolver import CombineResolver
from models import EntityPack


class Rule:
    def __init__(
        self,
        _id: str,
        description: str,
        effect: Effect,
        actors: Optional[ActorCombiner | ActorResolver] = None,
        condition: Type[EntityCombiner | EntityAttribute] = None,
    ):
        self._id = _id
        self._description = description
        self._effect = effect
        self._actors = actors
        self._condition = condition

    def execute(self, request: PBacRequest) -> Effect:
        actors_decision = self._actors.execute(request.target, request.subject) if self._actors else Effect.NOT_APPLICABLE
        if actors_decision is Effect.NOT_APPLICABLE or not actors_decision:
            return Effect.NOT_APPLICABLE

        pack = EntityPack(action=request.action, entities=(request.target, request.subject))

        condition_decision = self._condition.execute(pack) if self._condition else Effect.NOT_APPLICABLE
        if condition_decision is Effect.NOT_APPLICABLE or not condition_decision:
            return Effect.NOT_APPLICABLE

        return self._effect


class Policy:
    def __init__(
        self,
        _id: str,
        description: str,
        algorithm: Algorithm,
        actors:  Optional[ActorCombiner | ActorResolver] = None,
        condition: Type[EntityCombiner | EntityAttribute] = None,
        rules: Optional[Iterable[Rule]] = None,
    ):
        self._id = _id
        self._description = description
        self._algorithm = algorithm
        self._actors = actors
        self._condition = condition
        self._rules = rules if rules is not None else []

    def execute(self, request: PBacRequest) -> Effect:
        actors_decision = self._actors.execute(request.target, request.subject) if self._actors else Effect.NOT_APPLICABLE

        if actors_decision is Effect.NOT_APPLICABLE or not actors_decision:
            return Effect.NOT_APPLICABLE

        pack = EntityPack(action=request.action, entities=[request.target, request.subject])

        condition_decision = self._condition.execute(pack) if self._condition else Effect.NOT_APPLICABLE

        if condition_decision is Effect.NOT_APPLICABLE or not condition_decision:
            return Effect.NOT_APPLICABLE

        return CombineResolver.combine(self._algorithm, (rule.execute(request) for rule in self._rules))


class Group:
    def __init__(
        self,
        _id: str,
        description: str,
        algorithm: Algorithm,
        items: Iterable[Policy | Rule | Self],
    ):
        self._id = _id
        self._description = description
        self._algorithm = algorithm
        self._items = items

    def execute(self, request: PBacRequest):
        return CombineResolver.combine(self._algorithm, (item.execute(request) for item in self._items))
