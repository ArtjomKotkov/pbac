from enum import Enum

from modeller import SModel
from pydantic import BaseModel


__all__ = [
    'Algorithm',
    'Effect',
    'Actions',
    'EntityType',
    'ActorType',
    'MODEL',
    'PATCH_NODE',
]

MODEL = SModel | BaseModel


PATCH_NODE = "ab2d6311-7240-44dd-8ad9-0e9f09f70932"


class Algorithm:
    PERMIT_UNLESS_DENY = 1
    DENY_UNLESS_PERMIT = 2
    PERMIT_OVERRIDES = 3
    DENY_OVERRIDES = 4


class Effect:
    PERMIT = 1
    DENY = 2
    NOT_APPLICABLE = 3


class Actions(Enum):
    READ = 1
    WRITE = 2
    UPDATE = 3
    DELETE = 4


class EntityType(Enum):
    TARGET = 1
    SUBJECT = 2
    ACTION = 3
    OTHER = 4


class ActorType(Enum):
    TARGET = 1
    SUBJECT = 2
