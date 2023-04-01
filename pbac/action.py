from typing import Any

from .base import Executable


class MetaAction(type):
    def __eq__(self, action):
        return ActionResolver(action)


class Action(metaclass=MetaAction):
    ...


class ActionResolver(Executable):
    def __init__(self, action: str):
        self._action = action

    def execute(self, subject: Any, target: Any, action: str, context: Any) -> bool:
        return action == self._action
