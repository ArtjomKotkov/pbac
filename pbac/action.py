from base import Executable

from models import EntityPack


class MetaAction(type):
    def __eq__(self, action):
        return ActionResolver(action)


class Action(metaclass=MetaAction): ...


class ActionResolver(Executable):
    def __init__(self, action: str):
        self._action = action

    def execute(self, pack: EntityPack) -> bool:
        return pack.action == self._action
