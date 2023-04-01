from enum import StrEnum


__all__ = [
    'Algorithm',
    'Effect',
    'Actions',
    'ActorType',
]


class Algorithm(StrEnum):
    PERMIT_UNLESS_DENY = 'permit_unless_deny'
    DENY_UNLESS_PERMIT = 'deny_unless_permit'
    PERMIT_OVERRIDES = 'permit_overrides'
    DENY_OVERRIDES = 'deny_overrides'


class Effect(StrEnum):
    PERMIT = 'permit'
    DENY = 'deny'
    NOT_APPLICABLE = 'not_applicable'


class Actions(StrEnum):
    READ = 'read'
    WRITE = 'write'
    UPDATE = 'update'
    DELETE = 'delete'
    ACCESS = 'access'


class ActorType(StrEnum):
    TARGET = 'target'
    SUBJECT = 'subject'
    CONTEXT = 'context'
