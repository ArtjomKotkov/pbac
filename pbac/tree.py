from typing import Iterable, Self, Optional, Type, Any

from .base import Executable
from .const import Algorithm, Effect
from .entity import EntityCombiner, EntityAttribute
from .actor import ActorCombiner, ActorResolver
from .exceptions import NotApplicable
from .combine_resolver import CombineResolver


class Rule(Executable):
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

    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Effect:
        if self._actors:
            actors_decision = self._actors.execute(subject, target, action, context) if self._actors else Effect.NOT_APPLICABLE
            if actors_decision is Effect.NOT_APPLICABLE or not actors_decision:
                return Effect.NOT_APPLICABLE

        if self._condition:
            try:
                condition_decision = self._condition.execute(subject, target, action, context) if self._condition else Effect.NOT_APPLICABLE
            except NotApplicable:
                condition_decision = Effect.NOT_APPLICABLE

            if condition_decision is Effect.NOT_APPLICABLE or not condition_decision:
                return Effect.NOT_APPLICABLE

        return self._effect


class Policy(Executable):
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

    def execute(self, subject: Any, target: Any, action: str, context: Any) -> Effect:
        if self._actors:
            actors_decision = self._actors.execute(subject, target, action, context) if self._actors else Effect.NOT_APPLICABLE

            if actors_decision is Effect.NOT_APPLICABLE or not actors_decision:
                return Effect.NOT_APPLICABLE
        if self._condition:
            try:
                condition_decision = self._condition.execute(subject, target, action, context) if self._condition else Effect.NOT_APPLICABLE
            except NotApplicable:
                condition_decision = Effect.NOT_APPLICABLE

            if condition_decision is Effect.NOT_APPLICABLE or not condition_decision:
                return Effect.NOT_APPLICABLE

        return CombineResolver.combine(
            self._algorithm,
            (rule.execute(subject, target, action, context) for rule in self._rules),
        )


class Group(Executable):
    def __init__(
        self,
        _id: str,
        description: str,
        algorithm: Algorithm,
        items: Iterable[Policy | Rule | Self],
        actors: Optional[ActorCombiner | ActorResolver] = None,
        condition: Type[EntityCombiner | EntityAttribute] = None,
    ):
        self._id = _id
        self._description = description
        self._algorithm = algorithm
        self._items = items
        self._actors = actors
        self._condition = condition

    def execute(self, subject: Any, target: Any, action: str, context: Any):
        if self._actors:
            actors_decision = self._actors.execute(subject, target, action, context) if self._actors else Effect.NOT_APPLICABLE

            if actors_decision is Effect.NOT_APPLICABLE or not actors_decision:
                return Effect.NOT_APPLICABLE

        if self._condition:
            try:
                condition_decision = self._condition.execute(subject, target, action, context) if self._condition else Effect.NOT_APPLICABLE
            except NotApplicable:
                condition_decision = Effect.NOT_APPLICABLE

            if condition_decision is Effect.NOT_APPLICABLE or not condition_decision:
                return Effect.NOT_APPLICABLE

        return CombineResolver.combine(
            self._algorithm,
            (item.execute(subject, target, action, context) for item in self._items),
        )
